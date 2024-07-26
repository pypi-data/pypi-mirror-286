from dogma.vocab import AA_VOCAB
from dogma_data.dogma_rust import parse_cluster_member_fasta, FastaMapping

full_vocab = AA_VOCAB.get_stoi()

rna_default_value = full_vocab["<unk>"]
aa_default_value = full_vocab["<aaunk>"]

mapping = FastaMapping(full_vocab, default_value=rna_default_value)
print(mapping)
content, cu_seqlens, taxon_id, parent_cluster_id = parse_cluster_member_fasta("/dev/shm/uniref90_PROC.fasta", mapping)
print(len(parent_to_children_idx))