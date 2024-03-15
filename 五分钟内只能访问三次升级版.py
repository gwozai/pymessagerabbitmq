import time
import redis

class AccessLimit:
    def __init__(self, host='1.15.7.2', port=6379, db=0, password="sY38KEspDNZjptN6"):
        self.redis_conn = self.connect_to_redis(host, port, db, password)

    def connect_to_redis(self, host, port, db, password):
        try:
            pool = redis.ConnectionPool(host=host, port=port, db=db, password=password)
            r = redis.Redis(connection_pool=pool)
            r.ping()  # 尝试ping看是否连接正常
            return r
        except Exception as e:
            print(f"无法连接到Redis: {e}")
            return None

    def get_value(self, key):
        now = int(time.time())
        timestamps_key = f"{key}_timestamps"
        timestamps = self.redis_conn.lrange(timestamps_key, 0, -1)

        if len(timestamps) >= 3 and now - int(timestamps[0].decode()) < 300:
            return False
        else:
            if len(timestamps) >= 3:
                self.redis_conn.lpop(timestamps_key)  # 移除列表最旧的时间戳
            self.redis_conn.rpush(timestamps_key, now)  # 将当前时间戳添加到列表尾部
            value = self.redis_conn.get(key)
            if value is not None:
                print(f"{key}的值是：{value.decode()}")
            else:
                print(f"键{key}不存在。")
            return True

if __name__ == "__main__":
    access_limit = AccessLimit()

    key = '11'

    # 如果在5分钟内连续访问4次
    print(access_limit.get_value(key))  # 第一次访问，正常返回
    print(access_limit.get_value(key))  # 第二次访问，正常返回
    print(access_limit.get_value(key))  # 第三次访问，正常返回
    print(access_limit.get_value(key))  # 第四次访问返回False，表示访问过于频繁