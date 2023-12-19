import asyncio

from src.common import bot, dp
from src.handlers import catalog_router, menu_router, payment_router, profile_router


async def main():
    dp.include_router(menu_router)
    dp.include_router(profile_router)
    dp.include_router(payment_router)
    dp.include_router(catalog_router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
