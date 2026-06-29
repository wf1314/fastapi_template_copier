"""${message}

迁移版本 ID: ${up_revision}
上一版本: ${down_revision | comma,n}
创建时间: ${create_date}

"""
from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

revision: str = ${repr(up_revision)}
down_revision: str | Sequence[str] | None = ${repr(down_revision)}
branch_labels: str | Sequence[str] | None = ${repr(branch_labels)}
depends_on: str | Sequence[str] | None = ${repr(depends_on)}


def upgrade() -> None:
    """应用数据库结构变更。"""
    ${upgrades if upgrades else "pass"}


def downgrade() -> None:
    """回滚数据库结构变更。"""
    ${downgrades if downgrades else "pass"}
