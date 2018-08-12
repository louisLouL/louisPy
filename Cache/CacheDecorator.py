from io import StringIO
import pandas as pd
import json
import warnings
from Cache.SimpleContainer import SimpleContainer
import functools


class Cache:

    def __init__(self, redis_instance=None):
        if not redis_instance:
            self.cache_container = SimpleContainer()
            warnings.warn("No Redis instance Specified, ttl feature disabled, cache will stay in memory forever.")
        else:
            if type(redis_instance.echo("hello")) == str:
                self.cache_container = redis_instance
            else:
                raise AttributeError(
                    "Redis instance's decode_responses must be set True. Use StrictRedis(..., decode_responses=True)")

    def ttl(self, ttl=None):
        def enable(func):
            @functools.wraps(func)
            def func_wrapper(*args, **kwargs):
                target_key = ":".join(
                    ["Cache", str(":".join([func.__name__, *[str(i) for i in args], str(kwargs)]))])
                a = self.cache_container.get(target_key)
                if a:
                    return a
                else:
                    result = func(*args, **kwargs)
                    self.cache_container.set(target_key, result, ttl)
                    return result

            return func_wrapper

        return enable

    def _ser_df(self, func):
        @functools.wraps(func)
        def func_wrapper(*args, **kwargs):
            return func(*args, **kwargs).to_csv(index=False)

        return func_wrapper

    def _de_ser_df(self, func):
        @functools.wraps(func)
        def func_wrapper(*args, **kwargs):
            return pd.read_csv(StringIO(func(*args, **kwargs)))

        return func_wrapper

    def df(self, ttl=None):
        def deco(func):
            for dec in [self._ser_df, self.ttl(ttl), self._de_ser_df]:
                func = dec(func)
            return func

        return deco

    def _ser_number(self, func):
        @functools.wraps(func)
        def func_wrapper(*args, **kwargs):
            return str(func(*args, **kwargs))

        return func_wrapper

    def _de_ser_int(self, func):
        @functools.wraps(func)
        def func_wrapper(*args, **kwargs):
            return int(func(*args, **kwargs))

        return func_wrapper

    def _de_ser_float(self, func):

        @functools.wraps(func)
        def func_wrapper(*args, **kwargs):
            return float(func(*args, **kwargs))

        return func_wrapper

    def int(self, ttl=None):

        def deco(func):
            for dec in [self._ser_number, self.ttl(ttl), self._de_ser_int]:
                func = dec(func)
            return func

        return deco

    def float(self, ttl=None):
        def deco(func):
            for dec in [self._ser_number, self.ttl(ttl), self._de_ser_float]:
                func = dec(func)
            return func

        return deco

    def _ser_dict(self, func):
        @functools.wraps(func)
        def func_wrapper(*args, **kwargs):
            return json.dumps(func(*args, **kwargs))

        return func_wrapper

    def _de_ser_dict(self, func):
        @functools.wraps(func)
        def func_wrapper(*args, **kwargs):
            return json.loads(func(*args, **kwargs))

        return func_wrapper

    def dict(self, ttl=None):
        def deco(func):
            for dec in [self._ser_dict, self.ttl(ttl), self._de_ser_dict]:
                func = dec(func)
            return func

        return deco

    def list(self, ttl=None):
        def deco(func):
            for dec in [self._ser_dict, self.ttl(ttl), self._de_ser_dict]:
                func = dec(func)
            return func

        return deco

    def _de_ser_json(self, func):
        @functools.wraps(func)
        def func_wrapper(*args, **kwargs):
            return json.loads(func(*args, **kwargs))

        return func_wrapper

    def _ser_json(self, func):
        @functools.wraps(func)
        def func_wrapper(*args, **kwargs):
            return json.dumps(json.loads(func(*args, **kwargs)))

        return func_wrapper

    def json(self, ttl=None):
        def deco(func):
            for dec in [self._ser_json, self.ttl(ttl), self._de_ser_json]:
                func = dec(func)
            return func

        return deco


if __name__ == '__main__':
    pass
