from abc import ABC, abstractmethod
from typing import Type, Union, Awaitable, Any

from sqlalchemy import Select, Delete, Insert, Update, select, delete, update, Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from webapp_kit.persistence.entities import BaseDBEntity

class BaseRepository(ABC):
    model: Type[BaseDBEntity]
    db: AsyncSession|Session

    def __init__(self, db: AsyncSession|Session):
        self.db = db

    @abstractmethod
    def exec_query(
        self, query: Union[Select, Delete, Insert, Update]
    ) -> Result:
        raise NotImplementedError

    @abstractmethod
    def save(self, model: BaseDBEntity) -> None | Awaitable:
        raise NotImplementedError

    @abstractmethod
    def save_all(self, models: list[BaseDBEntity]) -> None | Awaitable:
        raise NotImplementedError

    def _select(self, *args: Any) -> Select:
        return select(*args)

    def select(self, *args: Any) -> Select:
        return self._select(*args)

    def delete(self, *args: Any) -> Delete:
        return delete(*args)

    def delete_by_ids(self, ids: list[str]) -> Union[None, Awaitable]:
        raise NotImplementedError

    def update(self, *args: Any) -> Update:
        return update(*args)