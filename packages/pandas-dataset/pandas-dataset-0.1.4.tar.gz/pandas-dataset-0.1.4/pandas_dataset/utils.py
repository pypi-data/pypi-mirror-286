"""utils for pandas-dataset"""
from __future__ import annotations
from pathlib import Path
from typing import Iterable, T, Union, Any
import numpy as np

StrOrPath = Union[str, Path]

def get_project_root() -> Path:
    """gets the root of the project for tests"""
    return Path(__file__).absolute().parents[1]

def flatten_list(x: Iterable[T]) -> list[T]:
    """Flattens a list of lists. Also flattens np arrays of object type, tuples and sets."""
    if x is None or len(x) == 0:
        return []
    res = []
    for item in x:
        if isinstance(item, (tuple, list, set)) or (isinstance(item, np.ndarray) and item.dtype == object):
            res.extend(flatten_list(item))
        else:
            res.append(item)
    return res

def parsed_str_type(item: Any) -> str:
    """Given an object with a type of the format: <class 'A.B.C.D'>, parse it and return 'A.B.C.D'"""
    return str(type(item)).rsplit(".", maxsplit=1)[-1][0:-2]
