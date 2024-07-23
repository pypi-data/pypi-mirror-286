"""Statistics for the given dataset. Only applies for numerical columns, plus vetors and categoricals"""
from __future__ import annotations

import numpy as np
import pandas as pd

from loggez import loggez_logger as logger

from .column_types import ColumnType

def compute_stats(dataset: "Dataset") -> dict[str, dict[str, np.ndarray]]:
    """computes the mins/maxs of all columns of all data groups and returns them as a dict"""
    res = {}
    for dg in dataset.keys():
        res[dg] = {}
        for col in dataset[dg].columns:
            res[dg][col] = _compute_col_stats(dataset[dg][col], dataset.column_types[dg][col])
    return res

def _compute_col_stats(col_data: pd.Series, col_data_type: ColumnType) -> np.ndarray:
    if col_data_type in ("object", "str", "datetime64[ns]", "timedelta64[ns]"):
        return None

    if col_data_type in ("float", "int"):
        return _numeric_col_stats(col_data, col_data_type)

    if col_data_type == "categorical":
        cats = col_data.dtype.categories
        return np.array([[0] * len(cats), [1] * len(cats)])

    if col_data_type == "bool":
        return np.array([0, 1])

    if col_data_type == "vector":
        n_cols = len(col_data.iloc[0])
        return np.array([[0] * n_cols, [1] * n_cols])

    raise TypeError(f"Unknown type reached. Column: '{col_data.name}'. Type: {col_data_type}")

def _numeric_col_stats(col_data: pd.Series, col_data_type: ColumnType) -> np.ndarray:
    assert col_data_type in ("float", "int")
    # Find the best min-max range from right to left. We're trying [5% - 95%] first, if it doesn't work, we'll try
    # [4% - 95%], then [4% - 96%], until [0.1% - 99.9%]. We never try real min/max as this could have outliers.
    percentiles_left = [0.1, 1, 2, 3, 4, 5]
    percentiles_right = [95, 96, 97, 98, 99, 99.9]
    potentials = np.percentile(col_data, [percentiles_left, percentiles_right])
    potential_min, potential_max = potentials
    if np.fabs(potential_min[0] - potential_max[-1]) < 1e-5:
        logger.warning(f"Column {col_data.name} has only one value: {potential_min[0]}.")
        return np.array([0, 1])

    i = len(potential_min) - 1 # start from right
    j = 0 # start from left
    k = 0 # odd/even counter
    while True:
        if i < 0 or j >= len(potential_min):
            break
        current_min = potential_min[i]
        current_max = potential_max[j]
        current_diff = np.fabs(current_min - current_max)
        # If we found a pair that has a value that is not identical (i.e. 5% percentile value == 95% percentile)
        if current_diff != 0:
            logger.debug(f"Column: '{col_data.name}. Min-max pair: [{percentiles_left[i]}% - {percentiles_right[j]}%]"
                         f" Values: {current_min:.2f} - {current_max:.2f}.")
            return np.array([current_min, current_max])
        k += 1
        i -= k % 2  # update only on odd iterations
        j += 1 - (k % 2)  # update only on even iterations

    raise ValueError(f"Could not compute a valid min-max for column '{col_data.name}'. "
                     f" Percentiles: {potential_min} and {potential_max}")
