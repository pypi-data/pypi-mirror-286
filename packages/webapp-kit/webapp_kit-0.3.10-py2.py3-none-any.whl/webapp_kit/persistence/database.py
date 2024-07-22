from contextlib import contextmanager, asynccontextmanager
from functools import cached_property
from typing import Type, Generator, AsyncGenerator

from sqlalchemy import create_engine, Engine
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker, Session, declarative_base


class DatabaseConnection:
    def __init__(self, db_dsn: str, engine_cls: Type[Engine | AsyncEngine] = Engine, echo: bool = False):
        self._db_dsn = db_dsn
        self._engine_cls = engine_cls
        self._echo = echo

    @cached_property
    def engine(self) -> Engine | AsyncEngine:
        if self._engine_cls == AsyncEngine:
            return create_async_engine(self._db_dsn, echo=self._echo)
        return create_engine(self._db_dsn, echo=self._echo)

    @cached_property
    def session(self) -> [sessionmaker | async_sessionmaker]:
        session = sessionmaker
        if self._engine_cls == AsyncEngine:
            session = async_sessionmaker
        return session(self.engine, expire_on_commit=False, autoflush=False)

    @contextmanager
    def connection(self) -> Generator[Session, None, None]:
        db = self.session()
        try:
            yield db
        finally:
            db.close()

    @asynccontextmanager
    async def async_connection(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session() as session:
            async with session.begin():
                yield session


Base = declarative_base()