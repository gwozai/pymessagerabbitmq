import time
import redis


class AccessLimit:
    def __init__(self, limit=3, per_seconds=300, host='1.15.7.2', port=6379, db=0, password="sY38KEspDNZjptN6"):
        self.redis_conn = self.connect_to_redis(host, port, db, password)
        self.limit = limit
        self.per_seconds = per_seconds

    def connect_to_redis(self, host, port, db, password):
        try:
            pool = redis.ConnectionPool(host=host, port=port, db=db, password=password)
            r = redis.Redis(connection_pool=pool)
            r.ping()
            print("成功连接到Redis数据库.")
            return r
        except Exception as e:
            print(f"无法连接到Redis: {e}")
            return None

    def get_value(self, key):
        now = int(time.time())
        timestamps_key = f"{key}_timestamps"
        timestamps = self.redis_conn.lrange(timestamps_key, 0, -1)

        if len(timestamps) >= self.limit and now - int(timestamps[0].decode()) < self.per_seconds:
            print(
                f"在{time.ctime(now)}，尝试访问键'{key}'被拒绝，因为在过去的{self.per_seconds}秒内已达到访问上限{self.limit}次。")
            return False
        else:
            if len(timestamps) >= self.limit:
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
    access_limit = AccessLimit(limit=1, per_seconds=10)

    key = 'test_11ke11asdfy11111'
    for i in range(6):
        print(f"\n第{i + 1}次尝试访问...")
        print(access_limit.get_value(key))