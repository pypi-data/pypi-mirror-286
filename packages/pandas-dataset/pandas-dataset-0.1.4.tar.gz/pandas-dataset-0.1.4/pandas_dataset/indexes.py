"""Indexes internal module to compute the indexes of a dataset"""
from __future__ import annotations
import pandas as pd
import numpy as np

def compute_indexes(data: "Dataset") -> dict[str, list]:
    """
    Computes a nested lists of indexes that helps to locate the data throughout a path:
    indexes from the `k`-th list help to locate the top node data points in the dataframe associated
    to the `k`-th node of the path.
    All the lists have the same length, equal to the length of the top node dataframe.

    Example:
        If the path is `users->sessions`, the `users` list contains just the row indexes oif the `users` dataframe
        (top node always has unique data points), and the `session` list contains the indexes from the `sessions`
        dataframe that correspond to users in the `users` dataframe.
        Thus, for each user in the top dataframe we know exactly where to find its sessions in the `sessions`
        dataframe.

    Returns a dict whose keys are the nodes in `path` and whose values are the correspondingly nested lists of
    indexes.
    """
    res: dict[str, list[list[int]]] = {}
    for dg in data.data_groups:
        # we start with the top-level data group. Since it is unique, it will a simple mapping: [ [0], [1], .., [n] ]
        assert len(pd.unique(data[dg[0]].index)) == len(data[dg[0]]), f"Index of data group '{dg[0]}' is not unique"
        res[dg[0]] = [ [i] for i in range(len(data[dg[0]])) ]

        for i in range(len(dg) - 1):
            parent: pd.DataFrame = data[dg[i]]
            child: pd.DataFrame = data[dg[i + 1]]
            assert len(pd.unique(child.index)) == len(child), f"Index of data group '{dg[i+1]}' is not unique"
            # Example: groupby dg='sessions' by 'Client ID', or dg='hits' by 'Session ID'
            indices: dict[str, np.ndarray] = child.groupby(parent.index.name).indices
            # turn the {index1: array([ix1]), index2: array([ix2])} into [ [ix1], [ix2] ]
            res[f"{dg[i]}-{dg[i+1]}"] = [x.tolist() for x in indices.values()]
    return res
