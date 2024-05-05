"""Added quiz results

Revision ID: 000006
Revises: 000005
Create Date: 2024-05-04 16:49:54.225843

"""
import uuid
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB, UUID

# revision identifiers, used by Alembic.
revision: str = "000006"
down_revision: Union[str, None] = "000005"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "quiz_results",
        sa.Column(
            "id",
            UUID(as_uuid=True),
            primary_key=True,
            default=uuid.uuid4,
            nullable=False,
        ),
        sa.Column("company_id", UUID(as_uuid=True)),
        sa.Column("quiz_id", UUID(as_uuid=True)),
        sa.Column("user_id", UUID(as_uuid=True)),
        sa.ForeignKeyConstraint(["company_id"], ["company.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["quiz_id"], ["quiz.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.Column("results", JSONB(), nullable=True),
        sa.UniqueConstraint(
            "company_id", "quiz_id", "user_id", name="unique_quiz_results"
        ),
    )


def downgrade() -> None:
    op.drop_table("quiz_results")
