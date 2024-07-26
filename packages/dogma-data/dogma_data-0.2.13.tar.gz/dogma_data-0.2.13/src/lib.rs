#![allow(clippy::type_complexity)]
mod fasta;
mod data;
pub mod parallel;

use crate::parallel::permute::Permute;

use std::collections::HashMap;

use fasta::{ParsedFasta, SubClusterHeader, TaxonIdHeader};

// use indicatif::{ParallelProgressIterator, ProgressIterator, ProgressStyle};
use pyo3::prelude::*;
use pyo3::types::{PyList, PyTuple};
use numpy::{IntoPyArray, PyArray1, PyArrayDescrMethods, PyReadonlyArray1, PyUntypedArray, PyUntypedArrayMethods};
use crate::data::{AwkwardArray, TreatAsByteSlice};


impl<'a, T: Clone + Sync> From<Bound<'a, PyTuple>> for AwkwardArray<'a, T> {
    fn from(value: Bound<'a, PyTuple>) -> Self {
        let _content = value.get_item(0);
        todo!()
    }
}

#[pyfunction]
fn parse_fasta<'py>(py: Python<'py>, path: &str, mapping: &FastaMapping) -> PyResult<(Bound<'py, PyArray1<u8>>, Bound<'py, PyArray1<isize>>, Bound<'py, PyArray1<u32>>)> {

    let ParsedFasta{sequences: AwkwardArray {content, cu_seqlens}, headers} = fasta::parse_fasta::<TaxonIdHeader>(path, mapping)?;

    let content = content.into_owned().into_pyarray_bound(py);
    let cu_seqlens = cu_seqlens.into_owned().into_pyarray_bound(py);
    let headers = headers.into_iter().map(|h| h.taxon_id).collect::<Vec<_>>().into_pyarray_bound(py);
    Ok((content, cu_seqlens, headers))
}

#[pyfunction]
fn parse_cluster_member_fasta<'py>(py: Python<'py>, path: &str, mapping: &FastaMapping) -> PyResult<(Bound<'py, PyArray1<u8>>, Bound<'py, PyArray1<isize>>, Bound<'py, PyArray1<u32>>, Bound<'py, PyArray1<u32>>)> {
    let ParsedFasta{sequences: AwkwardArray {content, cu_seqlens}, headers} = fasta::parse_fasta::<SubClusterHeader>(path, &mapping)?;

    println!("Finished parsing fasta, moving things to Python");
    let content = content.into_owned().into_pyarray_bound(py);
    let cu_seqlens = cu_seqlens.into_owned().into_pyarray_bound(py);
    let (taxon_ids, supercluster_ids) = headers.into_iter().map(|h| (h.taxon_id, h.supercluster_id)).unzip::<_, _, Vec<_>, Vec<_>>();

    // println!("Computing superclusters");
    // let argsorted = data::argsort(&supercluster_ids);

    let taxon_ids = taxon_ids.into_pyarray_bound(py);
    let supercluster_ids = supercluster_ids.into_pyarray_bound(py);
    // let hashmap = HashMap::new();
    println!("Returning!");
    Ok((content, cu_seqlens, taxon_ids, supercluster_ids))
}


#[pyfunction]
fn concatenate_awkward<'py>(py: Python<'py>, arrays: Bound<'py, PyList>) -> PyResult<(Bound<'py, PyArray1<u8>>, Bound<'py, PyArray1<isize>>)> {
    let awkwards: Vec<AwkwardArray<_>> = arrays.iter().map(|obj| {
        let tuple = obj.downcast::<PyTuple>()?;
        let tup_content = tuple.get_item(0)?;
        let tup_cu_seqlens = tuple.get_item(1)?;
        let content = tup_content.downcast::<PyUntypedArray>()?;
        let cu_seqlens = tup_cu_seqlens.downcast::<PyUntypedArray>()?;

        let content: &[u8] = unsafe { content.as_slice() }?;
        let cu_seqlens: &[isize] = unsafe { cu_seqlens.as_slice() }?;
        Ok(AwkwardArray::<u8>::new(content, cu_seqlens))
    }).collect::<PyResult<_>>()?;

    let awkward_refs = awkwards.iter().collect::<Vec<_>>();

    let AwkwardArray {content, cu_seqlens} = AwkwardArray::parallel_concatenate(&awkward_refs);

    Ok((content.into_owned().into_pyarray_bound(py), cu_seqlens.into_owned().into_pyarray_bound(py)))
}


