import numpy as np

from oocas.cache import Cache, IndexCache, TimeIndexCache


def test_cache(fib_df):
    fn = Cache()
    fn(fib_df)
    assert fn.data.equals(fib_df)


def test_indexcache(fib_df):
    fn = IndexCache(1)
    fn(fib_df)
    assert np.array_equal(
        fn.data['x'].to_numpy(), np.array([5]))


def test_timeindexcache(fib_df):
    fn = TimeIndexCache('4S')
    fn(fib_df.set_index('time'))
    assert np.array_equal(
        fn.data['x'].to_numpy(), np.array([1, 1, 2, 3, 5]))