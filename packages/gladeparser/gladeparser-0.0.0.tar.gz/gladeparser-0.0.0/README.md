# gladeparser

![tests](https://github.com/binado/gladeparser/actions/workflows/test.yml/badge.svg)

Parser for the [GLADE+ galaxy catalog](https://glade.elte.hu/).

## Usage

To read the catalog into a `pandas.DataFrame`:

```python
from gladeparser import to_pandas_df

filename = "path/to/catalog"
df = to_pandas_df(filename)
```

The preferred way of reading the catalog is using a `polars` backend, especially if you want to filter out the data:

```python
from gladeparser import to_polars_df
import polars as pl

# Grab objects from 2MASS catalog with redshifts corrected for peculiar velocity
filters = (
    pl.col("2MASS name").is_not_null(),
    pl.col("z_cmb").is_not_null(),
    pl.col("z_cmb") > 0,
    pl.col("z flag") == 1,
    pl.col("dist flag").is_in([1, 3])
)

# Selected columns
cols = ["ra", "dec", "z_cmb"]

filename = "path/to/catalog"
df = to_polars_df(filename, cols=cols, **filters)
```

### Parsing a subset of columns

```python
from gladeparser import to_pandas_df, get_columns

# Select the columns you want and return their names
# See more options in get_columns docstring
cols = get_columns('Localization', 'Distance', names=True)

filename = "path/to/catalog"
df = to_pandas_df(filename, cols=cols)
```

## Installation

Clone the repo and run

```bash
pip install .
```

## Testing

Make sure that you have `pytest` installed, or run

```bash
pip install .[dev]
```

Then run

```bash
pytest
```

## References

See the GLADE+ paper on [arXiv](https://arxiv.org/abs/2110.06184).
