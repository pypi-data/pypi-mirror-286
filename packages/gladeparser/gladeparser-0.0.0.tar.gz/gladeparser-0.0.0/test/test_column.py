import pytest

import numpy as np

from gladeparser.columns import Group, GLADEDescriptor, get_columns

from .fixtures import column_names

descriptor = GLADEDescriptor()

catalogs_indices = [2, 3, 4, 5, 6, 7]
catalogs_names = [
    "PGC no",
    "GWGC name",
    "HyperLEDA name",
    "2MASS name",
    "WISExSCOS name",
    "SDSS-DR16Q name",
]


class TestColumn:
    def test_groups(self):
        assert descriptor.groups == Group.values()

    def test_names(self):
        assert descriptor.names == column_names()

    @pytest.mark.parametrize(
        "ids, names", [([1, 2, 3, 4, 5, 6, 7, 8], column_names()[:8])]
    )
    def test_column_names(self, ids, names):
        assert descriptor._index_to_name(ids) == names

    def test_column_dtypes(self):
        true_dtypes = [int] + [str] * 7 + [np.float64] * 32
        dtypes = list(descriptor.column_dtypes.values())
        assert true_dtypes == dtypes

    @pytest.mark.parametrize(
        "args, indices",
        [
            ([1], [1]),  # Explicit Index
            ([Group.ID.value], [1]),  # Index via group
            ([1] * 10, [1]),  # Repeated indices
            ([2, 3, 4, 5, 6, 7], catalogs_indices),  # Multiple indices returned
            (
                [2, 2, 4, 4, 5, 6, 3, 3, 3, 7],
                catalogs_indices,
            ),  # Multiple indices, repeated input
            ([Group.CATALOG_ID.value], catalogs_indices),  # Multiple indices via group
            (
                [Group.CATALOG_ID.value, Group.CATALOG_ID.value],
                catalogs_indices,
            ),  # Multiple indices via group, repeated
            (
                [
                    "PGC no",
                    "GWGC name",
                    "HyperLEDA name",
                    "2MASS name",
                    "WISExSCOS name",
                    "SDSS-DR16Q name",
                    "GWGC name",
                    "GWGC name",
                ],
                catalogs_indices,
            ),  # Multiple indices, repeated input via column name
        ],
    )
    def test_columns_to_indices(self, args, indices):
        assert descriptor._columns_to_indices(*args) == indices

    def test_columns_to_indices_invalid_value(self):
        # Invalid ids
        with pytest.raises(ValueError):
            descriptor._columns_to_indices(3.14)  # type: ignore

    @pytest.mark.parametrize(
        "args, names",
        [
            ([1], ["GLADE no"]),  # Explicit Index
            ([Group.ID.value], ["GLADE no"]),  # Index via group
            ([1] * 10, ["GLADE no"]),  # Repeated indices
            (catalogs_indices, catalogs_names),  # Multiple indices returned
            (
                [2, 2, 4, 4, 5, 6, 3, 3, 3, 7],
                catalogs_names,
            ),  # Multiple indices, repeated input
            ([Group.CATALOG_ID.value], catalogs_names),  # Multiple indices via group
            (
                [Group.CATALOG_ID.value, Group.CATALOG_ID.value],
                catalogs_names,
            ),  # Multiple indices via group, repeated
            (
                [
                    "PGC no",
                    "GWGC name",
                    "HyperLEDA name",
                    "2MASS name",
                    "WISExSCOS name",
                    "SDSS-DR16Q name",
                    "GWGC name",
                    "GWGC name",
                ],
                catalogs_names,
            ),  # Multiple indices, repeated input via column name
        ],
    )
    def test_get_columns(self, args, names):
        assert descriptor.get_columns(*args) == names
        assert get_columns(*args) == names

    def test_get_columns_invalid_value(self):
        # Invalid ids
        with pytest.raises(ValueError):
            descriptor.get_columns(3.14)  # type: ignore

    def test_get_columns_all_columns(self):
        # All rows
        assert descriptor.get_columns() == column_names()
        assert get_columns() == column_names()
