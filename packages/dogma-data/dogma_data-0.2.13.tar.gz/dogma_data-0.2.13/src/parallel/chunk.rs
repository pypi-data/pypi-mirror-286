/// Uses the boundary function to determine where to split the array into chunks.
pub fn chunk_for_parallel<T>(arr: impl AsRef<[T]>, n_chunks: usize, boundary_fn: impl Fn(&[T], usize) -> bool) -> Vec<usize> {
    let arr = arr.as_ref();
    let len = arr.len();

    let chunk_size = len.div_ceil(n_chunks);

    let mut chunk_boundaries = vec![0];
    for i in 1..n_chunks {
        let mut j = chunk_size * i;
        while j < len && !boundary_fn(arr, j) {
            j += 1;
        }
        chunk_boundaries.push(j);
    }
    chunk_boundaries.push(len);

    chunk_boundaries
}


pub fn chunk_vec<T>(arr: &[T], n_chunks: usize, boundary_fn: impl Fn(&[T], usize) -> bool) -> Vec<&[T]> {
    let arr = arr.as_ref();
    let chunk_boundaries = chunk_for_parallel(arr, n_chunks, boundary_fn);

    chunk_boundaries.windows(2).map(|w| &arr[w[0]..w[1]]).collect()
}

pub trait AutoChunked<'a, T> {
    fn auto_chunked(self, n_chunks: usize, boundary_fn: impl Fn(&[T], usize) -> bool) -> Vec<&'a [T]>;
}

impl<'a, T> AutoChunked<'a, T> for &'a [T] {
    fn auto_chunked(self, n_chunks: usize, boundary_fn: impl Fn(&[T], usize) -> bool) -> Vec<&'a [T]> {
        chunk_vec(self, n_chunks, boundary_fn)
    }
}

impl <'a, T> AutoChunked<'a, T> for &'a Vec<T> {
    fn auto_chunked(self, n_chunks: usize, boundary_fn: impl Fn(&[T], usize) -> bool) -> Vec<&'a [T]> {
        let chunked = chunk_vec(&self, n_chunks, boundary_fn);
        chunked
    }
}



#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_chunk_for_parallel() {
        let arr = vec![1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
        let chunk_boundaries = chunk_for_parallel(&arr, 3, |_, i| i == 4 || i == 8);
        assert_eq!(chunk_boundaries, vec![0, 4, 8, 10]);
    }

    #[test]
    fn test_chunk_vec() {
        let arr = vec![1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
        let chunked = chunk_vec(&arr, 2, |a, i| a[i] == 7);
        assert_eq!(chunked, vec![&arr[0..6], &arr[6..]]);
    }

    #[test]
    fn test_auto_chunked() {
        let arr = vec![1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
        let chunked = arr.auto_chunked(3, |_, i| i % 2 == 0);
        assert_eq!(chunked, vec![&arr[0..4], &arr[4..8], &arr[8..10]]);
    }
}