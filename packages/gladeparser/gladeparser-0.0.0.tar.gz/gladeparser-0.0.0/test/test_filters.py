import os

from gladeparser.parser import to_df
from gladeparser.filters import filter_nonpositive_redshift, filter_quasars_clusters

dirname = os.getcwd()
filename = os.path.join(dirname, "test/mock.txt")


class TestFilters:
    def test_filter_nonpositive_redshift(self):
        df = to_df(filename, filter_fn=filter_nonpositive_redshift)
        assert df.shape[0] == 49

    def test_filter_quasars_clusters(self):
        df = to_df(filename, filter_fn=filter_quasars_clusters)
        assert df.shape[0] == 50