#[pyfunction]
fn concatenate_numpy<'py>(py: Python<'py>, arrays: Bound<'py, PyList>) -> PyResult<(Bound<'py, PyArray1<u8>>, Bound<'py, PyArray1<isize>>)> {
    // Takes in a list of numpy arrays of the same dtype, and concatenates them into a single numpy array
    // The output array is always of dtype u8, so must be casted to the correct dtype after concatenation using `numpy.ndarray.view(dtype)`
    
    let buf_refs: Vec<_> = arrays.iter().map(|obj| -> PyResult<_> {
        let arr = obj.downcast::<PyUntypedArray>()?;
        Ok((arr.dtype(), unsafe{let arr = *arr.as_array_ptr(); arr.data}, arr.len(), arr.is_contiguous()))
    }).collect::<PyResult<_>>()?;
    let first_dtype = &buf_refs[0].0;

    let all_dtypes_match = buf_refs.iter().all(|(dtype, _ptr, _len, contiguous)| first_dtype.is_equiv_to(dtype) && *contiguous);
    if !all_dtypes_match {
        return Err(pyo3::exceptions::PyValueError::new_err("All arrays must have the same dtype and be contiguous"));
    }

    let itemsize = first_dtype.itemsize();

    let slices: Vec<&[u8]> = buf_refs.iter().map(|(_dtype, ptr, len, _contiguous)| unsafe { std::slice::from_raw_parts(*ptr as *const u8, len * itemsize) }).collect();

    let (sequences, mut cu_seqlens) = parallel::parallel_concatenate_buffers(&slices);
    cu_seqlens.push(sequences.len() as isize);  // Add the final index
    
    let sequences = sequences.into_pyarray_bound(py);
    let cu_seqlens = cu_seqlens.into_pyarray_bound(py);

    Ok((sequences, cu_seqlens))
}

#[pyfunction]
fn awkward_from_list_of_numpy<'py>(py: Python<'py>, arrays: Bound<'py, PyList>) -> PyResult<Bound<'py, PyTuple>> {
    if arrays.len() == 0 {
        return Err(pyo3::exceptions::PyValueError::new_err("Must provide at least one array"));
    }
    struct ArrStorage {
        data: *const u8,
        len: usize,
    }
    unsafe impl Sync for ArrStorage {}

    let mut first_dtype = None;
    let buf_refs: Vec<_> = arrays.iter().map(|obj| -> PyResult<_> {
        let arr = obj.downcast::<PyUntypedArray>()?;
        let arrobj = unsafe {*arr.as_array_ptr()};
        match &mut first_dtype {
            None => {first_dtype = Some(arr.dtype());},
            Some(first) => {
                if !first.is_equiv_to(&arr.dtype()) {
                    return Err(pyo3::exceptions::PyValueError::new_err("All arrays must have the same dtype"));
                }
            }
        };
        if !arr.is_contiguous() {
            return Err(pyo3::exceptions::PyValueError::new_err("All arrays must be contiguous"));
        }
        Ok(ArrStorage{data: arrobj.data as *const u8, len: arr.len()})
    }).collect::<PyResult<_>>()?;

    let first_dtype = first_dtype.unwrap();

    let itemsize: usize = first_dtype.itemsize();

    let slices: Vec<&[u8]> = buf_refs.into_iter().map(|arr| unsafe { std::slice::from_raw_parts(arr.data, arr.len * itemsize) }).collect();

    let (content, mut cu_seqlens) = parallel::parallel_concatenate_buffers(&slices);
    cu_seqlens.push(content.len() as isize);  // Add the final index

    let content_arr = content.into_pyarray_bound(py);
    let cu_seqlens_arr = cu_seqlens.into_pyarray_bound(py);

    Ok(PyTuple::new_bound(py, &[content_arr.to_object(py), cu_seqlens_arr.to_object(py)]))
}

fn find_boundaries<T: Eq>(arr: &[T]) -> Vec<isize>{
    let mut boundaries = vec![0];
    for i in 1..arr.len() - 1 {
        if arr[i] != arr[i - 1] {
            boundaries.push(i as isize);
        }
    }
    boundaries.push(arr.len() as isize);
    boundaries
}

#[pyfunction]
fn find_boundaries_u32<'py>(py: Python<'py>, array: PyReadonlyArray1<'py, u32>) -> PyResult<Bound<'py, PyArray1<isize>>> {
    let array = array.as_slice()?;
    let boundaries = find_boundaries(array);
    Ok(boundaries.into_pyarray_bound(py))
}


// #[pyfunction]
// fn fast_pack<'py>(
//     starts: DogmaSlice<'py, isize>,
//     stops: Bound<PyArray1<isize>>,
//     content: Bound<'py, PyUntypedArray>,
//     nthreads: usize,
// ) -> PyResult<(PyArray1<u8>, PyArray1<isize>)> {

//     let stops = unsafe { stops.as_slice()? };

//     let starts_slice = starts.0;
    
//     let dtype_width = content.dtype().itemsize();
//     let content_bytes: &[u8] = unsafe { content.as_slice() }? ;

//     Ok(())
// }


// struct JaggedArray<'py, T>(&'py [T], &'py [isize]);

// impl<'py, T: numpy::Element> FromPyObject<'py> for JaggedArray<'py, T> {
//     fn extract_bound(ob: &Bound<'py, PyAny>) -> PyResult<Self> {
//         let tup = ob.downcast::<PyTuple>()?;
//         let data = tup.get_item(0)?.downcast::<PyArray1<T>>()?;
//         let offsets = tup.get_item(1)?.downcast::<PyArray1<isize>>()?;
//         Ok(JaggedArray(unsafe { data.as_slice() }?, unsafe { offsets.as_slice() }?))
//     }
// }

