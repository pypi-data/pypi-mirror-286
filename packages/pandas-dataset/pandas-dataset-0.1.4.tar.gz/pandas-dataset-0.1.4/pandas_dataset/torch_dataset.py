"""
TorchDataset -- wrapper on top of PandasDataset for nested structures data
TODO: can we make this optional and only use pandas and add this to `pip install pandas-dataset[torch]` ?
"""
from __future__ import annotations
from loggez import loggez_logger as logger
from natsort import natsorted
import numpy as np
import pandas as pd

import torch as tr
from torch.utils.data import Dataset

from .dataset import Dataset as PandasDataset
from .utils import parsed_str_type

class TorchDataset(Dataset):
    """
    Torch dataset -- wrapper for using PandasDataset in torch workflows for ML training/inference.
    Properly expands columns based on their data types.
    """
    def __init__(self, base_dataset: PandasDataset, features: dict[str, list[str]] = None):
        assert len(dgs := base_dataset.data_groups) == 1, f"Only 1 supported for now, got {dgs} ({len(dgs)})"
        assert 0 < len(dgs[0]) < 3, f"Only 1 or 2 tables in the singular data group supported now: {dgs[0]}"
        self.base_dataset = base_dataset
        self._tables_pk = {k: self.base_dataset[k].index.name for k in base_dataset.keys()}
        self._data: PandasDataset = None

        self.features = self._build_features(features)
        self.tables = list(self.features.keys())
        self.unexpanded_to_ixs: dict[str, tuple[int, int]] = self._build_unexpanded_to_ixs()

        self._indexes = None
        self._len = len(self.indexes[dgs[0][0]])

    # Public methods and properties

    @property
    def data(self) -> PandasDataset:
        """get the data -- can we reuse this from PandasDataset?"""
        if self._data is None:
            res = {}
            for table, pk in self._tables_pk.items():
                jks = self.base_dataset.join_keys[table]
                columns = list(set([*self.features[table], pk, *jks])) # just making sure jks and pks are there (TODO)
                res[table] = self.base_dataset[table].reset_index()[columns]
                sorted_cols = natsorted(res[table].columns)
                res[table] = res[table][sorted_cols].sort_values([*jks, pk]).set_index(pk)
            self._data = res
        return self._data

    @property
    def columns(self) -> dict[str, list[str]]:
        """get the expanded columns"""
        res = {}
        for tb in self.base_dataset.tables:
            res[tb] = []
            for col, ixs in self.unexpanded_to_ixs[tb].items():
                # if vector or categorical
                if self._data[tb].dtypes[col] == object:
                    if isinstance(self._data[tb][col].iloc[0], np.ndarray):
                        res[tb].extend([f"{col}_{ix}" for ix in range(ixs[1] - ixs[0])])
                    else:
                        raise NotImplementedError(f"Unknown dtype {self._data[tb].dtypes[col]} for column {col}")
                elif self._data[tb].dtypes[col] == "category":
                    res[tb].extend(f"{col}_{cat}" for cat in self._data[tb][col].cat.categories)
                else:
                    assert ixs[1] - ixs[0] == 1, f"Non vector/categorical column '{col}' has {ixs} indexes"
                    res[tb].append(col)
        return res

    @property
    def indexes(self) -> dict[str, list[int]]:
        """indexes -- can we reuse this from PandasDataset?"""
        if self._indexes is None:
            self._indexes = self._compute_indexes()
        return self._indexes

    @property
    def data_shape(self) -> dict[str, tuple[int, ...]]:
        """Data shape for the expanded columns"""
        res = {tb: (len(self.data[tb]), len(self.columns[tb])) for tb in self.tables}
        return res

    def to_batched_item(self, batch: list[dict]) -> dict:
        """Converts a list of data items to a batch."""
        tbs = self.base_dataset.data_groups[0]
        tb0_data = tr.stack([y[tbs[0]] for y in batch]).float()
        res = {tbs[0]: tb0_data}
        if len(tbs) == 2:
            res[tbs[1]] = [y[tbs[1]].float() for y in batch]
        return res

    # Private methods

    def _build_features(self, features: dict[str, list[str]] | None) -> dict[str, list[str]]:
        if features is not None:
            return features
        features = {tb: [] for tb in self.base_dataset.tables}
        for tb in self.base_dataset.tables:
            non_obj_cols = [col for col, col_type in self.base_dataset.column_types[tb].items() if col_type != "object"]
            obj_cols = [col for col, col_type in self.base_dataset.column_types[tb].items() if col_type == "object"]
            features[tb] = non_obj_cols
            if len(obj_cols) > 0:
                logger.warning(f"Table: '{tb}'. Skipped {len(obj_cols)} object columns: [{', '.join(obj_cols)}].")
        logger.debug(f"No explicit features provided. Using all found: { {k : len(v) for k, v in features.items() }}.")
        return features

    def _get_top_level(self, index: int) -> tr.Tensor:
        """Get top level for this torch pandas dataframe. TODO: generic n level getter"""
        tb = self.base_dataset.data_groups[0][0]
        index = self.indexes[tb][index]
        assert len(index) == 1, f"Top level has either no or >2 indexes: {len(index)}"
        top_level_unexpanded = self.data[tb].iloc[index[0]: index[0] + 1]
        top_level_data = tr.from_numpy(self._expand_columns(top_level_unexpanded, tb)[0])
        return top_level_data

    def _get_second_level(self, index: int) -> tr.Tensor:
        """Get second level for this torch pandas dataframe. TODO: generic n level getter"""
        tb0, tb1 = self.base_dataset.data_groups[0][0:2]
        second_level_index = self.indexes[f"{tb0}-{tb1}"][index]
        flat_index = np.array(second_level_index).flatten()
        second_level_unexpanded = self.data[tb1].iloc[flat_index]
        second_level_data = tr.from_numpy(self._expand_columns(second_level_unexpanded, tb1))
        return second_level_data

    def _build_unexpanded_to_ixs(self) -> dict[str, tuple[int, int]]:
        res = {}
        pks = [self.data[tb].index.name for tb in self.tables]
        for tb in self.tables:
            rows_data = self.data[tb].iloc[0:1]
            cols_ordered = natsorted(rows_data.columns)
            n_expanded = 0
            unexpanded_to_ixs = {}
            for col in cols_ordered:
                if col in pks:
                    continue
                if rows_data.dtypes[col] == "category":
                    unexpanded_to_ixs[col] = (n_expanded, n_expanded + len(rows_data[col].cat.categories))
                    n_expanded += len(rows_data[col].cat.categories)
                elif rows_data.dtypes[col] in ("int64", "float64", "int32", "float32", "bool", "datetime64[ns]",
                                               "datetime64[us]"):
                    unexpanded_to_ixs[col] = (n_expanded, n_expanded + 1)
                    n_expanded += 1
                elif rows_data.dtypes[col] == "object" and isinstance(rows_data[col].iloc[0], np.ndarray):
                    unexpanded_to_ixs[col] = (n_expanded, n_expanded + len(rows_data[col].iloc[0]))
                    n_expanded += len(rows_data[col].iloc[0])
                else:
                    raise NotImplementedError(f"Column '{col}' has type: {rows_data.dtypes[col]}")
            res[tb] = unexpanded_to_ixs
        return res

    def _expand_columns(self, rows_data: pd.Series, tb: str) -> np.ndarray:
        """Expand one row of the dataframe"s columns based on the type of features they are"""
        # Table has no features to expand. Returning empty array
        if len(self.unexpanded_to_ixs[tb]) == 0:
            return np.empty((len(rows_data), 0), dtype=np.float32)

        n_expanded = self.unexpanded_to_ixs[tb][list(self.unexpanded_to_ixs[tb])[-1]][-1]
        res = np.zeros((len(rows_data), n_expanded), dtype=np.float32)
        for col, ixs in self.unexpanded_to_ixs[tb].items():
            if rows_data.dtypes[col] == "category":
                res[:, ixs[0]: ixs[1]] = pd.get_dummies(rows_data[col]).values
            elif rows_data.dtypes[col] in ("int64", "float64", "int32", "float32", "bool", "datetime64[ns]",
                                           "datetime64[us]"):
                res[:, ixs[0]] = rows_data[col].values
            elif rows_data.dtypes[col] == "object":
                res[:, ixs[0]: ixs[1]] = np.stack(rows_data[col].values)
            else:
                raise NotImplementedError(f"Unknown dtype {rows_data.dtypes[col]} for column {col}")
        return res

    def _compute_indexes(self) -> dict[str, list]:
        dgs = self.base_dataset.data_groups
        res = {}
        for dg in dgs:
            # we start with the top-level data group. It is unique, it will a simple mapping: [ [0], [1], .., [n] ]
            assert len(pd.unique(self.data[dg[0]].index)) == len(self.data[dg[0]]), f"Index must be unique: {dg[0]}"
            res[dg[0]] = [[i] for i in range(len(self.data[dg[0]]))]

            for i in range(len(dg) - 1):
                parent: pd.DataFrame = self.data[dg[i]]
                child: pd.DataFrame = self.data[dg[i + 1]]
                assert len(pd.unique(child.index)) == len(child), f"Index of data group '{dg[i+1]}' is not unique"
                # Example: groupby dg='sessions' by 'Client ID', or dg='hits' by 'Session ID'
                indices: dict[str, np.ndarray] = child.groupby(parent.index.name).indices
                # turn the {index1: array([ix1]), index2: array([ix2])} into [ [ix1], [ix2] ]
                # Example: 'users-sessions'
                res[f"{dg[i]}-{dg[i+1]}"] = [indices[key] for key in parent.index.values if key in indices]
        return res

    # Magic methods

    def __getitem__(self, index: int) -> dict:
        """Gets a Users-Sessions Dataset item."""
        if isinstance(index, slice):
            return self.to_batched_item([self[x] for x in range(index.start, index.stop)])
        dg = self.base_dataset.data_groups[0] # TODO: only 1 dg and only up to 2 tables in it for now.
        res = {dg[0]: self._get_top_level(index)}
        if len(dg) == 2:
            res[dg[1]] = self._get_second_level(index)
        return res

    def __len__(self):
        return self._len

    def __str__(self):

        shape = {k: f"{self.data[k].shape}->{self.data_shape[k]}" for k in self.tables}
        return f"{parsed_str_type(self)}. Shape: {shape}."
