import os

import numpy as np
from pandas import read_hdf

from gladeparser.backends import to_pandas_df, to_polars_df
from gladeparser.parser import to_hdf5
from gladeparser.columns import Group, GLADEDescriptor, get_columns

descriptor = GLADEDescriptor()
dirname = os.getcwd()
filename = os.path.join(dirname, "test/mock.txt")


class TestParse:
    def test_to_pandas_df(self):
        indices = [Group.ID.value, Group.CATALOG_ID.value]
        cols = get_columns(*indices)
        df = to_pandas_df(filename, cols)
        assert df.columns.to_list() == cols
        assert len(df) == 50

        last_line = df.iloc[-1]
        assert last_line["GLADE no"] == 50
        assert np.isnan(last_line["PGC no"])
        assert np.isnan(last_line["GWGC name"])
        assert np.isnan(last_line["HyperLEDA name"])

    def test_to_polars_df(self):
        indices = [Group.ID.value, Group.CATALOG_ID.value]
        cols = get_columns(*indices)
        df = to_polars_df(filename, cols=cols)
        assert df.columns == cols
        assert df.shape[0] == 50

        last_line = df.row(-1, named=True)
        assert last_line["GLADE no"] == 50
        assert last_line["PGC no"] is None
        assert last_line["GWGC name"] is None
        assert last_line["HyperLEDA name"] is None

    def test_parse_to_hdf5(self):
        indices = [Group.ID.value, Group.CATALOG_ID.value]
        cols = get_columns(*indices)
        dirname = os.getcwd()
        outfile = os.path.join(dirname, "out.hdf5")
        hdf5_key = "test_key"
        to_hdf5(filename, outfile, hdf5_key, cols)

        assert os.path.isfile(outfile)

        # Read data
        df = read_hdf(outfile, hdf5_key)

        assert df is not None
        assert df.columns.to_list() == cols
        assert len(df) == 50

        last_line = df.iloc[-1]
        assert last_line["GLADE no"] == 50
        assert np.isnan(last_line["PGC no"])
        assert np.isnan(last_line["GWGC name"])
        assert np.isnan(last_line["HyperLEDA name"])

        os.remove(outfile)
        assert not os.path.isfile(outfile)
