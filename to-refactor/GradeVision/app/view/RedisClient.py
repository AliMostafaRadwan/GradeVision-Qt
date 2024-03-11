import redis


class RedisClient:
    def __init__(self):
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)

    def set(self, key, value):
        self.redis_client.set(key, value)

    def get(self, key):
        return self.redis_client.get(key).decode('utf-8')