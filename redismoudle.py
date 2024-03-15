import redis
import time

class SingletonRedis:
    _instances = {}

    def __init__(self, host='localhost', port=6379, db=0, password=None):
        if type(self) not in self._instances:
            try:
                pool = redis.ConnectionPool(host=host, port=port, db=db, password=password)
                self.redis_conn = redis.Redis(connection_pool=pool)
                print("成功连接到Redis数据库.")
            except (redis.RedisError, Exception) as e:
                print(f"无法连接到Redis: {e}")
                self.redis_conn = None
            self._instances[type(self)] = self

    @classmethod
    def get_instance(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls(*args, **kwargs)
        return cls._instances[cls].redis_conn


class AccessLimit:
    def __init__(self, host='1.15.7.2', port=6379, db=0, password="sY38KEspDNZjptN6"):
        self.redis_conn = SingletonRedis.get_instance(host, port, db, password)


    def get_value(self, key,limit=5,per_seconds=10):
        now = int(time.time())
        timestamps_key = f"{key}_timestamps"
        timestamps = self.redis_conn.lrange(timestamps_key, 0, -1)

        if len(timestamps) >= limit and now - int(timestamps[0].decode()) < per_seconds:
            print(
                f"在{time.ctime(now)}，尝试访问键'{key}'被拒绝，因为在过去的{per_seconds}秒内已达到访问上限{limit}次。返回False")
            return False
        else:
            if len(timestamps) >= limit:
                self.redis_conn.lpop(timestamps_key)
            self.redis_conn.rpush(timestamps_key, now)

            value = self.redis_conn.get(key)
            # if value is not None:
            #     print(
            #         f"在{time.ctime(now)}，成功访问到键'{key}'，其值为：{value.decode()}。这是在最近{self.per_seconds}秒内的第{len(timestamps) + 1}次访问。")
            # else:
            #     print(f"在{time.ctime(now)}，键'{key}'的值不存在。尝试访问失败。")
            return True


if __name__ == "__main__":
    access_limit = AccessLimit()

    key = 'test_ke1y'
    for i in range(6):
        print(f"\n第{i + 1}次尝试访问...")
        print(access_limit.get_value(key, 3 ,6))