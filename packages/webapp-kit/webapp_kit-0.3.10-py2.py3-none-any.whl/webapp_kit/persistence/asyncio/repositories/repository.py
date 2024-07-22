from typing import Union

from sqlalchemy import Select, Delete, Insert, Update, Result, CursorResult
from sqlalchemy.ext.asyncio import AsyncSession

from webapp_kit.persistence.entities import BaseDBEntity
from webapp_kit.persistence.repository import BaseRepository


class BaseAsyncRepository(BaseRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(db=db)

    async def exec_query(
        self, query: Union[Select, Delete, Insert, Update]
    ) -> Result | CursorResult:
        return await self.db.execute(query)

    async def save(self, model: BaseDBEntity) -> None:
        self.db.add(model)
        await self.db.flush()

    async def save_all(self, models: list[BaseDBEntity]) -> None:
        self.db.add_all(models)
        await self.db.flush()

    async def delete_by_ids(self, ids: list[str]) -> None:
        await self.exec_query(
            query=self.delete(self.model).where(self.model.id.in_(ids))
        )
        await self.db.flush()