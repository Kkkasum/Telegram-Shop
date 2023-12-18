from sqlalchemy import select, insert, update, func

from loguru import logger

from src.common import redis

from ._engine import async_session_maker
from ._models import User, Item, Order, Category


async def add_user(user: dict) -> None:
    res = await redis.get(name=str(user['id']))

    if not res:
        async with async_session_maker() as session:
            query = select(User.id, User.registration_date, User.balance).where(User.id == user['id'])
            result = await session.execute(query)

            if not result.scalar():
                stmt = insert(User)\
                    .values(id=user['id'], username=user['username'], registration_date=func.now(), balance=0)
                await session.execute(stmt)
                await session.commit()

                logger.success(f"User {user['id']} has been registered")

        await redis.set(name=str(user['id']), value=1)


async def add_order(order: dict) -> None:
    async with async_session_maker() as session:
        stmt = insert(Order)\
            .values(
                order_type=order['order_type'],
                user_id=order['user_id'],
                item_name=order['item_name'],
                order_date=order['order_date'],
                price=order['price']
            )
        await session.execute(stmt)
        await session.commit()

        logger.success(f"Order by {order['user_id']} has been completed")


async def get_user(user_id: int) -> dict:
    async with async_session_maker() as session:
        query = select(User.registration_date, User.balance)\
            .where(User.id == user_id)
        result = await session.execute(query)
        result = result.first()

    user = {
        'registration_date': result[0].strftime('%d/%m/%Y'),
        'balance': float(result[1])
    }

    return user


async def get_user_balance(user_id: int) -> float:
    async with async_session_maker() as session:
        query = select(User.balance)\
            .where(User.id == user_id)
        result = await session.execute(query)
        result = result.scalar()

    return result


async def get_categories() -> list:
    async with async_session_maker() as session:
        query = select(Category.id, Category.category)
        result = await session.execute(query)
        result = result.all()

    return result


async def get_items_by_category(category_id: int) -> list:
    async with async_session_maker() as session:
        query = select(Item.id, Item.item_name)\
            .where(Item.category_id == category_id)
        result = await session.execute(query)
        result = result.all()

    return result


async def get_item_by_id(item_id: int) -> dict:
    async with (async_session_maker() as session):
        query = select(Item.item_name, Item.price, Item.description)\
            .where(Item.id == item_id)
        result = await session.execute(query)
        result = result.first()._asdict()

    return result


async def get_user_purchases(user_id: int) -> list:
    async with async_session_maker() as session:
        query = select(Order.item_name, Order.order_date, Order.price)\
            .where(Order.user_id == user_id, Order.order_type != 'refill')
        result = await session.execute(query)
        result = result.all()

    return result


async def update_user_balance(user_id: int, balance: float) -> None:
    async with async_session_maker() as session:
        stmt = update(User)\
            .where(User.id == user_id)\
            .values(balance=balance)
        await session.execute(stmt)
        await session.commit()

        logger.success(f"User {user_id} balance has been updated")
