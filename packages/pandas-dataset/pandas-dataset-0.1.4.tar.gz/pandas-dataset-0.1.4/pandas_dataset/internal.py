"""Various checks done on the dataset to ensure its consistency. Called explicitly only for efficiency purposes"""
# pylint: disable=protected-access, consider-iterating-dictionary
from __future__ import annotations
from copy import copy
from collections import Counter
import pandas as pd

from loggez import loggez_logger as logger

from .utils import flatten_list

def _check_one_path(dataset: "Dataset", path):
    # Do a .unique() on each join key and check that data frames are perfectly inner joinable
    for i in range(len(path) - 1):
        parent: pd.DataFrame = dataset[path[i]]
        child: pd.DataFrame = dataset[path[i + 1]]
        index_col = parent.index
        if index_col.name not in child.columns:
            raise KeyError(f"Join key '{index_col.name}' not in child data frame: '{path[i + 1]}' (path: '{path}')")
        unique_join_key = child[index_col.name].unique()
        intersection = index_col.intersection(unique_join_key)
        union = parent.index.union(unique_join_key)
        diff = list(union.difference(intersection))
        if len(intersection) != len(union):
            raise ValueError(f"Child data frame '{path[i + 1]}' does not inner join with parent '{path[i]}'."
                             f"Differences on join key '{index_col.name}': '{diff}'")

def check_data_groups_consistency(dataset: "Dataset"):
    """Check that all nested data groups are perfectly inner-joinable on the join keys. Will throw an error if true"""
    logger.debug("Checking data groups consistency")
    for path in dataset.data_groups:
        _check_one_path(dataset, path)

def check_nans(dataset: "Dataset"):
    """Checks if the dataset has nans. Will throw an error if true"""
    logger.debug("Checking for nans inside the dataset")
    for tb in dataset.tables:
        nans = dataset[tb].isna().any() if len(dataset[tb]) > 0 else []
        if sum(nans):
            raise ValueError(f"NaNs or Infinities were found in the table '{tb}': {nans}")

def build_data(data: dict[str, pd.Series | pd.DataFrame]) -> dict[str, pd.DataFrame]:
    """Returns a proper dictionary of dataframes. Does basic checks as well."""
    # Convert series to dataframes if the case
    df_data: dict[str, pd.DataFrame] = {}
    all_cols = []
    pks = []
    for dg, v in data.items():
        if isinstance(v, pd.Series):
            assert v.name, f"The value of data group '{dg}' is a `pd.Series` without name."
            data[dg] = v.to_frame()

        if not isinstance(data[dg], pd.DataFrame):
            raise ValueError(f"The value of data group '{dg}' must be pd.Series or pd.Dataframe. Got: {type(v)}")

        if data[dg].index.name is None:
            logger.warning(f"Data group '{dg}' has empty index name. Defaulting to '{dg}'")
            data[dg].index.name = dg

        df_data[dg] = data[dg]
        all_cols.extend(df_data[dg].columns.tolist())
        pks.append(df_data[dg].index.name)

    all_cols_except_pks = [col for col in all_cols if col not in pks]
    duplicates = {k: v for k, v in Counter(all_cols_except_pks).items() if v > 1}
    if len(duplicates) > 0:
        raise ValueError(f"There are duplicate column names across tables: {duplicates}")

    return df_data

def build_data_groups(dataset: "Dataset") -> list[list[str]]:
    """
    Builds the nested data groups for all top-levels.
    Example: for users>sessions and products, we will get [[users, sessions], [products]]
    Cycles are ot allowed. Children with 2 parents are not allowed. One parent with 2 children are not allowed.
     - [tb1, tb2, tb3, tb1] -> wrong (rule 1)
     - tb1 => [tb2, tb3] -> wrong (rule 2)
     - [tb1, tb2] => tb3 -> wrong (rule 3)
     - [tb1, tb2, tb3] -> ok
    """
    pks = {tb: dataset._data[tb].index.name for tb in dataset._data}
    rels = {}
    tables = list(dataset._data.keys())
    for tb in tables:
        cols = set(dataset._data[tb].columns)
        rels[tb] = []
        for other_tb in tables:
            if pks[other_tb] in cols:
                rels[tb].append(other_tb)

    top_levels = [tb for tb in tables if len(rels[tb]) == 0]
    if len(top_levels) == 0:
        raise ValueError(f"No top levels found: {rels}. Possible cycles.")
    rels_orig = copy(rels)

    result = []
    for top_level in top_levels:
        this_dg = [top_level]
        current = top_level
        while True:
            del rels[current]
            found_one = False
            for tb in rels.keys():
                if current not in rels[tb]:
                    continue
                rels[tb].remove(current)
                # if we find one table that has only and only the primary key of current table, we continue this dg
                if len(rels[tb]) == 0:
                    if found_one:
                        raise ValueError(f"There may be cycles in your data tables: {rels_orig}")
                    this_dg.append(tb)
                    found_one = True
            if found_one is False:
                break
            current = this_dg[-1]
        result.append(this_dg)

    if len(flatten_list(result)) != len(rels_orig):
        raise ValueError(f"Not all tables were put into data groups. There may be cycles: {rels_orig}")

    result = sorted(result, key=lambda dg: dg[0])
    return result
