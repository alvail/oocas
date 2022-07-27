from oocas.read import Read, FileRead, ParquetRead, ParquetMetaDataRead, MultiRead, find_paths


def test_read():
    fn = Read(
        lambda x, suffix: x + suffix,
        '.csv'
    )
    assert fn('file1') == 'file1.csv'


def test_fileread():
    fn = FileRead(
        lambda x, suffix: x + suffix,
        add_path = True,
        suffix='.csv'
    )
    assert fn('file1') == ('file1.csv', 'file1')


def test_parquetread(sample_path, fib_df):
    fn = ParquetRead()
    df = fn(sample_path)
    assert df.equals(fib_df)


def test_parquetmetadataread(sample_path):
    fn = ParquetMetaDataRead()
    assert fn(sample_path).num_rows == 6


def test_multiread():
    fn = MultiRead(
        FileRead(
            lambda x, suffix: x + suffix,
            add_path=True),
    )
    assert fn(('file1', 'file2'), '.csv')\
        == [('file1.csv', 'file1'), ('file2.csv', 'file2')]


def test_findpaths(data_dir, sample_paths):
    paths = find_paths(data_dir, recursive=True)
    assert paths[0] == sample_paths


    