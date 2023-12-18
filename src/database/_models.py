from datetime import datetime

from sqlalchemy import BIGINT, String, Float, TIMESTAMP, func
from sqlalchemy.orm import declarative_base, mapped_column, Mapped


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    username: Mapped[str] = mapped_column(String(32))
    registration_date: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())
    balance: Mapped[float | None] = mapped_column(Float)


class Item(Base):
    __tablename__ = 'items'

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    item_name: Mapped[str] = mapped_column(String(32))
    price: Mapped[float] = mapped_column(Float)
    amount: Mapped[int | None] = mapped_column(BIGINT)
    category_id: Mapped[int] = mapped_column(BIGINT)
    description: Mapped[str | None] = mapped_column(String(128))


class Order(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    order_type: Mapped[str] = mapped_column(String(32))
    user_id: Mapped[str] = mapped_column(BIGINT)
    item_name: Mapped[str] = mapped_column(String(32))
    order_date: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())
    price: Mapped[float] = mapped_column(Float)


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    category: Mapped[str] = mapped_column(String(64))
