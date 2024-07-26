from .dataframe import DataFrameLike, as_pandas_df


def df_to_hdf5(df: DataFrameLike, filename: str, key: str, **kwargs):
    # format="table" is necessary to prevent a PerformanceWarning,
    # see https://github.com/pandas-dev/pandas/issues/3622#issuecomment-126132206
    as_pandas_df(df).to_hdf(filename, key, format="table", **kwargs)
