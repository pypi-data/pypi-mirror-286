from typing import Type, Union, Any, Awaitable

from sqlalchemy import Result, Select, Delete, Insert, Update, select, delete, update
from sqlalchemy.orm import Session

from webapp_kit.persistence.entities import BaseDBEntity
from webapp_kit.persistence.repository import BaseRepository


class BaseSyncRepository(BaseRepository):
    model: Type[BaseDBEntity]
    db: Session

    def __init__(self, db: Session):
        super().__init__(db)

    def exec_query(self, query: Union[Select, Delete, Insert, Update]) -> Result[Any]:
        return self.db.execute(query)

    def save(self, model: BaseDBEntity) -> None:
        self.db.add(model)
        self.db.flush()

    def save_all(self, models: list[BaseDBEntity]) -> None | Awaitable:
        self.db.add_all(models)
        self.db.flush()
        return

    def _select(self, *args: Any) -> Select:
        return select(*args)

    def select(self, *args: Any) -> Select:
        return self._select(*args)

    def delete(self, *args: Any) -> Delete:
        return delete(*args)

    def update(self, *args: Any) -> Update:
        return update(*args)

    def bulk_save(self, objs: list[BaseDBEntity]) -> None:
        self.db.add_all(objs)
        self.db.flush()