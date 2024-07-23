"""Dataset class module."""
from __future__ import annotations
from typing import Callable, Any, overload
from copy import copy, deepcopy
from pathlib import Path
import json
from natsort import natsorted
import pandas as pd
import numpy as np

from loggez import loggez_logger as logger

from .indexes import compute_indexes
from .stats import compute_stats
from .column_types import ColumnType, build_column_types, check_column_types
from .internal import check_data_groups_consistency, check_nans, build_data, build_data_groups
from .merge import merge_datasets
from .input_output import csv_read, csv_write, csv_peek, parquet_read, parquet_write, parquet_peek
from .utils import StrOrPath, flatten_list, parsed_str_type

class Dataset:
    """
    A `Dataset` represents a nested group of dataframes and contains the underlying data as a dict
    with string keys and `pd.DataFrame` values and the nested lists of indexes
    which help locating the corresponding data throughout the path.
    Notes:
    - each df must have a primary key (index) and each child dataframe must have a common join key with its parent.
    - all the columns, even inside the nested structure, must be named uniquely. The only exceptions are primary
    keys, as they are replicated across all data groups. The library will throw exceptions if this is not respected.
    - you can't have cycles in the tables (users -> sessions -> users). Join keys must be unidirectional
    - you can't more than 1 child/parent: dg1 -> [dg2, dg3] or [dg1, dg2] -> dg3 is not allowed, only dg1->dg2->dg3
    - you can have disjoin data groups: [products]. [users, sessions], as long as they are not interleaved

    Example:
         Assume we have a `users-sessions` dataset (one user has many sessions).
         The underlying data contains the users and the sessions dataframes. The indexes dict
         contains two lists for users and sessions respectively. The users list contains exactly the
         index of the users dataframe. The sessions list has the same size with the users list and
         the i-th elements in the sessions list provides the indices of all the sessions associated to
         the i-th user in the users list (i.e. for each user in the users dataframe, we know precisely
         how to retrieve all its sessions from the sessions dataframe).

    Args:
        data: The underlying data as a dict of `pd.DataFrames` or `pd.Series`.
        column_types: Optional argument to enforce some ambiguous column types (i.e. categoricals being numbers)
        check_consistency: If True checks the consistency of all the join keys.

    Attributes:
        data: The underlying data as a dict of `pd.DataFrame` with the keys ordered from root to leaf.
        indexes: The lists of the dataset's nested indexes.
        join_keys: The join keys of the dataset as a dict.
        primary_keys: The primary keys of the dataset as a dict.
        columns: The columns of the dataset values as a dict.
        all_column_names: The list of all column names, primary keys, and join keys for all tables.
        hash: The hashes of the dataset values as a dict.
        shape: The shapes of the dataset values as a dict.
        data_groups: The dict of lists representing the nested data groups.
        tables: The list of tables from which data_groups are formed.
        keys: The keys of the dataset (used as compatibility with dict).
        values: The values of the dataset (used as compatibility with dict).
        items: The items of the dataset (used as compatibility with dict).
    """
    def __init__(self,
                 data: dict[str, pd.DataFrame | pd.Series],
                 column_types: dict[str, list[ColumnType]] | None = None,
                 check_consistency: bool = False,
                 ):
        assert isinstance(data, dict), f"Datasets can only be constructed out of dicts of dataframes. Got {type(data)}"
        assert len(data.keys()) > 0, "No data groups were provided"
        self._data: dict[str, pd.DataFrame] = build_data(data)
        self._column_types = build_column_types(self, column_types)
        self._data_groups: list[list[str]] = build_data_groups(self)
        self._indexes: dict[str, list] | None = None
        self._stats: dict[str, dict[str, dict]] | None = None
        self._metadata: dict[str, Any] = {}
        if check_consistency:
            self.check_consistency()

    @property
    def data(self):
        """Returns the underlying data of this dataset."""
        return self._data

    @property
    def column_types(self) -> dict[str, dict[str, ColumnType]]:
        """Returns the dataset's data types dictionary"""
        assert self._column_types is not None, "Data types is not constructed. Call the constructor properly."
        return {dg: self._column_types[dg] for dg in self.tables}

    @property
    def dtypes(self) -> dict[str, dict[str, ColumnType]]:
        """same as self.column_types"""
        return self.column_types

    @property
    def indexes(self) -> dict[str, list]:
        """Returns the nested indexes of the dataset."""
        if self._indexes is None:
            self._indexes = compute_indexes(self)
        return self._indexes

    @property
    def stats(self) -> dict[str, dict[str, np.ndarray]]:
        """
        Returns the statistics (min, max) of each column in the dataset
        Return format:
        {
            "dg1": {
                "col1": np.array([
                    min_x, # can be also an array if dataset_type of col is categorical/vector
                    max_y
                ])
            }
        }
        """
        if self._stats is None:
            self._stats = compute_stats(self)
        return self._stats

    @property
    def metadata(self) -> dict[str, Any]:
        """Returns the metadata. It is guaranteed that it can be converted to a json representation"""
        return self._metadata

    @metadata.setter
    def metadata(self, metadata: dict[str, Any]):
        assert isinstance(metadata, dict), f"Expected a dictionary metadata, got {metadata}"
        assert json.loads(json.dumps(metadata)) == metadata, f"Metadata doesn't seem JSON-able: {metadata}"
        self._metadata = metadata

    @property
    def join_keys(self) -> dict[str, list[str]]:
        """
        Returns the join keys of the dataset as a dict {data_group: [join keys]}. We assume that each nested group
        contains the primary key of its parent.
        """
        res = {}
        for dg in self.data_groups:
            dg_keys = []
            for tb in dg:
                res[tb] = copy(dg_keys)
                dg_keys.append(self.primary_keys[tb])
        return res

    @property
    def primary_keys(self) -> dict[str, str]:
        """Returns the primary keys of the dataset as a dict {table: primary key}."""
        return {dg: self._data[dg].index.name for dg in self.tables}

    @property
    def columns(self) -> dict[str, list[str]]:
        """Returns the columns of the dataset as a dict {table: [columns]}."""
        return {dg: self._data[dg].columns.tolist() for dg in self.tables}

    @property
    def all_column_names(self) -> list[str]:
        """Returns the values of all column names + primary keys + join keys for all data groups."""
        all_cols = flatten_list(self.columns.values())
        all_keys = flatten_list(self.primary_keys.values())
        return list(set(all_cols + all_keys))

    @property
    def hash(self) -> dict[str, pd.Series]:
        """Returns the pandas hash of the dataset as a dict {data_group: hash}."""
        res = {}
        for tb in self.tables:
            hashable_df = self[tb].select_dtypes(exclude=[object])
            res[tb] = pd.util.hash_pandas_object(hashable_df, index=True)
        return res

    @property
    def shape(self) -> dict[str, tuple[int, int]]:
        """Returns the shapes of the dataset as a dict {data_group: dataframe_shape}."""
        return {dg: tuple(self._data[dg].shape) for dg in self.tables}

    @property
    def data_groups(self) -> list[list[str]]:
        """
        Returns the data groups as a list of lists. It is assumed that the data groups are designed as a forest of
        linear trees (1 child only). So, we might have [ [products], [users, sessions] ] as two data groups. Each inner
        data group is guaranteed to be returned from root to leaf, so no [ [products], [sessions (X), users] ].
        However, since all data groups are equal at top level, we may get them in any order, so
        [ [users, sessions], [products] ] and [ [products], [users, sessions] ]
        are both fine, because only the data groups are shuffled.
        """
        return self._data_groups

    @property
    def tables(self) -> list[str]:
        """Returns all the tables as a flattened list"""
        return flatten_list(self.data_groups)

    def keys(self):
        """Returns the data groups of the dataset. Used as compatibility to dicts. No guarantees on dg order!"""
        return self._data.keys()

    def values(self):  # pragma: no cover
        """Returns the dataframes of the dataset. Used as compatibility to dicts. No guarantees on dg order!"""
        return self._data.values()

    def items(self):
        """Returns the keys-values of the dataset. Used as compatibility to dicts. No guarantees on dg order!"""
        return self._data.items()

    def copy(self) -> Dataset:
        """Returns a (deep) copy of this dataset"""
        return deepcopy(self)

    # pylint: disable=protected-access
    def sort(self, inplace: bool) -> Dataset:
        """Sorts the index of all data groups of this dataset."""
        logger.debug(f"Sorting this dataset {self} (inplace={inplace})")
        dataset: Dataset = self if inplace else self.copy()
        for dg in dataset.tables:
            # We need to sort from the first join key to the last, including the index.
            # so, for dg=hits (users>sessions>hits), we first sort by client id, then session id and lastly hit id
            tmp_dg = dataset._data[dg].reset_index()
            sort_keys = [*self.join_keys[dg], self.primary_keys[dg]]
            tmp_dg = tmp_dg.sort_values(sort_keys)
            dataset._data[dg] = tmp_dg.set_index(self.primary_keys[dg])
        return self

    def sort_columns(self):
        """Sorts the columns of the dataset by name, inplace"""
        for dg in self.tables:
            cols = self.columns[dg]
            sorted_cols = natsorted(cols)
            self._data[dg] = self._data[dg][sorted_cols]

    def get_column(self, col_name: str) -> tuple[str, pd.Series]:
        """Gets the data of a column, if it exists in this dataset, alongside the data group it is part of"""
        assert isinstance(col_name, str), f"Expected a string, got {col_name}"
        for k, v in self.items():
            if col_name == v.index.name:  # pragma: no cover
                return k, v.index
            if col_name in v.columns:
                return k, v[col_name]
        raise KeyError(f"Column '{col_name}' not found in dataset.")

    def merge(self, other: Dataset | dict[str, pd.DataFrame | pd.Series],
              *args, must_be_disjoint: bool = False, **kwargs) -> Dataset:
        """Given another dataset, merge using the underlying pandas.merge method for each data group."""
        if isinstance(other, dict):
            logger.warning("Merge was called with a dionary of dataframes. Converting to Dataset.")
            other = Dataset(other)
        assert isinstance(other, Dataset), f"Can only merge two datasets together. Got '{type(other)}'"
        new_data, new_column_types = merge_datasets(self, other, *args, must_be_disjoint=must_be_disjoint, **kwargs)
        res = Dataset(new_data, new_column_types)
        # save some computation time later on.
        if self._indexes is not None:
            res._indexes = self._indexes
        elif other._indexes is not None:
            res._indexes = other._indexes
        return res

    def apply_merge(self, fn: Callable) -> Dataset:
        """
        Applies the function on the dataset, then merges the result. Useful for chaining features.
        Example: For f=feature callback. dataset = dataset.merge(f(dataset)) => dataset = dataset.apply_merge(f)
        """
        return self.merge(fn(self))

    # pylint: disable=unused-argument
    def check_consistency(self, data_groups: bool = True, check_for_nans: bool = True, column_types: bool = True):
        """
        Checks called after mutable methods that work with the underlying dataframes directly as we cannot ensure that
        the dataframe has not changed leading to corrupted memory. We can however, check afterwards that the datset is
        still clean.
        """
        if data_groups:
            check_data_groups_consistency(self)
        if check_for_nans:
            check_nans(self)
        if column_types:
            check_column_types(self, self.column_types)

    # I/O operations

    @staticmethod
    def read(path: StrOrPath, data_format: str, tables_pk: dict[str, str],
             columns: dict[str, list[str]] = None, **kwargs) -> Dataset:
        """
        Loads the dataset from a path given a mapping {data group => primary key} for all data groups and a list
        of columns for each data-groups. If columns is not set, it will read all the columns.
        Supported formats: "csv", "parquet". If indexes are provided, they will be used to set the index of the data.

        Usage: Datset.read("/path/to/disk_dir", "csv", tables_pk={"users": "client_id"}, [columns=col]}

        Parameters:
        - path: The path to the dataset on disk.
        - data_format: The format of the dataset. Supported: "csv", "parquet".
        - tables_pk: A mapping {table => primary key} for all tables.
        - columns: A mapping {table => list of columns} for all tables. If None, all columns will be read.
        - kwargs: Additional arguments to the underlying reader.
        """
        assert data_format in ("csv", "parquet"), f"Unsupported data format: {data_format}"
        path = Path(path)
        if columns is None:
            columns = Dataset.peek(path, data_format, tables_pk)
            # dataset.peek returns a {table: {col: col_tye}} dict, we only need the keys for the readers
            columns = {k: list(v.keys()) for k, v in columns.items()}

        for table in columns:
            if tables_pk[table] not in columns[table]:
                logger.warning(f"Table '{table}' didn't have pk '{tables_pk[table]}' in the list of cols.")
                columns[table] = [*columns[table], tables_pk[table]]

        if data_format == "csv":
            data, dataset_types = csv_read(path, tables_pk, columns, **kwargs)
        if data_format == "parquet":
            data, dataset_types = parquet_read(path, tables_pk, columns, **kwargs)
        dataset = Dataset(data, dataset_types)

        if (path / "indexes.npy").exists():
            dataset._indexes = np.load(path / "indexes.npy", allow_pickle=True).item()
        if (path / "metadata.json").exists():
            with open(path / "metadata.json", "r", encoding="utf-8") as f:
                dataset.metadata = json.load(f)
        return dataset

    @staticmethod
    def peek(path: StrOrPath, data_format: str, tables_pk: dict[str, str]) -> dict[str, dict[str, str]]:
        """
        Reads only the header and the dataset types from a path given a mapping {data group => primary key}.
        Supported formats: "csv", "parquet".

        Usage: Dataset.peek("/path/to/disk_dir", "parquet", {"users": "client_id", "sessions": "session_id"})
        """
        if data_format == "csv":
            return csv_peek(Path(path), tables_pk)
        if data_format == "parquet":
            return parquet_peek(Path(path), tables_pk)
        raise NotImplementedError(f"Unsupported data format: {data_format}")

    def write(self, path: StrOrPath, data_format: str, write_indexes: bool = False, write_metadata: bool = False,
              write_stats: bool = False):
        """
        Saves the dataset to a path on the disk given a data format.
        Usage: dataset.write("/path/to/disk_dir", "csv")

        Parameters:
        - path: The path where the dataset's tables will be saved
        - data_format: The format to use for saving the dataset. Supported formats: "csv", "parquet".
        - write_indexes: Whether to write the indexes of the dataframes or not.
        - write_metadata: Whether to write the metadata of the dataset or not.
        - write_stats: Whether to write the stats of the dataset or not.
        """
        assert data_format in ("csv", "parquet"), f"Unsupported data format: {data_format}"
        path = Path(path)
        if data_format == "csv":
            csv_write(self, path)
        if data_format == "parquet":
            parquet_write(self, path)

        if write_indexes:
            np.save(path / "indexes.npy", self.indexes)
        if write_metadata:
            with open(path / "metadata.json", "w", encoding="utf-8") as filename:
                json.dump(self.metadata, filename, indent=4)
        if write_stats:
            np.save(path / "dataset_stats.npy", self.stats)

    @overload
    def __getitem__(self, index: str) -> pd.DataFrame:
        ...

    @overload
    def __getitem__(self, index: dict) -> Dataset:
        ...

    @overload
    def __getitem__(self, index: list) -> Dataset:
        ...

    def __getitem__(self, index: dict | list | str) -> Dataset | pd.DataFrame:
        if isinstance(index, dict):
            res, res_dtypes = {}, {}
            # We can also index a dataset with a subset of columns {"dg": [cols], "dg2": [cols2]}
            for dg, v in index.items():
                assert isinstance(v, (tuple, set, list)), f"Expeted a list to index columns using a dict, got {v}"
                _v = sorted(list(set([*[(f.name if hasattr(f, "name") else f) for f in v], *self.join_keys[dg]])))
                res[dg] = self._data[dg][_v]
                res_dtypes[dg] = {v: self.column_types[dg][v] for v in self._data[dg].columns}
            return Dataset(res, res_dtypes)

        if isinstance(index, list):
            res, res_dtypes = {}, {}
            for dg in index:
                res[dg] = self._data[dg]
                res_dtypes[dg] = self.column_types[dg]
            return Dataset(res, res_dtypes)

        return self._data[index]

    def __getattribute__(self, name: str) -> Any:
        try:
            return super().__getattribute__(name)
        except AttributeError as ex:
            # this enables syntax like dataset.users if 'users' is a table in the dataset.
            # Alternative to dataset["users"], similarily to how it's done in pandas as well for columns.
            try:
                return self._data[name]
            except Exception:
                raise AttributeError(ex)

    def __setitem__(self, item, value):
        raise ValueError("Setting values to data groups is not allowed. Use dataset.merge() or Dataset() constructor.")

    def __contains__(self, key):
        return key in self.tables

    def __str__(self) -> str:
        f_str = parsed_str_type(self)
        for k in self.tables:
            f_str += f" '{k} ('{self._data[k].index.name}')':  {self._data[k].shape}"
        return f_str

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, other: Dataset) -> bool:
        """Two datasets are equal if they have the same keys and the same dataframe values."""
        if not isinstance(other, Dataset):
            return False

        # check key equality
        if self.tables != other.tables:
            return False

        # check shape equality
        if self.shape != other.shape:
            return False

        # check columns equality. They can be permuted, but we still count them
        if sorted(self.columns) != sorted(other.columns):
            return False

        # check data types
        for tb in self.tables:
            _other_tb = other[tb][self[tb].columns]
            if (self[tb].dtypes != _other_tb.dtypes).any():
                return False

        # check index equality
        for tb in self.tables:
            if (self[tb].index != other[tb].index).any():
                return False

        # finally, check all the values via hashing the rows
        self_hash = self.hash
        other_hash = other.hash
        for tb in self.tables:
            if (self_hash[tb] != other_hash[tb]).any():
                return False
        return True

    def __iter__(self):
        return iter(self._data)
