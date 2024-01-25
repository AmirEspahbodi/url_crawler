import redis

from app.core.config.database import RedisConfig

redis = redis.from_url(
    url=f"redis://{RedisConfig.REDIS_HOST}:{RedisConfig.REDIS_PORT}",
    decode_responses=True,
)
