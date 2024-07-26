use crate::FastaMapping;
use std::ops::Index;

pub struct CharMapping {
    mappings: [u8; 256],
}

impl CharMapping {
    pub fn from_pairs(mapping_pairs: &[(u8, u8)], default_value: u8) -> Self {
        let mut mappings = [default_value; 256];
        for (k, v) in mapping_pairs {
            mappings[*k as usize] = *v;
        }
        CharMapping {
            mappings,
        }
    }
}

impl From<&FastaMapping> for CharMapping {
    fn from(fasta_mapping: &FastaMapping) -> Self {
        CharMapping::from_pairs(&fasta_mapping.mapping, fasta_mapping.default_value)
    }
}

impl Index<u8> for CharMapping {
    type Output = u8;

    fn index(&self, index: u8) -> &Self::Output {
        &self.mappings[index as usize]
    }
}
