from typing import Optional, List

import polars as pl

from ..columns import GLADEDescriptor


def to_polars_df(
    filename: str,
    *expr: pl.Expr,
    cols: Optional[List[str]] = None,
    **kwargs,
) -> pl.DataFrame:
    """Parse the GLADE+ text file into a Polars DataFrame.
    Uses Polars.scan_csv method to efficiently query over the whole CSV before parsing.

    Parameters
    ----------
    filename : str
        The path to the GLADE+ text file
    cols : list, optional
        The list of columns to extract from the file. See `GlADEDescriptor.get_columns`.
        If None, will return all columns. By default None.
    expr : polars.Expr
        Polars filter expressions to be queried

    Returns
    -------
    Polars.DataFrame
        The DataFrame containing the extracted columns after filtering out the data
    """
    descriptor = GLADEDescriptor()
    query = pl.scan_csv(
        filename,
        has_header=False,
        separator=" ",
        schema_overrides=descriptor.polars_schema,
        new_columns=descriptor.names,
        null_values=["null"],
        **kwargs,
    )
    if len(expr) > 0:
        query = query.filter(*expr)

    return query.select(*(cols or descriptor.names)).collect()
