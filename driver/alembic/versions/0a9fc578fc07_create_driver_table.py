"""create driver table

Revision ID: 0a9fc578fc07
Revises: f8a7e94f2a94
Create Date: 2025-12-25 14:02:45.194749
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '0a9fc578fc07'
down_revision: Union[str, Sequence[str], None] = 'f8a7e94f2a94'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # add new column
    op.add_column(
        'driver_details',
        sa.Column('drive_password_confirm', sa.String(), nullable=False)
    )

    # safely convert string → float
    op.alter_column(
        'driver_details',
        'driver_lan',
        type_=sa.Float(),
        postgresql_using="driver_lan::double precision"
    )

    op.alter_column(
        'driver_details',
        'driver_long',
        type_=sa.Float(),
        postgresql_using="driver_long::double precision"
    )

    op.alter_column(
        'driver_details',
        'driver_rating',
        type_=sa.Float(),
        postgresql_using="driver_rating::double precision"
    )


def downgrade() -> None:
    op.alter_column(
        'driver_details',
        'driver_rating',
        type_=sa.String()
    )

    op.alter_column(
        'driver_details',
        'driver_long',
        type_=sa.String()
    )

    op.alter_column(
        'driver_details',
        'driver_lan',
        type_=sa.String()
    )

    op.drop_column('driver_details', 'drive_password_confirm')
