"""created users

Revision ID: 000001
Revises: 
Create Date: 2024-04-14 21:44:03.433504

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "000001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("uuid", sa.Integer, primary_key=True),
        sa.Column("email", sa.String(80), unique=True),
        sa.Column("password", sa.String),
        sa.Column("username", sa.String(100)),
    )


def downgrade() -> None:
    op.drop_table("users")
