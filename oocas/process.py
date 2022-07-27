from typing import Callable, List, Any
from tqdm.auto import tqdm
from datetime import datetime


class Process:
    def __init__(self,
        read: Callable = lambda x: x,
        transform: Callable = lambda x: x,
        write: Callable = lambda x, _: x,
        progress_bar=True,
        verbose: bool = False
        ) -> None:

        self._read = read
        self._transform = transform
        self._write = write
        self._verbose = verbose
        self._tqdm = tqdm if progress_bar else lambda x: x

    def __call__(self, data) -> List[Any]:
        return self._fn(data)

    def _fn(self, paths) -> List[Any]:
        results = []
        for path in self._tqdm(paths):
            if self._verbose:
                print(f"{datetime.now().strftime('%H:%M:%S')}   {path}")
            data = self._read(path)
            data = self._transform(data)
            results.append(self._write(data, path))
        return results