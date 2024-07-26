
use std::str::FromStr;

use thiserror::Error;
use numpy::Element;
use std::fmt::Debug;

#[derive(Debug, Clone, Copy)]
pub struct SubClusterHeader {
    pub taxon_id: u32,
    pub supercluster_id: u32,
}

#[derive(Debug, Clone, Copy)]
pub struct TaxonIdHeader{
    pub taxon_id: u32,
}

pub trait Header: FromStr + Clone + Copy + Debug + Send + Sync {}

unsafe impl Element for TaxonIdHeader {
    const IS_COPY: bool = true;

    fn get_dtype_bound(py: pyo3::prelude::Python<'_>) -> pyo3::prelude::Bound<'_, numpy::PyArrayDescr> {
        numpy::dtype_bound::<u32>(py)
    }
}

#[derive(Error, Debug)]
pub enum HeaderParseError {
    #[error("Failed to parse integer in header")]
    IntParseError(#[from] std::num::ParseIntError),
    #[error("Header was malformed")]
    ParseError,
}

impl FromStr for SubClusterHeader {
    type Err = HeaderParseError;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let mut parts = s.split_whitespace();
        let taxon_id = parts.next().unwrap().parse::<u32>()?;
        let supercluster_id = parts.next().ok_or(HeaderParseError::ParseError)?.parse::<u32>()?;
        Ok(SubClusterHeader {
            taxon_id,
            supercluster_id,
        })
    }
}

impl FromStr for TaxonIdHeader {
    type Err = HeaderParseError;
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let taxon_id = s.parse::<u32>()?;
        Ok(TaxonIdHeader {
            taxon_id,
        })
    }
}


impl Header for TaxonIdHeader {}
impl Header for SubClusterHeader {}