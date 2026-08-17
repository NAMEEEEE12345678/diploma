"""Align checklist table with its SQLAlchemy model."""

from alembic import op
import sqlalchemy as sa


revision = "a0d8e6c319f4"
down_revision = "f3a1c8b429e2"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column(
        "checklist_items",
        "created_at",
        existing_type=sa.DateTime(timezone=True),
        nullable=False,
    )
    op.create_index(op.f("ix_checklist_items_user_id"), "checklist_items", ["user_id"])


def downgrade() -> None:
    op.drop_index(op.f("ix_checklist_items_user_id"), table_name="checklist_items")
    op.alter_column(
        "checklist_items",
        "created_at",
        existing_type=sa.DateTime(timezone=True),
        nullable=True,
    )
