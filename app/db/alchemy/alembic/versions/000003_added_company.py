"""Added company

Revision ID: 000003
Revises: 000002
Create Date: 2024-04-25 22:54:04.733587

"""
import uuid
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision: str = "000003"
down_revision: Union[str, None] = "000002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "company",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column("owner_id", UUID(as_uuid=True)),
        sa.Column("name", sa.String(100), unique=True),
        sa.Column("description", sa.String(500)),
        sa.Column("visible", sa.Boolean, default=True),
    )


def downgrade() -> None:
    op.drop_table("company")
