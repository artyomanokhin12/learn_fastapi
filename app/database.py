from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import Config, load_config

config: Config = load_config()

DB_USER = config.host_config.DB_USER
DB_PASS = config.host_config.DB_PASS
DB_HOST = config.host_config.DB_HOST
DB_PORT = config.host_config.DB_PORT
DB_NAME = config.host_config.DB_NAME


DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_async_engine(DATABASE_URL)

async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

class Base(DeclarativeBase):
    pass


print(DATABASE_URL)
