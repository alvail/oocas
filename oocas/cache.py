from typing import Any, Callable, Union
import pandas as pd


class Cache:
    def __init__(self,
        fn: Callable = lambda x: x,
        data: Any = None,
        *args, **kwds) -> None:

        self._fn = fn
        self.data = data
        self._args = args
        self._kwds = kwds

    def __call__(self, data: Any, *args, **kwds) -> None:
        self.data = self._fn(data, *self._args, *args, **self._kwds, **kwds)


class IndexCache(Cache):
    def __init__(self, lookback: int) -> None:
        super().__init__(
            self._fn
        )
        self.lookback = lookback

    def _fn(self, data: pd.DataFrame, lookback: int = None) -> pd.DataFrame:
        if not lookback:
            lookback = self.lookback
        df = pd.concat([self.data, data], axis=0)
        cutoff = len(df) - lookback
        return df[cutoff:].copy()


class TimeIndexCache(Cache):
    def __init__(self, lookback: Union[str, pd.Timedelta, int]) -> None:
        super().__init__(
            self._fn
        )
        self.lookback = pd.Timedelta(lookback)

    def _fn(self, data: pd.DataFrame, lookback: pd.Timedelta = None) -> pd.DataFrame:
        if not lookback:
            lookback = self.lookback
        df = pd.concat([self.data, data], axis=0)
        cutoff = df.index[-1] - lookback
        return df[cutoff:].copy()