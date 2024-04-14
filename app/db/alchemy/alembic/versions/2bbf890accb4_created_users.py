"""created users

Revision ID: 2bbf890accb4
Revises: 
Create Date: 2024-04-14 13:11:01.347381

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "2bbf890accb4"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("email", sa.String(80), unique=True, index=True),
        sa.Column("password", sa.String),
    )


def downgrade() -> None:
    op.drop_table("account")
