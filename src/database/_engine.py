from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from ..common import DB_URL


engine = create_async_engine(DB_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
