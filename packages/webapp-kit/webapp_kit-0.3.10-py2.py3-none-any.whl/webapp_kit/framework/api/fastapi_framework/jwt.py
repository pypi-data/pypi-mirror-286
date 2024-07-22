from datetime import datetime, timedelta
from typing import NewType

from fastapi import Depends, Cookie
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt, JWTError

from webapp_kit.framework.api.fastapi_framework.exceptions import UnauthorizedException, ExceptionDetail

AccessToken = NewType("AccessToken", str)
RefreshToken = NewType("RefreshToken", str)


class JWTTokens:
    def __init__(self, secret_key: str,
                 algorithm: str = "HS256"):
        self._secret_key = secret_key
        self._algorithm = algorithm

    def tokens(self, data: dict, access_token_expiration: timedelta, refresh_token_expiration: timedelta) -> tuple[
        AccessToken, RefreshToken]:
        access_token_payload = data.copy()
        refresh_token_payload = data.copy()

        access_token_expire = datetime.utcnow() + access_token_expiration
        refresh_token_expire = datetime.utcnow() + refresh_token_expiration

        access_token_payload.update({"exp": access_token_expire})
        refresh_token_payload.update({"exp": refresh_token_expire, "refresh": True})

        access_token = jwt.encode(
            access_token_payload, self._secret_key, algorithm=self._algorithm
        )

        refresh_token = jwt.encode(
            refresh_token_payload, self._secret_key, algorithm=self._algorithm
        )

        return AccessToken(access_token), RefreshToken(refresh_token)

    def decoded_access_token(self, token: str) -> dict:
        try:
            decoded_token = jwt.decode(
                token, self._secret_key, algorithms=[self._algorithm]
            )
            return decoded_token
        except JWTError:
            raise UnauthorizedException(detail=[ExceptionDetail(detail="Invalid token or expired token")])


def token_from_header(
    token: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False)),
) -> str | None:
    if token is None:
        return None
    return token.credentials


def token_from_cookie(
    cookie_token: str = Cookie(None, alias="Authorization")
) -> str | None:
    if cookie_token is None:
        return None
    split_token = cookie_token.split()
    if len(split_token) != 2 or split_token[0] != "Bearer":
        raise UnauthorizedException(detail=[ExceptionDetail(detail="Invalid token")])

    return split_token[1]
