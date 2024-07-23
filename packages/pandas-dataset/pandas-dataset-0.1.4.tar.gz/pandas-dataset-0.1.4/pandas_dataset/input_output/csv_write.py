"""Writes a dataset to a (Typed) CSV file"""
from pathlib import Path
import json
import pandas as pd
import numpy as np
from loggez import loggez_logger as logger

def _arr_to_tuple(x: np.ndarray) -> tuple:
    """converts (nested) np arrays to nested tuples"""
    if len(x) == 0:
        return ()
    if isinstance(x[0], (np.ndarray, list)):
        return tuple(_arr_to_tuple(y) for y in x)
    return tuple(x)

def csv_write(dataset: "Dataset", path: Path):
    """Writes a typed csv file to a path"""
    assert not path.is_file(), f"Path must be a directory. Got '{path}'."
    path.mkdir(exist_ok=True, parents=True)
    logger.info(f"Writing {dataset} as CSV files. Path: '{path}'.")

    for dg in dataset.tables:
        output_path = path / f"{dg}.csv"
        df: pd.DataFrame = dataset[dg]
        for col in df.columns:
            # we have to convert vector types from np arrays into tuples so they are properly stored as CSV
            col_data = df[col]
            if dataset.column_types[dg][col] == "vector":
                df = df.drop(columns=[col])
                df[col] = col_data.apply(tuple)
            if dataset.column_types[dg][col] == "object":
                if isinstance(col_data.iloc[0], np.ndarray):
                    df = df.drop(columns=[col])
                    df[col] = col_data.apply(_arr_to_tuple)
        df.to_csv(output_path, index=True)

    with open(f"{path}/types.json", "w", encoding="utf8") as f:
        f.write(json.dumps(dataset.column_types, indent=2))
