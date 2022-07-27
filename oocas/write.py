from typing import Any, Callable, Tuple, Union, List
import pandas as pd
from pathlib import Path


class Write:
    def __init__(self, fn: Callable, *args, **kwds) -> None:
        self._fn = fn
        self._args = args
        self._kwds = kwds

    def __call__(self, data: Any, path: Any, *args, **kwds) -> Any:
        return self._fn(data, path, *self._args, *args, **self._kwds, **kwds)


class FileWrite(Write):
    def __init__(self,
        fn: Callable = lambda _, path: path,
        path_transform: Union[Callable[[Path], Path], None] = None,
        path_part_replace: Union[Tuple[str, str], None] = None,
        name_transform: Union[Callable[[str], str], None] = None,
        suffix: Union[str, None] = None,
        mkdirs: bool = False,
        overwrite: bool = False,
        add_result: bool = False,
        *args,
        **kwds) -> None:

        self._path_transform = path_transform
        self._path_part_replace = path_part_replace
        self._name_transform = name_transform
        self._suffix = suffix
        self._mkdirs = mkdirs
        self._overwrite = overwrite
        self._add_result = add_result
        super().__init__(fn, *args, **kwds)

    def __call__(self, data: Any, path: Path, *args, **kwds) -> Path:
        if self._path_transform:
            path = self._path_transform(path)
        if self._path_part_replace:
            path = replace_path_part(path, *self._path_part_replace)
        if self._name_transform:
            path = path.with_stem(self._name_transform(path.stem))
        if self._suffix:
            path = path.with_suffix(self._suffix)
        if not self._overwrite:
            check_exists(path)
        if self._mkdirs:
            mkdirs(path)
        result = super().__call__(data, path, *args, **kwds)
        if self._add_result:
            return path, result
        return path


class ParquetWrite(FileWrite):
    def __init__(self, suffix='.parquet', *args, **kwds) -> None:
        super().__init__(self._fn, suffix=suffix, *args, **kwds)

    def _fn(self, data: pd.DataFrame, path: Path, *args, **kwds) -> None:
        data.to_parquet(path, *args, **kwds)


class MultiWrite:
    def __init__(self, write: Write, *args, **kwds) -> List[Any]:
        self._write = write
        self._args = args
        self._kwds = kwds
    
    def __call__(self, data: List[Any], paths: List[Path], *args, **kwds) -> Any:
        return [self._write(
            x, path, *self._args, *args, *self._kwds, **kwds
            ) for x, path in zip(data, paths)]


def mkdirs(path: Path) -> None:
        dir_path = Path(*path.parts[:-1])
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)


def check_exists(path: Path) -> None:
    if path.exists():
        raise FileExistsError(
            f"File {path} already exists")


def replace_path_part(path: Path, from_part: str, to_part: str) -> Path:
    idx = path.parts.index(from_part)
    path = Path(
        *path.parts[:idx],
        to_part,
        *path.parts[idx + 1:])
    return path