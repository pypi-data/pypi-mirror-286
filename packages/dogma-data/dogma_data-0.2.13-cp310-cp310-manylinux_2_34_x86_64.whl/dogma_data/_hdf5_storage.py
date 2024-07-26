import dogma_data.compression
import numpy as np
import awkward as ak
from dogma_data.dogma_rust import FastaMapping, parse_cluster_member_fasta, find_boundaries_u32
from dogma.vocab import AA_VOCAB
from random import randrange
from tqdm.auto import trange
import hdf5plugin
from h5py import File as H5File
from dogma_data.utils import timer
from dogma_data._split import Splitter

def save_test():

    # s3 = s3fs.S3FileSystem()
    # store = s3fs.S3Map(root='ai-residency-stanford-snap-uce/', s3=s3, check=False, create=True)

    # cache = zarr.LRUStoreCache(store, max_size=None)
    # root = zarr.group(store=store, overwrite=True)

    fm = FastaMapping(AA_VOCAB.get_stoi(), default_value=AA_VOCAB['<aaunk>'])
    tokens, tokens_cu_seqlens, taxon_ids, supercluster_ids = parse_cluster_member_fasta("/dev/shm/uniref90_PROC.fasta", fm)
    print(tokens.shape, tokens_cu_seqlens.shape, taxon_ids.shape, supercluster_ids.shape)
    print(tokens.dtype, tokens_cu_seqlens.dtype, taxon_ids.dtype, supercluster_ids.dtype)

    # compressor = Blosc(cname='zstd', clevel=3, shuffle=Blosc.SHUFFLE)

    by_supercluster_ids = np.argsort(supercluster_ids)
    idx_for_supercluster_id = np.stack((supercluster_ids, np.arange(len(supercluster_ids), dtype=np.uint32)), axis=0)[:, by_supercluster_ids]
    print(f"{idx_for_supercluster_id=}")
    print(f'{idx_for_supercluster_id[0].dtype=}')
    supercluster_boundaries = find_boundaries_u32(np.ascontiguousarray(idx_for_supercluster_id[0])).astype(np.uint32)
    supercluster_ids_unique = idx_for_supercluster_id[0][supercluster_boundaries[:-1]]

    # Create train/val/test split
    splitter = Splitter(train_prop=0.95, val_prop=0.025, test_prop=None, length=len(supercluster_ids_unique))
    train, val, test = splitter.get_permutations()


    # np.testing.assert_array_equal(supercluster_ids_unique, np.unique(supercluster_ids))
    # print('Passed equal')
    # print(f"{supercluster_ids_unique.dtype=}, {supercluster_boundaries.dtype=}")
    # print(f"{supercluster_ids_unique=}")
    # print(f"{supercluster_boundaries=}")
    # print(f"{supercluster_ids_unique.nbytes=}")
    # print(f'{supercluster_boundaries.nbytes=}')
    # exit()

    # write_kwargs = {'compressor': compressor, 'overwrite': True, 'chunks': (2**15,)}

    # z_tokens = root.array('tokens', tokens, **write_kwargs)
    # z_tokens_cu_seqlens = root.array('tokens_cu_seqlens', tokens_cu_seqlens, **write_kwargs)
    # z_taxon_ids = root.array('taxon_ids', taxon_ids, **write_kwargs)
    # z_supercluster_ids_unique = root.array('supercluster_ids_unique', supercluster_ids_unique, **write_kwargs)
    # z_supercluster_boundaries = root.array('supercluster_boundaries', supercluster_boundaries, **write_kwargs)

    with H5File('protref90_clustered50.h5', 'w') as f:
        compressor = hdf5plugin.Blosc2(cname='zstd', clevel=3)
	
    	assert tokens.max() <= np.iinfo(np.uint8).max, "Data overflow in tokens"
    	assert tokens_cu_seqlens.max() <= np.iinfo(np.uint64).max, "Data overflow in tokens_cu_seqlens"
    	assert taxon_ids.max() <= np.iinfo(np.uint32).max, "Data overflow in taxon_ids"
    	assert supercluster_ids_unique.max() <= np.iinfo(np.uint64).max, "Data overflow in supercluster_ids_unique"
    	assert supercluster_boundaries.max() <= np.iinfo(np.uint64).max, "Data overflow in supercluster_boundaries"
    	assert train.max() <= np.iinfo(np.uint32).max, "Data overflow in train_split"
    	assert val.max() <= np.iinfo(np.uint32).max, "Data overflow in val_split"
    	assert test.max() <= np.iinfo(np.uint32).max, "Data overflow in test_split"

        with timer('writing tokens'):
            f.create_dataset('tokens', data=tokens, dtype=np.uint8, **compressor)
        f.create_dataset('tokens_cu_seqlens', data=tokens_cu_seqlens, dtype=np.uint64, **compressor)
        f.create_dataset('taxon_ids', data=taxon_ids, dtype=np.uint32, **compressor)
        f.create_dataset('supercluster_ids_unique', data=supercluster_ids_unique, dtype=np.uint64, **compressor)
        f.create_dataset('supercluster_boundaries', data=supercluster_boundaries, dtype=np.uint64, **compressor)
        f.create_dataset('train_split', data=train, dtype=np.uint32, **compressor)
        f.create_dataset('val_split', data=val, dtype=np.uint32, **compressor)
        f.create_dataset('test_split', data=test, dtype=np.uint32, **compressor)




class H5Dataset:
    def __init__(self, path = 'protref90_clustered50.h5'):
        # Keep the 
        # self.fs: WholeFileCacheFileSystem = fsspec.filesystem("filecache", target_protocol='s3',
        #                             cache_storage='./data_cache')
        # self.s3 = s3fs.S3FileSystem(cache_regions=True)
        # self.store = s3fs.S3Map(root='ai-residency-stanford-snap-uce/datasets', s3=self.s3, check=True, create=False)
        # self.store = self.fs.get_mapper(root='ai-residency-stanford-snap-uce/datasets', check=True)
        # self.store = zarr.N5Store('protref90_clustered50_zarr.n5')
        # self.cache = zarr.LRUStoreCache(self.store, max_size=None)  # This is in-memory cache
        # self.group = zarr.group(store=datasets, path=path_relto_datasets)
        # self.root = zarr.group(store=self.store)
        print('Loading superclusters')
        self.file = H5File(path, 'r')
        self.supercluster_ids = self.file['supercluster_ids_unique'][:]
        self.supercluster_boundaries = self.file['supercluster_boundaries']
        self.tokens_cu_seqlens = self.file['tokens_cu_seqlens']
        self.tokens = self.file['tokens']
        self.taxon_ids = self.file['taxon_ids']
        print(self.supercluster_ids.nbytes)
        print('Loaded superclusters')
    
    def __getitem__(self, item):
        if isinstance(item, int):
            supercluster_id = self.supercluster_ids[item]
            start_clust, end_clust = self.supercluster_boundaries[supercluster_id:supercluster_id+2]
            random_seq_idx = randrange(start_clust, end_clust)
            # random_seq_idx = randrange(start_clust, start_clust + 1)
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
    save_test()
    # crs = H5Dataset()
    # print('Init finished')
    # for i in trange(len(crs)):
    #     s = crs[i]
    # print('Loaded')
    # print(la[100:500])
