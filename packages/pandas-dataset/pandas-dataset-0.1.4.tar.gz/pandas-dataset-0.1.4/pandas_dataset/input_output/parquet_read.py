"""Reads a parquet dataset from a directory"""
# pylint: disable=c-extension-no-member
from __future__ import annotations
from pathlib import Path
import numpy as np
import pandas as pd
import pyarrow as pa
from pyarrow import parquet as pq
from loggez import loggez_logger as logger
from ..column_types import ColumnType

def _peek_one_file_only(path) -> pa.Schema:
    """
    Parquet exports can also be directories containing multiple singular parquet files.
    pq.read_schema wants only these files, so we provide it the first file inside that directory
    NOTE: this doesn't protect you from invalid parquet files (having different headers) inside the directory
    """
    try:
        schema = pq.read_schema(path)
    except OSError:
        all_files = list(path.iterdir())
        assert len(all_files) > 0, f"Found dir at '{path}' but with no parquet files inside"
        pq_files = [x for x in all_files if x.suffix == ".parquet" and x.is_file()]
        assert len(pq_files) == len(all_files), f"Found other type of files at '{path}' except parquet: {all_files}"
        return _peek_one_file_only(pq_files[0])
    return schema

def _pq_to_dataset_type(pq_type) -> ColumnType:
    """Maps parquet types to Dataset types"""
    if pq_type == "string":
        return "str"
    if pq_type in ("float", "double"):
        return "float"
    if pq_type == "bool":
        return "bool"
    if pq_type in ("int64", "int32"):
        return "int"
    if isinstance(pq_type, pa.lib.ListType):
        # Both vectors and objects are stored as lists, so we need to look at the inner type to differnetiate
        if pq_type.value_type == "float":
            return "vector"
        return "object"
    if isinstance(pq_type, pa.lib.dictionaryType):
        return "categorical"
    if isinstance(pq_type, pa.lib.TimestampType):
        assert pq_type.to_pandas_dtype() == np.dtype("datetime64[ns]"), f"Unknown datetime format: {pq_type}"
        return "datetime64[ns]"
    if isinstance(pq_type, pa.lib.DurationType):
        assert pq_type.unit == "ns", f"Unknown timedelta format: {pq_type}"
        return "timedelta64[ns]"
    if isinstance(pq_type, pa.lib.DataType):
        if pq_type == "date32[day]":
            assert pq_type.to_pandas_dtype() == np.dtype("datetime64[ns]"), f"Unknown datetime format: {pq_type}"
            return "datetime64[ns]"

    raise TypeError(f"Unknown parquet type: {pq_type} found in the dataset.")

def parquet_peek(path: Path, tables_pk: dict[str, str]) -> dict[str, dict[str, str]]:
    """Reads just the first row of all pq files given a path. Then, reads the types.json file and returns it."""
    column_types = {}
    for tb, pk in tables_pk.items():
        column_types[tb] = {}
        schema = _peek_one_file_only(path / f"{tb}.parquet")
        assert pk in schema.names, f"Primary key '{tb}/{pk}' not found in the parquet file!"
        for col, pq_type in zip(schema.names, schema.types):
            column_type = _pq_to_dataset_type(pq_type)
            column_types[tb][col] = column_type
    return column_types

def parquet_read(path: Path, tables_pk: dict[str, str], columns: dict[str, list[str]]) -> tuple[dict, dict]:
    """Reads data from a path of parquets, given a list of columns and a list of data-groups plus their primary keys"""
    assert path.is_dir(), f"Path must be a directory. Got '{path}'."
    assert isinstance(columns, dict), f"Expected dict, got {columns}"

    logger.info(f"Reading Dataset from parquet files. Path: '{path}'. Data groups: {list(tables_pk)}")
    header = parquet_peek(path, tables_pk)
    data = {}
    dataset_types = {}
    for tb, pk in tables_pk.items():
        file_name = path / f"{tb}.parquet"
        # parquet data type conversion is built-in. No manual needed, like in csv case.
        logger.debug(f"Reading the parquet file: '{file_name}' ({len(columns[tb])} columns)")
        assert columns[tb] is None or isinstance(columns[tb], list), f"Expected list or None, got {columns[tb]}"
        data[tb] = pd.read_parquet(file_name, columns=columns[tb])
        data[tb] = data[tb].set_index(pk) if data[tb].index.name != pk else data[tb]
        dataset_types[tb] = {k: v for k, v in header[tb].items() if k in columns[tb]}
    return data, dataset_types
