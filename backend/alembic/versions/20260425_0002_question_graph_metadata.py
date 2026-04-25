"""question graph metadata

Revision ID: 20260425_0002
Revises: 20260404_0001
Create Date: 2026-04-25 00:00:00
"""

from alembic import op
import sqlalchemy as sa


revision = "20260425_0002"
down_revision = "20260404_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("questions", sa.Column("key", sa.String(length=80), nullable=True))
    op.add_column("questions", sa.Column("main_dimension", sa.String(length=50), nullable=True))
    op.create_unique_constraint("uq_questions_key", "questions", ["key"])

    op.add_column(
        "options",
        sa.Column("activates_contradiction", sa.Boolean(), server_default=sa.false(), nullable=False),
    )
    op.add_column("options", sa.Column("contradiction_code", sa.String(length=120), nullable=True))
    op.add_column(
        "options",
        sa.Column("contradiction_penalty", sa.Integer(), server_default="0", nullable=False),
    )
    op.alter_column("options", "activates_contradiction", server_default=None)
    op.alter_column("options", "contradiction_penalty", server_default=None)


def downgrade() -> None:
    op.drop_column("options", "contradiction_penalty")
    op.drop_column("options", "contradiction_code")
    op.drop_column("options", "activates_contradiction")

    op.drop_constraint("uq_questions_key", "questions", type_="unique")
    op.drop_column("questions", "main_dimension")
    op.drop_column("questions", "key")
