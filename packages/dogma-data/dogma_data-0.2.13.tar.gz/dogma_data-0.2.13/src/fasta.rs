mod header;
mod atcg;

use crate::fasta::atcg::CharMapping;
use crate::FastaMapping;
use std::{collections::HashMap, fs::File};
use std::io::Read;
use rayon::prelude::*;
use crate::data::AwkwardArray;
use crate::parallel::parallel_concatenate_buffers;
use indicatif::{ProgressBar, ProgressStyle};
use eyre::Result;

pub use header::{TaxonIdHeader, SubClusterHeader};

use self::header::Header;

// Any fasta mapping can be stored in a vector of 256 elements
pub struct ParsedFasta<H> {
    pub sequences: AwkwardArray<'static, u8>,
    pub headers: Vec<H>,
}

fn parse_fasta_chunk<H>(text: &[u8], start_i: usize, end_i: usize, mapping: &atcg::CharMapping) -> Result<ParsedFasta<H>>
where
    H: Header,
    H::Err: 'static + std::fmt::Debug + std::error::Error + Send + Sync
{
    let use_progress = start_i == 0;
    let progress_bar = if use_progress { Some(ProgressBar::new(end_i as u64).with_message("Parsing FASTA")) } else { None };
    let mut out_content = vec![];
    let mut out_cu_seqlens = vec![0];
    let mut out_headers = vec![];
    let mut i = start_i;

    let text_length = text.len();
    while i < text_length && unsafe { *text.get_unchecked(i) } != b'>' {
        // Move to first header
        i += 1;
    }

    let parse_char = |c| {
        mapping[c]
    };

    let mut current_header: Option<H> = None;

    while i < text.len() {
        let c = unsafe { *text.get_unchecked(i) };

        if c == b'>' { // New header
            if let Some(progress_bar) = &progress_bar {
                progress_bar.update(|s| s.set_pos(i as u64))
            }
            if i >= end_i { // Continue until a header shows up that has been handled by a later chunk.
                break;
            }
            let taxon_id_start = i + 1;
            // Maybe parse the header in the future?
            while i < text.len() && unsafe { *text.get_unchecked(i) } != b'\n' {
                i += 1;
            }
            let header_end_idx = i;
            let header_str = std::str::from_utf8(&text[taxon_id_start..header_end_idx]).unwrap();
            current_header = Some(header_str.parse()?);
            i += 1; // Move to next line
            continue;
        } else { // Parse one line
            while i < text_length && unsafe { *text.get_unchecked(i) } != b'\n' {
                unsafe {
                    out_content.push(parse_char(*text.get_unchecked(i)));
                }
                i += 1;
            } // Ends if newline or end of file
            i += 1;
            out_cu_seqlens.push(out_content.len() as isize);
            out_headers.push(current_header.unwrap());
        }
    }

    if let Some(progress_bar) = progress_bar {
        progress_bar.finish();
    }

    Ok(ParsedFasta {
        sequences: AwkwardArray::new(out_content, out_cu_seqlens),
        headers: out_headers,
    })
    
}

/// A header from a fasta file that indicates its supercluster
pub(crate) fn parse_fasta<H>(path: &str,
    mapping: &FastaMapping,
) -> Result<ParsedFasta<H>>
where H: Header + Send + Sync + std::fmt::Debug,
      H::Err: std::fmt::Debug + std::error::Error + Send + Sync + 'static
{
    let char_mapping: CharMapping = mapping.into();

    // Read file
    println!("Reading file");
    let source = File::open(path).unwrap();
    let file_size = source.metadata().unwrap().len();
    let reader = std::io::BufReader::new(source);
    let pb = ProgressBar::new(file_size).with_message("Reading fasta").with_style(
        ProgressStyle::with_template("{msg} {wide_bar} [{elapsed_precise}<{eta_precise}]").unwrap()
    );
    let mut data = vec![];
    pb.wrap_read(reader).read_to_end(&mut data)?;

    let mut n_threads = rayon::current_num_threads();

    let total_length = data.len();

    if total_length < 100_000 {
        n_threads = 1;
    }


    // let mapping_pairs = if is_rna {vec![
    //     (b'A', 4),
    //     (b'G', 5),
    //     (b'C', 6),
    //     (b'T', 7),
    //     (b'U', 7),
    // ]} else { vec![
    //     (b'A', 8 ),
    //     (b'C', 9 ),
    //     (b'D', 10),
    //     (b'E', 11),
    //     (b'F', 12),
    //     (b'G', 13),
    //     (b'H', 14),
    //     (b'I', 15),
    //     (b'K', 16),
    //     (b'L', 17),
    //     (b'M', 18),
    //     (b'N', 19),
    //     (b'P', 20),
    //     (b'Q', 21),
    //     (b'R', 22),
    //     (b'S', 23),
    //     (b'T', 24),
    //     (b'V', 25),
    //     (b'W', 26),
    //     (b'Y', 27),
    // ]};
    // let default_value = if is_rna {3} else {29};

    println!("Parsing file {path} in chunks");

    // let chunks = 

    let chunk_size = total_length.div_ceil(n_threads);
    let chunk_results: Vec<ParsedFasta<H>> = (0..n_threads).into_par_iter().map(|i| {
        let start_i = i * chunk_size;
        let end_i = std::cmp::min((i + 1) * chunk_size, total_length);
        // println!("Parsing chunk {} from {} to {}", i, start_i, end_i);
        let res = parse_fasta_chunk(&data, start_i, end_i, &char_mapping);
        let res = res?;
        // if i == 0 {
        //     println!("Parsed chunk {} with {:?}", i, res.headers);
        // }
        Ok(res)
    }).collect::<Result<_>>()?;


    let sequences_refs = chunk_results.iter().map(|pf| &pf.sequences).collect::<Vec<_>>();
    let headers = chunk_results.iter().map(|pf| pf.headers.as_slice()).collect::<Vec<_>>();

    let (merged_headers, _cu) = parallel_concatenate_buffers(&headers);
    // println!("{:?} -> {:?}", headers[0], merged_headers[0]);
    let merged_sequences = AwkwardArray::parallel_concatenate(&sequences_refs);
    drop(chunk_results);

    Ok(ParsedFasta {
        sequences: merged_sequences,
        headers: merged_headers,
    })
}


#[cfg(test)]
mod tests {
    use super::*;

    // #[test]
    // fn test_big_fasta() {
    //     let fasta_path = "/lfs/local/0/roed/projects/dogma-data/fasta_data/result_rep_seq.fasta";
    //     let result: ParsedFasta<i64> = parse_fasta(fasta_path, &[1, 2, 3, 4, 5], true);

    //     println!("Parsed fasta with {} sequences and {} tokens", result.sequences.cu_seqlens.len() - 1, result.sequences.content.len());
    //     println!("Got the following taxon ids: {:?}", result.headers);
    //     std::hint::black_box(&result);
    // }
}