class Cache:

    def __init__(self, redis_instance):
        self.redis = redis_instance

    def ttl(self, ttl=3600):
        def enable(func):
            def func_wrapper(*args, **kwargs):
                target_key = ":".join(["CACHE", func.__name__, *args, str(kwargs)])
                target_key = hash(target_key)
                a = self.redis.get(target_key)
                if a:
                    return a
                else:
                    result = func(*args, **kwargs)
                    self.redis.set(target_key, result, ttl)
                    return result
            return func_wrapper
        return enable


if __name__ == '__main__':
    from datetime import datetime
    from time import sleep
    from redis import StrictRedis

    redis = StrictRedis(decode_responses=True)
    cache = Cache(redis)


    @cache.ttl(300)
    def pseudo_calc():
        sleep(1)
        print("Compute in progress")
        return str(datetime.now())


    while True:
        print(pseudo_calc())
        sleep(.1)
