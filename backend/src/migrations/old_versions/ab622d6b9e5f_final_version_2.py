"""Final version 2

Revision ID: ab622d6b9e5f
Revises: 21dd39acd73b
Create Date: 2024-10-06 12:03:30.800442

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ab622d6b9e5f'
down_revision: Union[str, None] = '21dd39acd73b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('hierarchies', sa.Column('sub_username', sa.String(), nullable=False))
    op.add_column('hierarchies', sa.Column('super_username', sa.String(), nullable=False))
    op.drop_constraint('hierarchies_super_id_fkey', 'hierarchies', type_='foreignkey')
    op.drop_constraint('hierarchies_sub_id_fkey', 'hierarchies', type_='foreignkey')
    op.create_foreign_key(None, 'hierarchies', 'users', ['super_username'], ['username'])
    op.create_foreign_key(None, 'hierarchies', 'users', ['sub_username'], ['username'])
    op.drop_column('hierarchies', 'super_id')
    op.drop_column('hierarchies', 'sub_id')
    op.add_column('tasks', sa.Column('creator_username', sa.String(), nullable=False))
    op.add_column('tasks', sa.Column('receiver_username', sa.String(), nullable=False))
    op.drop_constraint('tasks_task_creator_fkey', 'tasks', type_='foreignkey')
    op.drop_constraint('tasks_task_receiver_fkey', 'tasks', type_='foreignkey')
    op.create_foreign_key(None, 'tasks', 'users', ['creator_username'], ['username'])
    op.create_foreign_key(None, 'tasks', 'users', ['receiver_username'], ['username'])
    op.drop_column('tasks', 'task_receiver')
    op.drop_column('tasks', 'task_creator')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tasks', sa.Column('task_creator', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('tasks', sa.Column('task_receiver', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'tasks', type_='foreignkey')
    op.drop_constraint(None, 'tasks', type_='foreignkey')
    op.create_foreign_key('tasks_task_receiver_fkey', 'tasks', 'users', ['task_receiver'], ['username'])
    op.create_foreign_key('tasks_task_creator_fkey', 'tasks', 'users', ['task_creator'], ['username'])
    op.drop_column('tasks', 'receiver_username')
    op.drop_column('tasks', 'creator_username')
    op.add_column('hierarchies', sa.Column('sub_id', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('hierarchies', sa.Column('super_id', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'hierarchies', type_='foreignkey')
    op.drop_constraint(None, 'hierarchies', type_='foreignkey')
    op.create_foreign_key('hierarchies_sub_id_fkey', 'hierarchies', 'users', ['sub_id'], ['username'])
    op.create_foreign_key('hierarchies_super_id_fkey', 'hierarchies', 'users', ['super_id'], ['username'])
    op.drop_column('hierarchies', 'super_username')
    op.drop_column('hierarchies', 'sub_username')
    # ### end Alembic commands ###
