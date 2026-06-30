from typing import Annotated, Literal

from fastapi import Query
from pydantic import BaseModel, ConfigDict, Field

DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100

SortDirection = Literal["asc", "desc"]


class PaginationParams(BaseModel):
    """分页查询参数模型。"""

    model_config = ConfigDict(frozen=True)

    page: int = Field(default=1, ge=1, description="页码，从 1 开始。")
    page_size: int = Field(
        default=DEFAULT_PAGE_SIZE,
        ge=1,
        le=MAX_PAGE_SIZE,
        description=f"每页数量，最大 {MAX_PAGE_SIZE}。",
    )

    @property
    def offset(self) -> int:
        """SQL 查询常用 offset。"""
        return (self.page - 1) * self.page_size

    @property
    def limit(self) -> int:
        """SQL 查询常用 limit。"""
        return self.page_size


class SortParams(BaseModel):
    """排序查询参数模型。"""

    model_config = ConfigDict(frozen=True)

    sort_by: str | None = Field(
        default=None,
        pattern=r"^[a-zA-Z_][a-zA-Z0-9_]*$",
        description="排序字段名称；为空时使用业务默认排序。",
    )
    sort_order: SortDirection = Field(
        default="asc",
        description="排序方向。",
    )


class ListQueryParams(PaginationParams):
    """常见列表接口查询参数模型，组合分页和排序。"""

    sort_by: str | None = Field(
        default=None,
        pattern=r"^[a-zA-Z_][a-zA-Z0-9_]*$",
        description="排序字段名称；为空时使用业务默认排序。",
    )
    sort_order: SortDirection = Field(
        default="asc",
        description="排序方向。",
    )


PaginationQuery = Annotated[PaginationParams, Query()]
SortQuery = Annotated[SortParams, Query()]
ListQuery = Annotated[ListQueryParams, Query()]
