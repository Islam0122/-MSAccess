
import os
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from .model import Base


# Создаем асинхронный engine для подключения к базе данных
# Строка подключения берется из переменной окружения DB_LITE
# echo=True — выводит все SQL запросы в консоль (удобно для разработки)
# in .env --> DB_LITE=sqlite+aiosqlite:///db.sqlite3
engine = create_async_engine(os.getenv('DB_LITE'), echo=True)


# Создаем фабрику сессий (session maker)
# Через нее будут создаваться новые сессии для работы с базой данных
session_maker = async_sessionmaker(
    bind=engine,                 # привязываем к нашему engine
    class_=AsyncSession,         # используем асинхронную сессию
    expire_on_commit=False       # объекты не "очищаются" после commit
)


# Функция для создания всех таблиц в базе данных
# Берет все модели, которые наследуются от Base
# и создает соответствующие таблицы
async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Функция для удаления всех таблиц из базы данных
# Используется обычно только при тестировании или полной очистке базы
async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
