
import torch
from torch.utils.data import IterableDataset, DataLoader, get_worker_info
import numpy as np

from multiprocessing.managers import DictProxy
from torch.multiprocessing import Manager
from multiprocessing.shared_memory import SharedMemory
from multiprocessing import shared_memory
from torch.multiprocessing.spawn import spawn
import awkward as ak


class SharedDictDataset(IterableDataset):
    def __init__(self, d):
        self.d = d

    def __iter__(self):
        worker_info = get_worker_info()
        print(id(self.d))
        for i in range(10_000_000):
            yield self.d.get(i)


def main(i):
    arr = ak.Array({'tokens': np.empty(63_957_703_870)})
    dataloader = DataLoader(dataset, num_workers=4)
    for item in dataloader:
        print(item)
    del m


if __name__ == '__main__':
    main(0)
