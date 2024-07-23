"""Fundamental column types to Dataset library"""
# pylint: disable=protected-access
from __future__ import annotations
from typing import Dict
import numpy as np
import pandas as pd
from loggez import loggez_logger as logger

ColumnType = str
# { users: {client_id: str, total_number_of_sessions: int}, sessions: {...}, ... }
DatasetDgTypes = Dict[str, Dict[str, ColumnType]]

VALID_COLUMN_TYPES = ["int", "float", "bool", "object", "str", "categorical", "vector",
                      "datetime64[ns]", "timedelta64[ns]"]

def column_type_to_dtype(column_type: ColumnType) -> type:
    """Converts a dataset type, represented as a string to a python dtype"""
    if column_type == "int":
        return int
    if column_type == "float":
        return float
    if column_type == "bool":
        return bool
    if column_type == "object":
        return object
    if column_type == "str":
        return str
    if column_type == "categorical":
        return pd.CategoricalDtype
    if column_type == "vector":
        return np.ndarray
    if column_type == "datetime64[ns]":
        return np.dtype("datetime64[ns]")
    if column_type == "timedelta64[ns]":
        return np.dtype("timedelta64[ns]")
    raise KeyError(f"Dataset type '{column_type}' not supported")

def _dtype_to_column_type(col_data: pd.Series, dtype: type) -> ColumnType:
    """Converts a regular dtype from a backend (i.e. pandas) to a dataet type, which is represented as string"""
    # This is first checked because it's not a numpy type, but a pandas type. All the other ones are numpy dtypes
    # used by pandas in their series.
    if isinstance(dtype, pd.CategoricalDtype):
        return "categorical"
    if isinstance(dtype, int) or np.issubdtype(dtype, np.integer):
        return "int"
    if isinstance(dtype, float) or np.issubdtype(dtype, np.floating):
        return "float"
    if isinstance(dtype, bool) or np.issubdtype(dtype, np.dtype("bool")):
        return "bool"
    if np.issubdtype(dtype, np.dtype("datetime64")):
        return "datetime64[ns]"
    if np.issubdtype(dtype, np.dtype("timedelta64")):
        return "timedelta64[ns]"
    if isinstance(dtype, object) or np.issubdtype(dtype, np.dtype("object")):
        if not isinstance(col_data.iloc[0], np.ndarray):
            return "object"
        if len(col_data) > 100_000: # TODO: add tests
            col_data = col_data.sample(n=100_000)
        return "object" if len(col_data.apply(len).unique()) > 1 else "vector"
    if isinstance(dtype, str) or np.issubdtype(dtype, np.dtype("str")):
        return "str"
    raise KeyError(f"Dtype '{dtype}' not supported")

def _check_col_data(col_data: pd.Series, col_data_type: ColumnType):
    """checks a single column given it's data type"""
    name = col_data.name
    if col_data_type == "vector":
        first_item = col_data.iloc[0]
        if not isinstance(first_item, np.ndarray):
            raise TypeError(f"Column '{name}' with data_type 'vector' has vectors stored as '{type(first_item)}'")
    if col_data_type == "categorical":
        if not isinstance(col_data.dtype, pd.CategoricalDtype):
            raise TypeError(f"Column '{name}' with data_type 'categorical' has dtype '{col_data.dtype}'")

def _auto_detect_column_types(dataset: "Dataset") -> DatasetDgTypes:
    logger.debug("Auto detecting data types from the dataset. It's recommended you provided this dict yourself.")
    res = {}
    for dg in dataset._data.keys():
        res[dg] = {}
        dg_data: pd.DataFrame = dataset._data[dg].reset_index()
        for col in dg_data:
            col_data = dg_data[col]
            res[dg][col] = _dtype_to_column_type(col_data, col_data.dtype)
    return res

def check_column_types(dataset: "Dataset", column_types: DatasetDgTypes) -> DatasetDgTypes:
    """Just checks the validity of the provided data types against the actual data in the dataset"""
    if column_types.keys() != dataset._data.keys():
        raise KeyError(f"Provided data types: {column_types.keys()}. Dataset: {dataset._data.keys()}")
    for dg in dataset._data.keys():
        for col in dataset._data[dg].columns:
            assert column_types[dg][col] in VALID_COLUMN_TYPES, f"{column_types[dg][col]} & {VALID_COLUMN_TYPES}"
            _check_col_data(dataset._data[dg][col], column_types[dg][col])
    return column_types

def build_column_types(dataset: "Dataset", column_types: DatasetDgTypes | None) -> DatasetDgTypes:
    """Returns a properly verified dictionary of dg => {col: data type} for all data groups"""
    if column_types is None:
        column_types = _auto_detect_column_types(dataset)

    return check_column_types(dataset, column_types)
