import blosc2
import numcodecs

enum_dict = {
    'blosclz': blosc2.Codec.BLOSCLZ,
    'lz4': blosc2.Codec.LZ4,
    'lz4hc': blosc2.Codec.LZ4HC,
    'zlib': blosc2.Codec.ZLIB,
    'zstd': blosc2.Codec.ZSTD,
    'NDLZ': blosc2.Codec.NDLZ,
    'ZFP_ACC': blosc2.Codec.ZFP_ACC,
    'ZFP_PREC': blosc2.Codec.ZFP_PREC,
    'ZFP_RATE': blosc2.Codec.ZFP_RATE,
}


class Blosc2(numcodecs.abc.Codec):

    codec_id = 'blosc2'

    def __init__(self, cname='zstd', clevel=5, shuffle=1, blocksize=0):
        self.cname = cname
        self.clevel = clevel
        self.shuffle = shuffle
        self.blocksize = blocksize
    
    def encode(self, data):
        return blosc2.compress2(data, codec=enum_dict[self.cname], clevel=self.clevel, filter=blosc2.Filter(self.shuffle), blocksize=self.blocksize)
    
    def decode(self, data):
        return blosc2.decompress(data)
    
numcodecs.register_codec(Blosc2, 'blosc2')