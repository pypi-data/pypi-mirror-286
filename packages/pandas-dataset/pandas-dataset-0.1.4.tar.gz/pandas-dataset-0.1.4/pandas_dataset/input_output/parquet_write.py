"""Writes a dataset to a parquet file"""
from pathlib import Path
import pandas as pd
import numpy as np

from loggez import loggez_logger as logger

def parquet_write(dataset: "Dataset", path: Path):
    """Writes a parquet file to a path"""
    assert not path.is_file(), f"Path must be a directory. Got '{path}'."
    path.mkdir(exist_ok=True, parents=True)
    logger.info(f"Writing {dataset} as Parquet files. Path: '{path}'.")

    for dg in dataset.tables:
        output_path = path / f"{dg}.parquet"
        df: pd.DataFrame = dataset[dg]
        for col in df.columns:
            col_data = df[col]
            # convert to float32, as we have defined a rule in parquet_read to look only for float arrays
            if dataset.column_types[dg][col] == "vector":
                df = df.drop(columns=[col])
                df[col] = col_data.apply(lambda arr: arr.astype(np.float32))
            # list of lists with dtype object cannot be exported. If we shallow convert the outer array to list it's ok
            if dataset.column_types[dg][col] == "object" and isinstance(col_data.iloc[0], np.ndarray):
                df = df.drop(columns=[col])
                df[col] = col_data.apply(list)
        # reset index, because parquet reader is a bit weird and keeps the index as-is. It's simpler for now.
        df.to_parquet(output_path)
