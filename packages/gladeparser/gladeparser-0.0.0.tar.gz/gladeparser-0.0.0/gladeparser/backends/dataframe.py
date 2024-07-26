from typing import Union

from pandas import DataFrame as PandasDataFrame
from polars import DataFrame as PolarsDataFrame

DataFrameLike = Union[PandasDataFrame, PolarsDataFrame]


def as_pandas_df(df: DataFrameLike, **kwargs) -> PandasDataFrame:
    return df if isinstance(df, PandasDataFrame) else df.to_pandas(**kwargs)
