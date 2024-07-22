from abc import abstractmethod
from functools import cached_property
from typing import Any

from fastapi import Depends

from webapp_kit.framework.api.fastapi_framework.exceptions import UnauthorizedException, ExceptionDetail
from webapp_kit.framework.api.fastapi_framework.jwt import token_from_header, token_from_cookie
from webapp_kit.persistence.asyncio import unit_of_work as async_uow
from webapp_kit.persistence.asyncio.unit_of_work import AsyncUnitOfWork
from webapp_kit.persistence.sync import unit_of_work as sync_uow
from webapp_kit.persistence.sync.unit_of_work import SyncUnitOfWork


class BaseHandler:
    pass


class BaseAuthenticationHandler(BaseHandler):
    token: str = Depends(token_from_header)
    cookie_token: str = Depends(token_from_cookie)

    @cached_property
    def auth_token(self) -> str:
        if self.token is None and self.cookie_token is None:
            raise UnauthorizedException(
                detail=[ExceptionDetail(detail="Bad credentials")]
            )
        return self.token or self.cookie_token


class AsyncAuthenticationHandler(BaseAuthenticationHandler):
    uow: AsyncUnitOfWork = Depends(async_uow.unit_of_work)

    @property
    @abstractmethod
    async def user(self) -> Any:
        raise NotImplementedError


class AuthenticationHandler(BaseAuthenticationHandler):
    uow: SyncUnitOfWork = Depends(sync_uow.unit_of_work)

    @property
    @abstractmethod
    def user(self) -> Any:
        raise NotImplementedError
