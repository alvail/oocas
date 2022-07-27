from typing import Any, Callable, Union
import oocas as oc


class Transform:
    def __init__(self, fn: Callable, *args, **kwds) -> None:
        self._fn = fn
        self._args = args
        self._kwds = kwds

    def __call__(self, data: Any, *args, **kwds) -> Any:
        return self._fn(data, *self._args, *args, **self._kwds, **kwds)


class CacheTransform(Transform):
    def __init__(self, fn: Callable, cache: Union[oc.Cache, Any] = oc.Cache(), *args, **kwds) -> None:
        super().__init__(fn, *args, **kwds)
        if not isinstance(cache, oc.Cache):
            self._cache = oc.Cache(data=cache)
        else:
            self._cache = cache

    def __call__(self, data: Any, *args, **kwds) -> Any:
        return super().__call__(data, self._cache, *args, **kwds)
