from aiogram import Dispatcher

from ._catalog import router as catalog_router
from ._menu import router as menu_router
from ._payment import router as payment_router
from ._profile import router as profile_router


def include_routers(dp: Dispatcher) -> None:
    dp.include_routers(
        menu_router,
        profile_router,
        payment_router,
        catalog_router
    )
