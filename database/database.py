import os
import redis

database = redis.Redis(
    host=os.getenv("REDIS_IP"),
    port=os.getenv("REDIS_PORT"),
    password=os.getenv("REDIS_PSWD"),
)
