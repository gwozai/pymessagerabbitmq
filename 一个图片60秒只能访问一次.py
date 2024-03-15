import redis


class AccessLimit:
    def __init__(self, host='1.15.7.2', port=6379, db=0, password="sY38KEspDNZjptN6"):
        self.redis_conn = self.connect_to_redis(host, port, db, password)

    def connect_to_redis(self, host, port, db, password):
        try:
            pool = redis.ConnectionPool(host=host, port=port, db=db, password=password)
            r = redis.Redis(connection_pool=pool)
            r.ping()  # 尝试ping操作确认连接正常
            return r
        except Exception as e:
            print(f"Unable to connect to Redis: {e}")
            return None

    def get_value(self, key):
        lock_key = f"{key}_lock"
        if self.redis_conn.get(lock_key) is None:
            value = self.redis_conn.get(key)
            if value is not None:
                print(f"The value of {key} is {value.decode()}")
                self.redis_conn.set(lock_key, 'True', ex=60)  # 设定 ${key}_lock 为 True，并在60秒后过期。
            else:
                print(f"The key {key} does not exist.")
        else:
            print(f"The key {key} has been accessed within the past minute.")

if __name__ == "__main__":
    access_limit = AccessLimit()

    key = 'test_key'
    access_limit.redis_conn.set(key, 'test_value')  # 假设我先设定了一个键值对

    access_limit.get_value(key)  # 第一次访问，会返回这个值，并将其对应的 ${key}_lock 设 为 True。
    access_limit.get_value(key)  # 这次访问，会告知这个键在一分钟内被访问过。