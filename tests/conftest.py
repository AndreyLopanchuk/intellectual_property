import os
from typing import AsyncGenerator

import pytest
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from httpx import ASGITransport, AsyncClient
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.api.authors.routes import router as authors_router
from app.api.books.routes import router as books_router
from app.api.borrows.routes import router as borrows_router
from app.database.db import db
from app.models.base import Base


if "HOSTNAME" in os.environ:
    DATABASE_URL_TEST: str = "postgresql+asyncpg://admin:admin@testdb/librarytest"
else:
    DATABASE_URL_TEST: str = "postgresql+asyncpg://admin:admin@localhost:5434/librarytest"

test_engine = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)

test_async_session = async_sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Функция создает асинхронную сессию с базой данных
    """
    async with test_async_session() as session:
        yield session


@pytest.fixture(scope="function")
async def test_app() -> FastAPI:
    app = FastAPI(default_response_class=ORJSONResponse)
    app.dependency_overrides[db.session_getter] = override_get_async_session
    app.include_router(router=authors_router, prefix="/authors")
    app.include_router(router=books_router, prefix="/books")
    app.include_router(router=borrows_router, prefix="/borrows")
    yield app


@pytest.fixture(scope="function")
async def test_client(test_app) -> AsyncGenerator[AsyncClient, None]:
    """
    Фикстура создает тестовый клиент
    """
    transport = ASGITransport(app=test_app)
    async with AsyncClient(transport=transport, base_url="http://test") as async_client:
        yield async_client


@pytest.fixture(scope="function")
async def test_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Фикстура создает сессию с базой данных
    """
    async with test_async_session() as session:
        yield session


@pytest.fixture(scope="function", autouse=True)
async def create_db() -> AsyncGenerator:
    """
    Фикстура создает базу данных и очищает ее перед каждым тестом
    """
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
