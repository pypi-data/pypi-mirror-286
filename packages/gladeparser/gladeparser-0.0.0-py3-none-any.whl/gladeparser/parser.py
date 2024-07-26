from typing import Callable, Optional

import pandas as pd
from tqdm import tqdm

from .columns import GLADEDescriptor


def to_df(
    filename: str,
    cols: Optional[list] = None,
    filter_fn: Optional[Callable[[pd.DataFrame], pd.DataFrame]] = None,
    chunksize: int = 200000,
    **kwargs,
) -> pd.DataFrame:
    """Parse the GlADE+ text file into a Pandas DataFrame.
    Uses Pandas.read_csv method.

    Parameters
    ----------
    filename : str
        The path to the GLADE+ text file
    cols : list, optional
        The list of columns to extract from the file. See `GlADEDescriptor.get_columns`.
        If None, will return all columns. By default None.
    filter_fn : Callable[[pd.DataFrame], pd.DataFrame], optional
        A filter function to be executed on each DataFrame chunk. By default None.
    chunksize : int, optional
        The chunksize argument of read_csv. Defaults to 200000, which corresponds to roughly 100 iterations

    Returns
    -------
    Pandas.DataFrame
        The DataFrame containing the extracted columns after filtering out the data
    """
    descriptor = GLADEDescriptor()
    reader_args = dict(
        sep=" ",
        names=descriptor.names,
        usecols=cols,
        dtype=descriptor.column_dtypes,
        header=None,
        false_values=["null"],
        chunksize=chunksize,
    )
    chunks = []
    _desc = "Parsing GLADE+ catalog with the desired options"
    with pd.read_csv(filename, **reader_args, **kwargs) as reader:
        fn = filter_fn if filter_fn is not None else lambda x: x
        for chunk in tqdm(reader, desc=_desc):
            chunks.append(fn(chunk))

        catalog = pd.concat(chunks, ignore_index=True)

    return catalog


def to_hdf5(
    filename: str,
    output_filename: str,
    hdf5_key: str,
    cols: Optional[list] = None,
    filter_fn: Optional[Callable[[pd.DataFrame], pd.DataFrame]] = None,
    chunksize: int = 200000,
    complevel: Optional[int] = None,
    **kwargs,
):
    """Parse the GlADE+ text file onto an HDF5 file.
    Uses Pandas.read_csv method.

    Parameters
    ----------
    filename : str
        The path to the GLADE+ text file
    output_filename: str
        The path to the output file
    hdf5_key: str
        The hdf5 key to put the data
    cols : list, optional
        The list of columns to extract from the file. See `GlADEDescriptor.get_columns`.
        If None, will return all columns. By default None.
    filter_fn : Callable[[pd.DataFrame], pd.DataFrame], optional
        A filter function to be executed on each DataFrame chunk. By default None.
    chunksize : int, optional
        The chunksize argument of read_csv. Defaults to 200000, which corresponds to roughly 100 iterations
    complevel : int, optional
        complevel argument in pandas.HDFStore
    """
    descriptor = GLADEDescriptor()
    reader_args = dict(
        sep=" ",
        names=descriptor.names,
        usecols=cols,
        dtype=descriptor.column_dtypes,
        header=None,
        false_values=["null"],
        chunksize=chunksize,
    )
    _desc = "Parsing GLADE+ catalog with the desired options"
    with pd.HDFStore(output_filename, mode="w", complevel=complevel) as store:
        with pd.read_csv(filename, **reader_args, **kwargs) as reader:
            fn = filter_fn if filter_fn is not None else lambda x: x
            for chunk in tqdm(reader, desc=_desc):
                store.append(hdf5_key, fn(chunk))
