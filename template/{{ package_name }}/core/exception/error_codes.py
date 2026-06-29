from enum import IntEnum


class ErrorCode(IntEnum):
    """通用错误码。

    0 表示成功；100xxx 为模板内置通用错误码。业务模块可按团队约定扩展
    独立号段，但不要直接复用 HTTP 状态码作为业务码。
    """

    SUCCESS = 0
    BAD_REQUEST = 100400
    UNAUTHORIZED = 100401
    FORBIDDEN = 100403
    NOT_FOUND = 100404
    CONFLICT = 100409
    VALIDATION_ERROR = 100422
    INTERNAL_ERROR = 100500
    SERVICE_UNAVAILABLE = 100503


_DEFAULT_ERROR_CODE_BY_STATUS = {
    400: ErrorCode.BAD_REQUEST,
    401: ErrorCode.UNAUTHORIZED,
    403: ErrorCode.FORBIDDEN,
    404: ErrorCode.NOT_FOUND,
    409: ErrorCode.CONFLICT,
    422: ErrorCode.VALIDATION_ERROR,
    500: ErrorCode.INTERNAL_ERROR,
    503: ErrorCode.SERVICE_UNAVAILABLE,
}


def default_error_code(status_code: int) -> ErrorCode:
    """根据 HTTP 状态码返回默认通用错误码。"""
    return _DEFAULT_ERROR_CODE_BY_STATUS.get(status_code, ErrorCode.INTERNAL_ERROR)
