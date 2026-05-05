"""add description to products

Revision ID: b9f4c6e7d2a3
Revises: 8c1d2f31a5b1
Create Date: 2026-05-05 20:05:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "b9f4c6e7d2a3"
down_revision: Union[str, Sequence[str], None] = "8c1d2f31a5b1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("products") as batch_op:
        batch_op.add_column(
            sa.Column(
                "description",
                sa.String(length=255),
                nullable=False,
                server_default="Added after migration",
            )
        )

    with op.batch_alter_table("products") as batch_op:
        batch_op.alter_column("description", server_default=None)


def downgrade() -> None:
    with op.batch_alter_table("products") as batch_op:
        batch_op.drop_column("description")
