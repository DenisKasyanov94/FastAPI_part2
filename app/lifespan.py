from contextlib import asynccontextmanager
from app.database import create_tables

@asynccontextmanager
async def lifespan(app):
    # При запуске создаем таблицы
    create_tables()
    yield