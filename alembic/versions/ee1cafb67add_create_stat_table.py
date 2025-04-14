"""create stat_table

Revision ID: ee1cafb67add
Revises:
Create Date: 2025-04-14 16:11:30.599218

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "ee1cafb67add"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "player_stats",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("player", sa.String, nullable=False),
        sa.Column("pts", sa.Float, nullable=False),
        sa.Column('ast', sa.Float(), nullable=False),
        sa.Column('three_pt_pct', sa.Float(), nullable=False),  # maps to 3P%
        sa.Column('fg_pct', sa.Float(), nullable=False),        # maps to FG%
        sa.Column('trb', sa.Float(), nullable=False),
        sa.Column('stl', sa.Float(), nullable=False),
        sa.Column('blk', sa.Float(), nullable=False),
        sa.Column('tov', sa.Float(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('player_stats')
