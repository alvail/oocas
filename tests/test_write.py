from pathlib import Path

from oocas.write import Write, FileWrite, MultiWrite


def test_write():
    fn = Write(
        lambda x, suffix: x + suffix,
    )
    assert fn('file1', '.csv') == 'file1.csv'


def test_filewrite():
    fn = FileWrite(
        lambda a, _, b: a + b,
        path_transform=lambda x: x[0],
        path_part_replace=('C', 'D'),
        name_transform=lambda x: x[:-1],
        suffix='.csv',
        add_result=True,
        b=2
    )
    assert fn(1, [Path('/C/data/file1.parquet')]) == (Path('/D/data/file.csv'), 3)


def test_multiwrite():
    fn = MultiWrite(
        Write(lambda x, path: path),
    )
    assert fn((1, 2), ('file1.csv', 'file2.csv'))\
        == ['file1.csv', 'file2.csv']