import pytest
from pathlib import Path
import pandas as pd


@pytest.fixture(scope='session')
def fib_df():
     return pd.DataFrame({
        'time': [
            pd.to_datetime('2022-09-09 00:00:00'),
            pd.to_datetime('2022-09-09 00:00:01'),
            pd.to_datetime('2022-09-09 00:00:01'),
            pd.to_datetime('2022-09-09 00:00:02'),
            pd.to_datetime('2022-09-09 00:00:03'),
            pd.to_datetime('2022-09-09 00:00:05'),
        ],
        'x': [0, 1, 1, 2, 3, 5]
    })


@pytest.fixture(scope='session')
def data_dir(tmp_path_factory):
    return tmp_path_factory.mktemp('data')


@pytest.fixture(scope='session')
def sample_paths(data_dir, fib_df):
    paths = [data_dir / Path(path) for path in [
        'file_1.parquet',
        'file_2.parquet'
    ]]
    for path in paths:
        fib_df.to_parquet(path)
    return paths


@pytest.fixture(scope='session')
def sample_path(sample_paths):
    return sample_paths[0]
