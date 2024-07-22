from typing import TypedDict, Optional, Iterable

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse


class ExceptionDetail(TypedDict, total=False):
    detail: str
    field: Optional[str]
    type: Optional[str]


class APIException(HTTPException):
    detail: Iterable[ExceptionDetail] = ()

    def __init__(self, status_code: int, detail: Iterable[ExceptionDetail] = ()):
        super().__init__(status_code, detail=detail)


class NotFoundException(APIException):
    def __init__(self, detail: Iterable[ExceptionDetail] = ()) -> None:
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class UnauthorizedException(APIException):
    def __init__(self, detail: Iterable[ExceptionDetail] = ()) -> None:
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class BadRequestException(APIException):
    def __init__(self, detail: Iterable[ExceptionDetail] = ()) -> None:
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class PermissionDeniedException(APIException):
    def __init__(self, detail: Iterable[ExceptionDetail] = ()) -> None:
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


class ThrottleException(APIException):
    def __init__(self, detail: Iterable[ExceptionDetail] = ()) -> None:
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


def validation_exception_handler(request: Request, exc: APIException) -> JSONResponse:
    errors_list = []
    for error in exc.detail:
        errors_list.append(
            {
                "loc": error.get("field"),
                "msg": f"{error.get('detail')}",
                "type": error.get("type"),
            }
        )

    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": jsonable_encoder(errors_list)},
    )
