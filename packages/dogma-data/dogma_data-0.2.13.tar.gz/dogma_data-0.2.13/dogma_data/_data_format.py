import pickle
from pathlib import Path
from dogma_data import read_awkward
import blosc2
import h5py
import hdf5plugin
from dogma_data.utils import timer
import awkward as ak
import tables
import os
import zarr
from numcodecs import Blosc
import numcodecs
import zipfile
import xarray
import dask
from itertools import count

from utils import ceildiv

os.environ['BLOSC_NTHREADS'] = '64'
h5py_filters = hdf5plugin.Blosc2(clevel=1, cname='zstd', filters=hdf5plugin.Blosc2.SHUFFLE)

def save_dataset(arr: ak.Array):
    main_data = ak.to_buffers(arr)[2]['node2-data']
    f = h5py.File('test.h5', 'w')
    with timer('Creating dataset'):
        f.create_dataset('main_data', data=main_data, chunks=2**28, **h5py_filters)
    f.close()


def save_dataset_blosc2(arr: ak.Array):
    main_data = ak.to_buffers(arr)[2]['node2-data']
    with timer('Saving to blosc2'):
        blosc2.save_array(main_data, 'test.blosc2', chunksize=2**28)


def write_blosc2_files(arr: ak.Array, dir: Path) -> int:
    form, length, container = ak.to_buffers(ak.to_packed(arr))
    
    for k, v in container.items():
        n_out_bytes = blosc2.asarray(v, urlpath=str(dir / f'{k}.blosc2'), mode='w',
                                     cparams={'codec': blosc2.Codec.ZSTD, 'nthreads': 64},
                                     # dparams={'nthreads': 1},
                                     chunks=(2**24,))  # Chunksize and blocksize are different
    
    with open(dir / 'meta.pkl', 'wb') as f:
        pickle.dump({'form': form, 'length': length}, f)

    return n_out_bytes

def read_blosc2_files(dir: Path, nthreads=1) -> ak.Array:
    with open(dir / 'meta.pkl', 'rb') as f:
        meta = pickle.load(f)
    container = {}
    for file in dir.glob('*.blosc2'):
        k = file.stem
        container[k] = blosc2.open(str(file), dparams={'nthreads': nthreads})
    return ak.from_buffers(meta['form'], meta['length'], container)


class LazyBlosc:
    def __init__(self, dir: Path):
        self.dir = dir
        with open(dir / 'meta.pkl', 'rb') as f:
            self.meta = pickle.load(f)
    
    def __len__(self):
        return self.meta['length']
    
    def __getindex__(self, index):
        container = {}
        for file in dir.glob('*.blosc2'):
            k = file.stem
            container[k] = blosc2.open(str(file), dparams={'nthreads': 1})
        return ak.from_buffers(self.meta['form'], self.meta['length'], container)

def lazy_read_blosc2_files(dir: Path) -> ak.Array:
    return LazyBlosc(dir)


def write_blosc2_sharded(arr: ak.Array, root_dir: Path, shard_size_bytes: int = 2**28):
    shard_seqs = ceildiv(shard_size_bytes * len(arr), arr.nbytes)
    total_seqs = len(arr)
    total_bytes = arr.nbytes

    shards = []
    for i, start in enumerate(range(0, len(arr), shard_seqs)):
        out_path = root_dir / f'shard_{i}'
        shard_arr: ak.Array = ak.to_packed(arr[i:i+shard_seqs])
        compressed_bytes = write_blosc2_files(shard_arr, out_path)
        shards.append({
            'path': out_path.relative_to(root_dir),
            'compressed_bytes': compressed_bytes,
            'length': len(shard_arr),
        })
    


if __name__ == '__main__':
    with timer('Reading data'):
        arr = read_awkward('canonical_data/ensembl_rna_aa_taxon.blosc.pkl')
    with timer('Saving to h5'):
        # save_dataset(arr)
        save_dataset_blosc2(arr)