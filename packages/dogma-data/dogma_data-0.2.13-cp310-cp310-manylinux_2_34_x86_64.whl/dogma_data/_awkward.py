from typing import Callable, TypeVar, Tuple

import awkward as ak
import numpy as np
from numpy.typing import NDArray, NBitBase, DTypeLike

_T = TypeVar('_T', bound=np.generic)
_U = TypeVar('_U', bound=np.generic)

def map_awkward(arr: ak.Array,
                field_fn: Callable[..., Tuple[NDArray[_T], NDArray[np.int64]]],
):
    """
    """
    new_fields = {}
    for field_name in arr.fields:
        field = arr[field_name]
        if isinstance(field.layout, ak.contents.listoffsetarray.ListOffsetArray):
            offsets = field.layout.offsets
            content = field.layout.content.data
            new_field = ak.contents.ListOffsetArray(*field_fn(offsets, content))
