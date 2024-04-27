"""Added is_active field for user

Revision ID: 4498ae3601a9
Revises: 000001
Create Date: 2024-04-24 21:26:58.095206

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "000002"
down_revision: Union[str, None] = "000001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "users", sa.Column("is_active", sa.Boolean, default=True, nullable=False)
    )


def downgrade() -> None:
    op.drop_column("users", "is_active")
