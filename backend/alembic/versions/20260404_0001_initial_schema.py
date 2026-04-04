"""initial schema

Revision ID: 20260404_0001
Revises: 
Create Date: 2026-04-04 00:00:00
"""

from alembic import op
import sqlalchemy as sa


revision = "20260404_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "questions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("text", sa.String(length=500), nullable=False),
        sa.Column("is_start", sa.Boolean(), nullable=False),
        sa.Column("is_terminal", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_questions_id"), "questions", ["id"], unique=False)

    op.create_table(
        "sessions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("final_score", sa.Float(), nullable=True),
        sa.Column("final_result", sa.String(length=50), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_sessions_id"), "sessions", ["id"], unique=False)

    op.create_table(
        "options",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("question_id", sa.Integer(), nullable=False),
        sa.Column("text", sa.String(length=300), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["question_id"], ["questions.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_options_id"), "options", ["id"], unique=False)

    op.create_table(
        "option_effects",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("option_id", sa.Integer(), nullable=False),
        sa.Column("dimension", sa.String(length=50), nullable=False),
        sa.Column("value", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["option_id"], ["options.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_option_effects_id"), "option_effects", ["id"], unique=False)

    op.create_table(
        "option_next_questions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("option_id", sa.Integer(), nullable=False),
        sa.Column("next_question_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["next_question_id"], ["questions.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["option_id"], ["options.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("option_id"),
    )
    op.create_index(op.f("ix_option_next_questions_id"), "option_next_questions", ["id"], unique=False)

    op.create_table(
        "session_answers",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("session_id", sa.Integer(), nullable=False),
        sa.Column("question_id", sa.Integer(), nullable=False),
        sa.Column("option_id", sa.Integer(), nullable=False),
        sa.Column("answered_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["option_id"], ["options.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["question_id"], ["questions.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["session_id"], ["sessions.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_session_answers_id"), "session_answers", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_session_answers_id"), table_name="session_answers")
    op.drop_table("session_answers")
    op.drop_index(op.f("ix_option_next_questions_id"), table_name="option_next_questions")
    op.drop_table("option_next_questions")
    op.drop_index(op.f("ix_option_effects_id"), table_name="option_effects")
    op.drop_table("option_effects")
    op.drop_index(op.f("ix_options_id"), table_name="options")
    op.drop_table("options")
    op.drop_index(op.f("ix_sessions_id"), table_name="sessions")
    op.drop_table("sessions")
    op.drop_index(op.f("ix_questions_id"), table_name="questions")
    op.drop_table("questions")
