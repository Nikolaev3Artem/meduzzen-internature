"""Added quizzes

Revision ID: 000005
Revises: 000004
Create Date: 2024-05-03 20:50:42.663951

"""
import uuid
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB, UUID

# revision identifiers, used by Alembic.
revision: str = "000005"
down_revision: Union[str, None] = "000004"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "quiz",
        sa.Column(
            "id",
            UUID(as_uuid=True),
            primary_key=True,
            default=uuid.uuid4,
            nullable=False,
        ),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("description", sa.String(500), nullable=True),
        sa.Column("submitions", sa.Integer(), nullable=False, default=0),
        sa.Column("questions", JSONB(), nullable=False),
        sa.Column("company_id", UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(["company_id"], ["company.id"], ondelete="CASCADE"),
    )


def downgrade() -> None:
    op.drop_table("quiz")
