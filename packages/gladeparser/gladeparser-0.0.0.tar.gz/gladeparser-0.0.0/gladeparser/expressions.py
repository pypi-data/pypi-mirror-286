from typing import Tuple
import polars as pl


def filter_by_valid_redshifts(zmin: float = 0.0) -> Tuple[pl.Expr, pl.Expr]:
    return (pl.col("z_cmb") > zmin, pl.col("z_cmb").is_not_null())


def filter_by_catalog_name(catalog_name: str) -> Tuple[pl.Expr]:
    return (pl.col(catalog_name).is_not_null(),)


PGC = filter_by_catalog_name("PGC no")
GWGC = filter_by_catalog_name("GWGC name")
WISExSCOS = filter_by_catalog_name("WISExSCOS name")
TWOMASS = filter_by_catalog_name("2MASS name")
HYPERLEDA = filter_by_catalog_name("HyperLEDA name")
SDSS_DR16Q = filter_by_catalog_name("SDSS-DR16Q name")
