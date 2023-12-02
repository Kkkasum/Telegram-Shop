from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage


from ._config import config


bot = Bot(token=config.BOT_TOKEN, parse_mode='HTML')
storage = MemoryStorage
dp = Dispatcher()
