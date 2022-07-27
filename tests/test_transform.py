from oocas.transform import Transform, CacheTransform


def test_transform():
    transform = Transform(
        lambda x, suffix: x + suffix,
        '.csv'
    )
    assert transform('file1') == 'file1.csv'


def test_cachetransform():
    transform = CacheTransform(
        lambda a, cache, b: a + cache.data + b,
        2
    )
    assert transform(1, 3) == 6
