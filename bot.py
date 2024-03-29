import asyncio

from src.common import bot, dp
from src.handlers import include_routers


async def main():
    include_routers(dp)

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
