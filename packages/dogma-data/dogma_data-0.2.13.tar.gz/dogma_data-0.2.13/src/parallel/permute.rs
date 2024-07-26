use std::borrow::Cow;

use rayon::prelude::*;

use crate::parallel::SendPtr;
use crate::parallel::writeable::ParallelWriter;
use crate::data::AwkwardArray;

pub trait Permute {
    fn permute(&mut self, permutation: impl AsRef<[usize]>);
}

impl<T> Permute for Vec<T>
where T: Copy + Clone + Sync + Send {
    fn permute(&mut self, permutation: impl AsRef<[usize]>) {
        let permutation = permutation.as_ref();
        assert_eq!(permutation.len(), self.len());
        let mut new_vec = Vec::with_capacity(self.len());
        unsafe {new_vec.set_len(self.len());}

        let new_vec = ParallelWriter::new(new_vec);

        let chunk_size = permutation.len().div_ceil(rayon::current_num_threads());
        permutation.par_chunks(chunk_size).enumerate().for_each(|(i_chunk, chunk)| {
            let chunk_start = i_chunk * chunk_size;
            let new_vec_ref = unsafe {new_vec.get_mut()};

            chunk.iter().enumerate().for_each(|(i, &j)| {
                new_vec_ref[chunk_start + i] = self[j];
            });
        });

        *self = new_vec.inner.into_inner();
    }
}

impl<'a, T> Permute for AwkwardArray<'a, T>
where T: Clone + Copy + Sync + Send
{
    fn permute(&mut self, permutation: impl AsRef<[usize]>) {
        let permutation = permutation.as_ref();
        assert_eq!(permutation.len(), self.len());

        let permuted_seqlens: Vec<_> = permutation.iter()
            .map(|&i| self.cu_seqlens[i + 1] - self.cu_seqlens[i])
            .collect();
        let permuted_cu_seqlens: Vec<isize> = vec![0].iter().copied().chain(permuted_seqlens.iter().scan(0, |acc, &seqlen| {
            *acc += seqlen;
            Some(*acc)
        })).collect::<Vec<_>>();

        let new_content = Vec::with_capacity(self.content.len());
        let shared_content = ParallelWriter::new(new_content);

        let chunk_size = permutation.len().div_ceil(rayon::current_num_threads());
        permutation.par_chunks(chunk_size).enumerate().for_each(|(i_chunk, chunk_permutations)| {
            // Working with a chunk of the new locations
            let new_content = unsafe { shared_content.get_mut() } ;

            for i in 0..chunk_permutations.len() - 1 {
                let permutation_idx = i_chunk + i;
                let get_from_idx = chunk_permutations[i];

                let read_data = &self.content[self.cu_seqlens[get_from_idx] as usize..self.cu_seqlens[get_from_idx + 1] as usize];

                let write_data = &mut new_content[permuted_cu_seqlens[permutation_idx] as usize..permuted_cu_seqlens[permutation_idx + 1] as usize];

                write_data.copy_from_slice(read_data);
            }
        });

        self.content = Cow::Owned(shared_content.inner.into_inner());
        self.cu_seqlens = Cow::Owned(permuted_cu_seqlens);
    }
}