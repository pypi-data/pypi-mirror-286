def filter_nonpositive_redshift(chunk):
    query = "z_cmb.notnull() and z_cmb >= 0"
    return chunk.query(query)


def filter_quasars_clusters(chunk):
    query = '`Object type flag` == "G"'
    return chunk.query(query)


def filter_inferred_redshift(chunk):
    query = "`dist flag` == [1, 3]"
    return chunk.query(query)


def filter_no_peculiar_velocity_corrections(chunk, z_max):
    query = "`z flag` == 0 and z_cmb < z_max"
    return chunk.query(query)


def filter_catalog(chunk, catalog_name):
    query = "catalog_name.notnull()"
    return chunk.query(query)


class FilterAggregator:
    def __init__(self):
        self._fns = []

    def add(self, fn, *args, **kwargs):
        # Ensure args and kwargs are not None
        args = args if args is not None else ()
        kwargs = kwargs if kwargs is not None else {}
        el = [fn, args, kwargs]
        self._fns.append(el)
        return self

    def bulk_add(self, fns):
        for el in fns:
            try:
                _ = len(el)
            except TypeError:
                el = (el, (), {})
            self._fns.append(el)

    def apply(self, chunk):
        for fn, args, kwargs in self._fns:
            chunk = fn(chunk, *args, **kwargs)

        return chunk
