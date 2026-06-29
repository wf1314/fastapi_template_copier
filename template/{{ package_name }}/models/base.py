from datetime import datetime

from sqlalchemy import DateTime, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


def system_now() -> datetime:
    """返回当前本地时间，便于测试时替换时间来源。"""
    return datetime.now()


class Base(DeclarativeBase):
    """所有 SQLAlchemy 模型的声明式基类。"""

    pass


class TimestampMixin:
    """提供自增主键和创建、更新时间字段的通用模型混入。"""

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        default=system_now,
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        default=system_now,
        onupdate=system_now,
        nullable=False,
    )
