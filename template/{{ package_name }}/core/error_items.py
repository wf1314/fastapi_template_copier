from pydantic import BaseModel, ConfigDict, Field


class ErrorItem(BaseModel):
    """统一错误明细项。"""

    model_config = ConfigDict(extra="allow")

    field: str | None = Field(
        default=None,
        description="出错字段或业务对象标识；无法定位到字段时为 null。",
        examples=["resource_id"],
    )
    message: str = Field(
        description="面向调用方的错误明细消息。",
        examples=["Resource cannot be processed."],
    )
    code: str | None = Field(
        default=None,
        description="错误明细码，可用于前端按字段或规则做精确处理。",
        examples=["invalid_resource_state"],
    )
