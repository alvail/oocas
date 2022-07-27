# oocas

[![PyPI version fury.io](https://badge.fury.io/py/oocas.svg)](https://pypi.python.org/pypi/oocas/)
[![PyPI license](https://img.shields.io/pypi/l/oocas.svg)](https://pypi.python.org/pypi/oocas/)
[![PyPI download month](https://img.shields.io/pypi/dm/oocas.svg)](https://pypi.python.org/pypi/oocas/)

**oocas** is an out-of-core data processing framework built for pandas. Its main purpose is local ETL processing of large data by sequentially processing smaller files.

## Installation

```bash
pip install oocas
```

```bash
conda install -c conda-forge oocas 
```

## Usage

The data, which are specified by a list of file paths, are read, transformed, and written/returned. In a transform substep data can be cached to be available in later transform substeps. A processing pipeline is build out of callable components.

+ **Process**
+ **Read**, **FileRead**, ParquetRead, ParquetMetadataRead, **MultiRead**
+ **Transform**, **CacheTransform**
+ **Cache**, IndexCache, TimeIndexCache
+ **Write**, **FileWrite**, ParquetWrite, **MultiWrite**

High level components (bold) support plugin callables in addition to a variety of other useful arguments. Low level components inherit their behavior by passing a predefined method this way.

## Examples

Examples can be found in the docs.

### Read files to dataframe
```python
import oocas as oc

paths = oc.find_paths('data/raw')
sqp = oc.Process(oc.ParquetRead(), progress_bar=False)
df = pd.concat(sqp(paths), axis=0)
```

###  Random sampling
```python
import oocas as oc

sqp = oc.Process(
    oc.ParquetMetaDataRead(),
    lambda x: x.num_rows,
    progress_bar=False)

nrows = sum(sqp(paths))                     
sample_idxs = np.random.choice(nrows, 10**3)

def sample(df, cache):
    adjusted_idxs = sample_idxs - cache.data
    cache(cache.data + len(df))
    return df.iloc[[                                      
        idx for idx in adjusted_idxs\
             if idx >= 0 and idx < len(df)
    ]].copy()

sqp = oc.Process(
    oc.ParquetRead(),
    oc.CacheTransform(sample, cache=0))

sample_df = pd.concat(sqp(paths), axis=0)
```

###  Time series moving average
```python
import oocas as oc

def moving_average(df, cache):
    nrows = len(df)
    df = pd.concat([cache.data, df])
    cache(df)
    return df.rolling(cache.lookback)\
        .mean().iloc[-nrows:]
    
sqp = oc.Process(
    oc.ParquetRead(),
    oc.CacheTransform(
        moving_average,
        oc.TimeIndexCache('1H')),
    oc.ParquetWrite(
        path_part_replace=('raw', 'mavg'),
        mkdirs=True))

mavg_paths = sqp(paths)
```

### N-to-1 file write

```python
import oocas as oc

pickle_multi_to_one_write = oc.FileWrite(
    lambda x, path, **kwargs:\
        x.to_pickle(path, **kwargs),
    path_transform=lambda x: x[0],
    path_part_replace=('raw', 'pickle'),
    name_transform=lambda x:\
        '_'.join(x.split('_')[1:]),
    suffix='.pkl.gz',
    mkdirs=True,
    overwrite=True,
    compression='infer')
```