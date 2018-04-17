# louisPy
A collection of handy python utilities developed by myself over time.
## CacheDecorator
Given a function and a combination of args and kwargs, the function will cache result into redis or simple dictionary(if you don't have redis instance)

When it is called the second time, it will return the result from cache.

### Quick start
#### Initialize
```python
from Cache import Cache

### Comment this section if you don't have redis instance ###
from redis import StrictRedis
redis = StrictRedis(decode_responses=True)
cache = Cache(redis)

###### Comment this section if you are using redis ##########
# cache = Cache()
```
#### Example1 : Cache string return

```python
# set cache's time to live to 300 seconds (expires in 300 seconds)
@cache.ttl(300)
def pseudo_calc():
    sleep(1)
    print("Computation in progress")
    return str(datetime.now())

# The first call takes 1 seconds, after that every call is immediately returned from cache.
for i in range(10):
    print(pseudo_calc())
```
#### Example 2: Cache Pandas Dataframe
```python
# Set cache's time to live to 300 seconds (expires in 300 seconds)
# If left blank, e.g. @cache.df(), cache will stay forever. Don't recommended.
@cache.df(300)
def return_a_df(*args, **kwargs):
    sleep(1)
    print("Computation in progress")
    return pd.DataFrame({"time": [str(datetime.now()) for _ in range(5)], "foo": list(range(5))})


for i in range(5):
    print(return_a_df(1, 5))
```

#### Example 3: Cache dict
```python

@cache.dict(60)
def return_a_dict(*args, **kwargs):
    sleep(1)
    print("Computation in progress")
    return {"now": str(datetime.now())}


for i in range(5):
    print(return_a_dict())
```

#### Example 4: Cache float number
```python
@cache.float(60)
def return_a_float(*args, **kwargs):
    return random()


for i in range(5):
    print(return_a_float())
```