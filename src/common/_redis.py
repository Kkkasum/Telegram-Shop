from redis.asyncio import Redis

from ._config import config

redis = Redis(host=config.REDIS_HOST, port=config.REDIS_PORT)
