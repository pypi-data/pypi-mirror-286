"""Reads a (Typed) CSV dataset from a directory"""
# pylint: disable=consider-iterating-dictionary
from __future__ import annotations
from typing import Callable
from pathlib import Path
import json
import ast
import numpy as np
import pandas as pd
from loggez import loggez_logger as logger
from ..column_types import VALID_COLUMN_TYPES, ColumnType, column_type_to_dtype

def _build_converters(dg_column_types: dict[str, dict[str, ColumnType]],
                      object_converters: dict[str, Callable]) -> dict[str, dict[str, Callable]]:
    """Special types that must be explicitly converted after reading them with pd.read_csv"""
    converters = {}
    for tb in dg_column_types.keys():
        converters[tb] = {}
        for k, v in dg_column_types[tb].items():
            if v == "vector":
                converters[tb][k] = lambda x: np.array(ast.literal_eval(x), dtype=np.float32)
            if v == "datetime64[ns]":
                converters[tb][k] = pd.to_datetime
            if v == "object":
                if k not in object_converters:
                    logger.warning(f"Column '{k}' is object and has no object converter callback. Reading as string.")
                    continue
                converters[tb][k] = object_converters[k]
    return converters

def _read_column_types(path: Path, columns: dict[str, list[str]]) -> dict[str, dict[str, ColumnType]]:
    """Reads dataset types from types.json expected in the same dir as the csv files"""
    col_types_file = path / "types.json"
    with open(col_types_file, "r", encoding="utf8") as json_file:
        raw_dtypes: dict[str, dict[str, str]] = json.load(json_file)

    col_types_file = {}
    for tb, tb_columns in columns.items():
        col_types_file[tb] = {}
        for column in tb_columns:
            assert column in raw_dtypes[tb], f"'{tb}/{column}' not in {raw_dtypes[tb]} (path: '{col_types_file}')"
            column_dtype = raw_dtypes[tb][column]
            assert column_dtype in VALID_COLUMN_TYPES, f"Got '{column_dtype}'. Valid: {VALID_COLUMN_TYPES}"
            col_types_file[tb][column] = column_dtype

    return col_types_file

def csv_peek(path: Path, tables_pk: dict[str, str]) -> dict[str, dict[str, str]]:
    """Reads just the first row of all csv files given a path. Then, reads the types.json file and returns it."""
    cols = {}
    for tb in tables_pk.keys():
        cols[tb] = pd.read_csv(f"{path}/{tb}.csv", nrows=0).columns.tolist()
    res = _read_column_types(path, cols)
    return res

def csv_read(path: Path, tables_pk: dict[str, str], columns: dict[str, list[str]],
             object_converters: dict[str, Callable] | None = None) -> tuple[dict, dict]:
    """Reads data from a path of CSVs, given a list of columns and a list of data-groups plus their primary keys"""
    assert path.is_dir(), f"Path must be a directory. Got '{path}'."
    assert isinstance(columns, dict), f"Expected dict, got {columns}"

    object_converters = object_converters if object_converters is not None else {}
    column_types = _read_column_types(path, columns)
    converters = _build_converters(column_types, object_converters)
    logger.info(f"Reading Dataset from CSV files. Path: '{path}'. Data groups: {list(tables_pk)}")

    data = {}
    for dg, pk in tables_pk.items():
        file_name = path / f"{dg}.csv"
        dtypes = {k: column_type_to_dtype(v) for k, v in column_types[dg].items() if k not in converters[dg]}
        dtypes = {k: v if v != pd.CategoricalDtype else "category" for k, v in dtypes.items()}
        # This is here so we can read w/o explicitly putting pks in the columns. They are deduced by being pks.
        logger.debug(f"Reading the CSV file: '{file_name}' ({len(columns[dg])} columns)")
        read_data = pd.read_csv(file_name, usecols=columns[dg], dtype=dtypes).set_index(pk)

        # force float32 so we don't get weird float64/float32 differences during computation
        float64_cols = read_data.select_dtypes(include="float64").columns
        read_data = read_data.astype({col_name: np.float32 for col_name in float64_cols})

        for col, converter_fn in converters[dg].items():
            logger.debug(f"Converting '{col}' with dtype '{column_types[dg][col]}'")
            if column_types[dg][col] == "datetime64[ns]":
                read_data[col] = converter_fn(read_data[col])
            else:
                read_data[col] = read_data[col].apply(converter_fn)

        data[dg] = read_data
    return data, column_types
