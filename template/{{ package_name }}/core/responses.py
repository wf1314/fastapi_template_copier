from typing import Any

from pydantic import BaseModel, Field


class ApiResponse[DataT](BaseModel):
    """所有接口共用的响应包裹结构。"""

    code: int = Field(description="业务状态码，0 表示成功。", examples=[0])
    message: str = Field(description="响应消息。", examples=["success"])
    data: DataT | None = Field(default=None, description="业务响应数据。")
    errors: list[dict[str, Any]] | None = Field(
        default=None,
        description="结构化错误明细；成功响应为 null。",
    )


class ErrorResponse(BaseModel):
    """统一错误响应结构，用于 Swagger 展示通用异常格式。"""

    code: int = Field(
        description="业务错误码，通常与 HTTP 状态码一致。",
        examples=[400, 422, 500],
    )
    message: str = Field(
        description="错误消息。",
        examples=[
            "Example error",
            "Request validation failed",
            "Internal server error",
        ],
    )
    data: None = Field(default=None, description="错误响应没有业务数据。")
    errors: list[dict[str, Any]] | None = Field(
        default=None,
        description="结构化错误明细；没有明细时为 null。",
    )


def success_response[DataT](
    data: DataT | None = None,
    *,
    message: str = "success",
    code: int = 0,
) -> ApiResponse[DataT]:
    """构造统一成功响应。"""
    return ApiResponse(code=code, message=message, data=data, errors=None)


def error_response_content(
    *,
    code: int,
    message: str,
    errors: list[dict[str, Any]] | None = None,
    data: Any | None = None,
) -> dict[str, Any]:
    """构造统一错误响应内容，供异常处理器直接序列化。"""
    return {
        "code": code,
        "message": message,
        "data": data,
        "errors": errors,
    }
