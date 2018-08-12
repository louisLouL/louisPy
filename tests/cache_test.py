from redis import StrictRedis
from random import random, randint
import pandas as pd
from redis_dec import Cache
import json


redis = StrictRedis(decode_responses=True)
cache = Cache(redis)
cache_time = 3600
cache.delete_cache()


@cache.int(cache_time)
def func_int(a, b=0):
    return a + b + randint(0, 10)


def test_int():
    prev = func_int(1, 2)
    assert func_int(1, 2) == prev
    assert func_int(1, 3) != prev


@cache.float(cache_time)
def func_float(a, b=0.0):
    return a + b + random()


def test_float():
    prev = func_float(1.1, b=2.1)
    assert func_float(1.1, b=2.1) == prev
    assert func_float(1.1, b=3.1) != prev


@cache.df(cache_time)
def func_df(a, b=0.0):
    rows = 12
    a = [a] * rows
    b = [b] * rows
    tmp = [random() for _ in range(rows)]
    return pd.DataFrame({"a": a, "b": b, "foo": tmp})


def test_df():
    prev = func_df(1.1, b=2.1)
    assert (prev == func_df(1.1, b=2.1)).all().all()
    assert not (prev == func_df(1.1, b=3.1)).all().all()


@cache.list(cache_time)
def func_list(a, b=0):
    return [a, b, random()]


def test_list():
    prev = func_list(1, 2)
    assert func_list(1, 2) == prev
    assert func_list(1, 3) != prev


@cache.dict(cache_time)
def func_dict(a, b=0):
    return {
        "a": a,
        "b": b,
        "foo": random()
    }


def test_dict():
    prev = func_dict(1, 2)
    assert func_dict(1, 2) == prev
    assert func_dict(1, 3) != prev

@cache.json(cache_time)
def func_json(a, b=0):
    return json.dumps({
        "a": a,
        "b": b,
        "foo": random()
    })

def test_json():
    prev = func_json(1, 2)
    assert func_json(1, 2) == prev
    assert func_json(1, 3) != prev

def test_delete_single_cache():
    prev = func_json(2, b=3)
    assert func_json(2, b=3) == prev
    cache.delete_cache(func_json, 2, b=3)
    assert func_json(2, b=3) != prev

def test_delete_cache_by_func():
    prev = func_json(2, b=3)
    assert func_json(2, b=3) == prev
    cache.delete_cache(func_json)
    assert func_json(2, b=3) != prev

def test_delete_all_cache():
    prev = func_json(2, b=3)
    assert func_json(2, b=3) == prev
    cache.delete_cache()
    assert func_json(2, b=3) != prev
