from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage

from ._config import config
from ._redis import redis

bot = Bot(token=config.BOT_TOKEN, parse_mode='HTML')
storage = RedisStorage(redis=redis)
dp = Dispatcher(storage=storage)
