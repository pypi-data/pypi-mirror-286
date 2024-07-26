use crate::parallel::parallel_concatenate_buffers;
use std::borrow::Cow;
use numpy::{PyArray1, PyArrayDescrMethods, PyArrayMethods, PyUntypedArray, PyUntypedArrayMethods};
use rayon::prelude::*;
use pyo3::{exceptions::PyValueError, prelude::*, types::PyTuple};

#[derive(Clone, Debug)]
pub struct AwkwardArray<'a, T>
where T: Clone {
    pub content: Cow<'a, [T]>,
    pub cu_seqlens: Cow<'a, [isize]>,
}

impl<'py, T: Clone + numpy::Element + Send + Sync> FromPyObject<'py> for AwkwardArray<'py, T> {
    fn extract_bound(ob: &Bound<'py, PyAny>) -> PyResult<Self> {
        println!("starting extraction");
        let tup = ob.downcast::<PyTuple>()?;
        let tup_content = &tup.get_item(0)?;
        let content = tup_content.downcast::<PyArray1<T>>()?; 
        let tup_offsets = tup.get_borrowed_item(1)?;
        let offsets = tup_offsets.downcast::<PyArray1<isize>>()?;

        let content: Vec<T> = unsafe { content.as_slice() }?.to_owned();
        let offsets: Vec<isize> = unsafe { offsets.as_slice() }?.to_owned();
        // let cu_seqlens = ob.getattr("cu_seqlens")?.extract()?;
        // Ok(AwkwardArray::new(content, cu_seqlens))
        Ok(AwkwardArray::new(Cow::from(content), Cow::from(offsets)))
    }
}


pub fn argsort<T: Ord>(data: &[T]) -> Vec<usize> {
    let mut indices = (0..data.len()).collect::<Vec<_>>();
    indices.sort_by_key(|&i| &data[i]);
    indices
}



impl<'a, T: Sync + Clone> AwkwardArray<'a, T> {
    pub fn new(content: impl Into<Cow<'a, [T]>>, cu_seqlens: impl Into<Cow<'a, [isize]>>) -> Self {
        AwkwardArray {
            content: content.into(),
            cu_seqlens: cu_seqlens.into(),
        }
    }

    pub fn parallel_concatenate(arrs: &[&AwkwardArray<'_, T>]) -> AwkwardArray<'static, T> {
        let content_buffers: Vec<&[T]> = arrs.iter().copied().map(|arr| arr.content.as_ref()).collect();
        let (cat_content, _) = parallel_concatenate_buffers(&content_buffers);

        let cu_seqlen_offsets: Vec<isize> = arrs.iter().copied().scan(0, |acc, arr| {
            let start = *acc;
            *acc += arr.cu_seqlens.last().copied().unwrap_or(0);
            Some(start)
        }).collect();

        let shifted_cu_seqlens = arrs.par_iter().zip(cu_seqlen_offsets).map(|(arr, offset)| {
            if offset == 0 {
                arr.cu_seqlens.to_vec()
            } else {
                let mut shifted = (arr.cu_seqlens[1..]).to_vec(); // Skip the first element
                shifted.iter_mut().for_each(|cu_seqlen| *cu_seqlen += offset);
                shifted
            }
        }).collect::<Vec<_>>();

        let shifted_cu_seqlens_refs: Vec<&[isize]> = shifted_cu_seqlens.iter().map(|cu_seqlens| {
            cu_seqlens.as_slice()
        }).collect();

        let (out_cu_seqlens, _) = parallel_concatenate_buffers(&shifted_cu_seqlens_refs);


        AwkwardArray::new(cat_content, out_cu_seqlens)
    }
}

impl<'a, T: Clone> AwkwardArray<'a, T> {
    pub fn len(&self) -> usize {
        self.cu_seqlens.len() - 1
    }
}


impl<'a, T> std::ops::Index<usize> for AwkwardArray<'a, T>
where
    T: Clone,
{
    type Output = [T];
    fn index(&self, index: usize) -> &Self::Output {
        let start = self.cu_seqlens[index] as usize;
        let end = self.cu_seqlens[index + 1] as usize;
        &self.content[start..end]
    }
}

pub trait TreatAsByteSlice<'a, T> {
    unsafe fn as_slice(&self) -> PyResult<&'a [T]>;
}

impl<'a, T> TreatAsByteSlice<'a, T> for Bound<'a, PyUntypedArray> {
    unsafe fn as_slice(&self) -> PyResult<&'a [T]> {
        if !self.is_contiguous(){
            return Err(PyValueError::new_err("Array is not contiguous"));
        }
        let arr = *self.as_array_ptr();
        let dtype_width = self.dtype().itemsize();
        Ok(std::slice::from_raw_parts(arr.data as *const T, self.len() * dtype_width / std::mem::size_of::<T>()))
    }
}