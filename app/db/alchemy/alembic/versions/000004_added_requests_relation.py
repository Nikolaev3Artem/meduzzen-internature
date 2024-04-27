"""added requests relation

Revision ID: 000004
Revises: 000004
Create Date: 2024-04-26 18:40:31.538691

"""
import uuid
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import ENUM, UUID

from app.db.alchemy.models import RequestStatus

# revision identifiers, used by Alembic.
revision: str = "000004"
down_revision: Union[str, None] = "000003"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "company_requests",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column("user_id", UUID(as_uuid=True)),
        sa.Column("company_id", UUID(as_uuid=True)),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["company_id"], ["company.id"], ondelete="CASCADE"),
        sa.Column("status", ENUM(RequestStatus)),
    )


def downgrade() -> None:
    op.drop_table("company_requests")
