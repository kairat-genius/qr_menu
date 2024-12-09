from app.settings import DATABASE
import os

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

# Ініціалізація асинхроного підключення до БД
engine = create_async_engine(os.environ.get("DATABASE_URL", DATABASE))

