from typing import Any

from fastapi import status


class AppException(Exception):
    """业务异常。

    携带统一响应所需的状态码、业务码和错误明细。
    """

    def __init__(
        self,
        message: str,
        *,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        code: int | None = None,
        errors: list[dict[str, Any]] | None = None,
    ) -> None:
        self.message = message
        self.status_code = status_code
        self.code = code if code is not None else status_code
        self.errors = errors
        super().__init__(message)
