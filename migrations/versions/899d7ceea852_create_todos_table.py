"""create todos table

Revision ID: 899d7ceea852
Revises: e1029ea042ab
Create Date: 2024-10-09 13:24:23.911117

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '899d7ceea852'
down_revision: Union[str, None] = 'e1029ea042ab'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'todos',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column(
            'state',
            sa.Enum(
                'draft', 'todo', 'doing', 'done', 'trash', name='todostate'
            ),
            nullable=False,
        ),
        sa.Column(
            'user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False
        ),
        sa.Column(
            'created_at',
            sa.DateTime(),
            server_default=sa.text('(CURRENT_TIMESTAMP)'),
            nullable=False,
        ),
        sa.Column(
            'updated_at',
            sa.DateTime(),
            server_default=sa.text('(CURRENT_TIMESTAMP)'),
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_table('todos')
