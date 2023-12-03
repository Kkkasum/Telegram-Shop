import asyncio

from src.common import bot, dp
from src.handlers import menu_router, profile_router, payment_router, catalog_router


async def main():
    dp.include_router(menu_router)
    dp.include_router(profile_router)
    dp.include_router(payment_router)
    dp.include_router(catalog_router)

    await dp.start_polling(bot)


# run long-polling
if __name__ == '__main__':
    asyncio.run(main())
