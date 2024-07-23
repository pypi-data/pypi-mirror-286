# Pandas Dataset library

Wrapper on top of pandas to support nested datasets from pandas dataframes provided as dicts.

Readers for CSV and parquet.

Minimal support for adding new features.

## Usage

Copy paste from [the examples](examples/basic_nested_dataset.py).

```python
#!/usr/bin/env python3
from pprint import pprint
import pandas as pd
import numpy as np
from pandas_dataset import Dataset

n_root, n_nested = 100, 300 # 100 rows in root df, 300 in the nested one which joins the root one
df_root = pd.DataFrame({"column": np.random.randn(100,), # random floats
                        "column2": [''.join(chr(_y) for _y in y) for y in np.random.randint(ord("A"), ord("z"), # text
                                    size=(100, 10))]}).set_index(pd.Index(range(100), name="root_index"))
df_nested = pd.DataFrame({"column3": [x.astype(object) for x in np.random.randn(300, 20)], # vector column (embeddings)
                          "root_index": np.random.randint(0, 100, size=(300, )) # join key with df_root
                          })
dataset = Dataset({"root": df_root, "nested": df_nested})
print(dataset)
pprint(dataset.dtypes)

```

Outputs:
```
[20240311 12:06-WARNING] Data group 'nested' has empty index name. Defaulting to 'nested' (internal.py:75)
Dataset: 'root ('root_index')':  (100, 2) 'nested ('nested')':  (300, 2)
{'nested': {'column3': 'vector', 'nested': 'int', 'root_index': 'int'},
 'root': {'column': 'float', 'column2': 'object', 'root_index': 'int'}}
```

Explanation:
- we print the index a well in the dtypes. `root_index` is the index of `df_root`. `nested` is the index of
`df_nested` which is automatically added because we provide an empty index name (no `set_index`) so the name is taken
from the table name (key of the dict to the constructor)
- `column` is a float column with random numbers
- `column2` is an object column (text)
- `column3` is a vector column (arrays) which can be used for embeddings purposes (i.e. knn embedding)
- `nested` is the join key from `df_nested` to `df_root` so each entry in the nested df is directly mapped to the entry
in the root df!
