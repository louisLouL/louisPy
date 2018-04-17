class Cache:

    def __init__(self, redis_instance, cache_ttl=3600):
        self.redis = redis_instance
        self.cache_ttl = cache_ttl

    def enable(self, func):
        def func_wrapper(*args, **kwargs):
            target_key = ":".join(["CACHE", func.__name__, *args, str(kwargs)])
            target_key = hash(target_key)
            a = self.redis.get(target_key)
            if a:
                return a
            else:
                result = func(*args, **kwargs)
                self.redis.set(target_key, result, self.cache_ttl)
                return result

        return func_wrapper


if __name__ == '__main__':
    from datetime import datetime
    from time import sleep
    from redis import StrictRedis

    redis = StrictRedis(decode_responses=True)
    cache = Cache(redis)


    @cache.enable
    def time():
        return str(datetime.now())


    while True:
        print(time())
        sleep(1)
