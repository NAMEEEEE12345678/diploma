"""add custom itinerary places

Revision ID: e2b9c5f210d1
Revises: d74dd7e0fc2b
"""
from alembic import op
import sqlalchemy as sa

revision = "e2b9c5f210d1"
down_revision = "d74dd7e0fc2b"
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.alter_column("itinerary_items", "place_id", existing_type=sa.Integer(), nullable=True)
    op.add_column("itinerary_items", sa.Column("custom_title", sa.String(length=180), nullable=True))

def downgrade() -> None:
    op.drop_column("itinerary_items", "custom_title")
    op.alter_column("itinerary_items", "place_id", existing_type=sa.Integer(), nullable=False)
