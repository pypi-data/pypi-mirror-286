"""DatasetHashCheck module"""

from loggez import loggez_logger as logger
from .dataset import Dataset

class DatasetHashCheck:
    """
    Dataset consistency class. Can be used in a 'with statement context manager'. It checks that the Dataset object has
    not changed on the previously existing columns. This is used to allow new columns to be added in an 'append only'
    fashion while making sure that the old ones were not modified between the initial call and the exist from the
    context manager. Useful for creating new features and guaranteeing dataset consistency.
    """
    def __init__(self, dataset: Dataset):
        self.dataset = dataset

        self.hash_before = dataset.hash
        self.shape_before = self.dataset.shape

    def __call__(self):
        logger.debug(f"Running dataset hash check on {self.dataset}")
        hash_after = self.dataset.hash

        if self.hash_before.keys() != hash_after.keys():
            raise ValueError(f"Keys have changed. Before: {self.hash_before.keys()}. After: {hash_after.keys()}")

        for dg in self.hash_before.keys():
            self.hash_before[dg].sort_index(inplace=True)
            hash_after[dg].sort_index(inplace=True)
            if (self.hash_before[dg] != hash_after[dg]).any():
                raise ValueError(f"Hash changed between enter and exit on data group '{dg}'. "
                                 f"Shape before: {self.shape_before[dg]}. After: {self.dataset.shape[dg]}. "
                                 "Did you add alter the original dataset instead of a new dataset at compute step ?")

    def __enter__(self, *args, **kwargs):
        return self

    def __exit__(self, *args, **kwargs):
        return self.__call__()
