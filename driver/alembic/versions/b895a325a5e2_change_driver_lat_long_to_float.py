"""change driver lat long to float

Revision ID: b895a325a5e2
Revises: 0a9fc578fc07
Create Date: 2025-12-25 14:07:54.932852

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b895a325a5e2'
down_revision: Union[str, Sequence[str], None] = '0a9fc578fc07'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