// impl<'py, T> JaggedArray<'py, T> {
//     fn len(&self) -> usize {
//         self.1.len() - 1
//     }

//     fn get(&self, i: usize) -> &[T] {
//         let start = self.1[i] as usize;
//         let end = self.1[i + 1] as usize;
//         &self.0[start..end]
//     }

//     fn reorder(&self, py: Python<'py>, order: &[isize]) -> Self {
//         let mut new_offsets = unsafe {numpy::PyArray1::new_bound(py, [order.len() + 1], false) };

//         let mut new_data = 
//     }
    
// }

#[pyclass]
struct FastaMapping {
    pub mapping: Vec<(u8, u8)>,
    pub default_value: u8,
}

#[pymethods]
impl FastaMapping {
    #[new]
    fn new(mapping: HashMap<String, isize>, default_value: isize) -> PyResult<Self> {
        let mut tuples_mapping = vec![];
        let mut warn_unused = vec![];
        for (k, v) in mapping.iter() {
            if k.len() != 1 {
                warn_unused.push(k.as_str());
                continue
            }
            tuples_mapping.push((k.as_bytes()[0], *v as u8));
        }

        if !warn_unused.is_empty() {
            eprintln!("Warning: The following keys were not used in the mapping: {:?}", warn_unused);
        }

        let default_value = u8::try_from(default_value)?;

        Ok(Self {mapping: tuples_mapping, default_value})
    }

    fn __str__(&self) -> PyResult<String> {
        let mut s = String::new();
        s.push_str("CharMapping({\n");
        for (k, v) in self.mapping.iter() {
            s.push_str(&format!("{} -> {}\n", *k as char, *v));
        }
        s.push_str(&format!("<default> -> {}\n", self.default_value));
        s.push_str("})");
        Ok(s)
    }

    fn __repr__(&self) -> PyResult<String> {
        self.__str__()
    }
}

#[pyfunction]
fn permute_awkward<'py>(py: Python<'py>, mut awkward: AwkwardArray<'py, u8>, permutation: Vec<usize>) -> PyResult<(Bound<'py, PyArray1<u8>>, Bound<'py, PyArray1<isize>>)> {
    println!("awkward len: {:?} permutation: {:?}", awkward.len(), permutation);
    (&mut awkward).permute(permutation);
    Ok((awkward.content.into_owned().into_pyarray_bound(py), awkward.cu_seqlens.into_owned().into_pyarray_bound(py)))
}


/// Assumes the input array is pre-bounded to the maximum sequence length, and that it is sorted in descending order
#[pyfunction]
fn find_chunk_boundaries<'py>(py: Python<'py>, sequence_lengths: PyReadonlyArray1<'py, isize>, chunk_tokens: isize) -> PyResult<Bound<'py, PyArray1<isize>>> {
    let sequence_lengths = sequence_lengths.as_slice()?;

    let mut boundaries = vec![0];
    let mut running_length = 0;
    let mut current_start = sequence_lengths[0];
    for (i, &current_len) in sequence_lengths.iter().enumerate() {
        running_length += current_start;
        // If adding this length to the running length would exceed the chunk size, add a boundary at this new sample.
        if running_length > chunk_tokens {
            boundaries.push(i as isize);
            running_length = current_len;
            current_start = current_len;
        }
    }

    if *boundaries.last().unwrap() != sequence_lengths.len() as isize {
        boundaries.push(sequence_lengths.len() as isize);
    }

    // Assert that all the boundaries are valid
    for i in 1..boundaries.len() {
        let start = boundaries[i - 1] as usize;
        let end = boundaries[i] as usize;
        let start_element_size = sequence_lengths[start];
        let chunk_len = start_element_size * (end - start) as isize;
        assert!(chunk_len <= chunk_tokens, "Chunk length {} exceeds chunk size {}", chunk_len, chunk_tokens);
    }

    Ok(boundaries.into_pyarray_bound(py))
}

/// A Python module implemented in Rust.
#[pymodule]
#[pyo3(name="dogma_rust")]
fn dogma_rust(_py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(parse_fasta, m)?)?;
    m.add_function(wrap_pyfunction!(concatenate_numpy, m)?)?;
    m.add_function(wrap_pyfunction!(concatenate_awkward, m)?)?;
    m.add_function(wrap_pyfunction!(awkward_from_list_of_numpy, m)?)?;
    m.add_function(wrap_pyfunction!(parse_cluster_member_fasta, m)?)?;
    m.add_function(wrap_pyfunction!(permute_awkward, m)?)?;
    m.add_function(wrap_pyfunction!(find_boundaries_u32, m)?)?;
    m.add_function(wrap_pyfunction!(find_chunk_boundaries, m)?)?;
    m.add_class::<FastaMapping>()?;
    Ok(())
}
