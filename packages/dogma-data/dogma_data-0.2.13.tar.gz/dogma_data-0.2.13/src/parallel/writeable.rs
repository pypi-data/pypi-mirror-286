use std::cell::UnsafeCell;

use rayon::prelude::*;


pub struct ParallelWriter<T> {
    pub inner: UnsafeCell<T>
}

impl<T> ParallelWriter<T> {
    pub fn new(inner: T) -> Self {
        ParallelWriter { inner: UnsafeCell::from(inner) }
    }
    pub unsafe fn get_mut(&self) -> &mut T {
        let inner_ptr = self.inner.get();
        unsafe { &mut *inner_ptr }
    }
}

unsafe impl<T> Sync for ParallelWriter<T> where T: Sync {}