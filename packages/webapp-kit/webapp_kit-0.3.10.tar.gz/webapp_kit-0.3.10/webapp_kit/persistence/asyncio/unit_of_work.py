from __future__ import annotations

from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, Callable, Type, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

from webapp_kit.persistence.database import DatabaseConnection


class AsyncUnitOfWork:
    session: AsyncSession

    def __init__(self, session: AsyncSession):
        self.session = session

    async def __aenter__(self) -> AsyncUnitOfWork:
        return self

    async def rollback(self) -> None:
        await self.session.rollback()

    async def commit(self) -> None:
        await self.session.commit()

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        if exc_type is not None:
            await self.rollback()
        else:
            await self.commit()
        await self.session.close()


T = TypeVar("T", bound=AsyncUnitOfWork)


@asynccontextmanager
async def unit_of_work(cls: Type[T], connection: DatabaseConnection) -> Callable[
    [], AsyncGenerator[T, None]]:
    async with connection.async_connection() as session:
        async with cls(session=session) as uow:
            yield uow
