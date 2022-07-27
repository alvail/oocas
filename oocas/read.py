from typing import Any, Callable, List, Union, Tuple
from pathlib import Path
import pandas as pd
import pyarrow.parquet as pq


class Read:
    def __init__(self, fn: Callable, *args, **kwds) -> None:
        self._fn = fn
        self._args = args
        self._kwds = kwds

    def __call__(self, path: Any, *args, **kwds) -> Any:
        return self._fn(path, *self._args, *args, **self._kwds, **kwds)


class FileRead(Read):
    def __init__(self, fn: Callable, add_path: bool = False, *args, **kwds) -> None:
        super().__init__(fn, *args, **kwds)
        self._add_path = add_path

    def __call__(self, path: Path, *args, **kwds) -> Union[Any, Tuple[Any, Path]]:
        result = super().__call__(path, *args, **kwds)
        if self._add_path:
            return result, path
        return result


class ParquetRead(FileRead):
    def __init__(self, *args, **kwds) -> None:
        super().__init__(self._fn, *args, **kwds)

    def _fn(self, path: Path, *args, **kwds) -> pd.DataFrame:
        return pd.read_parquet(path, *args, **kwds)


class ParquetMetaDataRead(FileRead):
    def __init__(self, *args, **kwds) -> None:
        super().__init__(self._fn, *args, **kwds)

    def _fn(self, path: Path, *args, **kwds) -> pq.FileMetaData:
        return pq.read_metadata(path, *args, **kwds)


class MultiRead:
    def __init__(self, read: Read, *args, **kwds) -> None:
        self._read = read
        self._args = args
        self._kwds = kwds

    def __call__(self, paths: List[Path], *args, **kwds) -> List[Any]:
        return [self._read(
            path, *self._args, *args, **self._kwds, **kwds
            ) for path in paths]


def find_paths(
    parent: Union[str, Path],
    pattern: str = '*',
    recursive: bool = False
    ) -> Union[List[Path], List[List[Path]]]:

    if isinstance(parent, str):
        parent = Path(parent)
    if recursive:
        paths = [p for p in parent.rglob(pattern) if p.is_file()]
        result = []
        for parent in {p.parent for p in paths}:
            result.append([p for p in paths if p.parent == parent])
        return result
    else:
        return [p for p in parent.glob(pattern) if p.is_file()]