import zarr
import s3fs
import dogma_data.compression
import numpy as np
import awkward as ak
from dogma_data.dogma_rust import FastaMapping, parse_cluster_member_fasta, find_boundaries_u32
from dogma.vocab import AA_VOCAB
from random import randrange
import fsspec
from fsspec.implementations.cached import WholeFileCacheFileSystem
from tqdm.auto import trange

from numcodecs import Blosc

def save_test():

    # s3 = s3fs.S3FileSystem()
    # store = s3fs.S3Map(root='ai-residency-stanford-snap-uce/', s3=s3, check=False, create=True)

    # cache = zarr.LRUStoreCache(store, max_size=None)
    store = zarr.DirectoryStore('protref90_clustered50_zarr')
    root = zarr.group(store=store, path='')
    # group = root.create_group('protref90_clustered50_zarr', overwrite=True)
    group = root

    fm = FastaMapping(AA_VOCAB.get_stoi(), default_value=AA_VOCAB['<aaunk>'])
    tokens, tokens_cu_seqlens, taxon_ids, supercluster_ids = parse_cluster_member_fasta("/dev/shm/uniref90_PROC.fasta", fm)
    print(tokens.shape, tokens_cu_seqlens.shape, taxon_ids.shape, supercluster_ids.shape)
    print(tokens.dtype, tokens_cu_seqlens.dtype, taxon_ids.dtype, supercluster_ids.dtype)

    compressor = Blosc(cname='zstd', clevel=3, shuffle=Blosc.SHUFFLE)

    by_supercluster_ids = np.argsort(supercluster_ids)
    idx_for_supercluster_id = np.stack((supercluster_ids, np.arange(len(supercluster_ids), dtype=np.uint32)), axis=0)[:, by_supercluster_ids]
    print(f"{idx_for_supercluster_id=}")
    print(f'{idx_for_supercluster_id[0].dtype=}')
    supercluster_boundaries = find_boundaries_u32(np.ascontiguousarray(idx_for_supercluster_id[0])).astype(np.uint32)
    # supercluster_ids_unique = idx_for_supercluster_id[0][supercluster_boundaries[:-1]]
    # np.testing.assert_array_equal(supercluster_ids_unique, np.unique(supercluster_ids))
    # print('Passed equal')
    # print(f"{supercluster_ids_unique.dtype=}, {supercluster_boundaries.dtype=}")
    # print(f"{supercluster_ids_unique=}")
    # print(f"{supercluster_boundaries=}")
    # print(f"{supercluster_ids_unique.nbytes=}")
    # print(f'{supercluster_boundaries.nbytes=}')
    # exit()

    write_kwargs = {'compressor': compressor, 'overwrite': True, 'chunks': (2**15,), 'dtype': 'u8'}

    z_tokens = group.array('tokens', tokens, **write_kwargs)
    z_tokens_cu_seqlens = group.array('tokens_cu_seqlens', tokens_cu_seqlens, **write_kwargs)
    z_taxon_ids = group.array('taxon_ids', taxon_ids, **write_kwargs)
    z_supercluster_ids_unique = group.array('supercluster_ids_unique', supercluster_ids, **write_kwargs)
    z_supercluster_boundaries = group.array('supercluster_boundaries', supercluster_boundaries, **write_kwargs)



class CachedRemoteSeqs:
    def __init__(self, path_relto_datasets: str = 'protref90_clustered50_zarr'):
        # Keep the 
        # self.fs: WholeFileCacheFileSystem = fsspec.filesystem("filecache", target_protocol='s3',
        #                             cache_storage='./data_cache')
        # self.s3 = s3fs.S3FileSystem(cache_regions=True)
        # self.store = s3fs.S3Map(root='ai-residency-stanford-snap-uce/datasets', s3=self.s3, check=True, create=False)
        # self.store = self.fs.get_mapper(root='ai-residency-stanford-snap-uce/datasets', check=True)
        self.store = zarr.DirectoryStore('protref90_clustered50_zarr')
        # self.cache = zarr.LRUStoreCache(self.store, max_size=None)  # This is in-memory cache
        # self.group = zarr.group(store=datasets, path=path_relto_datasets)
        self.group = zarr.group(store=self.store, path='')
        print('Loading superclusters')
        self.supercluster_ids = self.group['supercluster_ids_unique'][:]
        self.supercluster_boundaries = self.group['supercluster_boundaries']
        self.tokens_cu_seqlens = self.group['tokens_cu_seqlens']
        self.tokens = self.group['tokens']
        self.taxon_ids = self.group['taxon_ids']
        print(self.supercluster_ids.nbytes)
        print('Loaded superclusters')
    
    def __getitem__(self, item):
        if isinstance(item, int):
            supercluster_id = self.supercluster_ids[item]
            start_clust, end_clust = self.supercluster_boundaries[supercluster_id:supercluster_id+2]
            # random_seq_idx = randrange(start_clust, end_clust)
            random_seq_idx = randrange(start_clust, start_clust + 1)
            start, end = self.tokens_cu_seqlens[random_seq_idx:random_seq_idx+2]
            tokens = self.tokens[start:end]
            taxon_id = self.taxon_ids[random_seq_idx]
            return {'tokens': tokens, 'taxon_id': taxon_id, 'supercluster_id': supercluster_id} 
        # elif isinstance(item, np.ndarray):
        #     supercluster_ids = self.supercluster_ids[item]
        #     start_clusts, end_clusts = self.supercluster_boundaries[supercluster_ids], self.supercluster_boundaries[supercluster_ids + 1]
        #     random_seq_idcs = np.random.randint(start_clusts, end_clusts)
        #     starts, ends = self.tokens_cu_seqlens[random_seq_idcs], self.tokens_cu_seqlens[random_seq_idcs + 1]
        #     np.take
        #     tokens = self.tokens
    
    def __len__(self):
        return len(self.supercluster_ids)
    
    # def save_dataset(self, arr: ak.Array):
        
if __name__ == '__main__':
    # save_test()
    crs = CachedRemoteSeqs()
    print('Init finished')
    for i in trange(len(crs)):
        s = crs[i]
    print('Loaded')
    # print(la[100:500])