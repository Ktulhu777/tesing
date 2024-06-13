"""'initial'

Revision ID: e697badc7330
Revises: 034b352bf7eb
Create Date: 2024-06-12 17:32:37.385149

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e697badc7330'
down_revision: Union[str, None] = '034b352bf7eb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
