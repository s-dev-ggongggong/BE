"""empty message

Revision ID: d03b82083c64
Revises: aab2b0ac72d2
Create Date: 2024-09-24 15:29:28.846577

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite


# revision identifiers, used by Alembic.
revision = 'd03b82083c64'
down_revision = 'aab2b0ac72d2'
branch_labels = None
depends_on = None

def upgrade():
    with op.batch_alter_table('complete_trainings', schema=None) as batch_op:
        batch_op.alter_column('dept_target',
               existing_type=sa.TEXT(),
               type_=sa.JSON().with_variant(sqlite.JSON(), 'sqlite'),
               existing_nullable=False)
        batch_op.alter_column('role_target',
               existing_type=sa.TEXT(),
               type_=sa.JSON().with_variant(sqlite.JSON(), 'sqlite'),
               existing_nullable=False)

def downgrade():
    with op.batch_alter_table('complete_trainings', schema=None) as batch_op:
        batch_op.alter_column('role_target',
               existing_type=sa.JSON().with_variant(sqlite.JSON(), 'sqlite'),
               type_=sa.TEXT(),
               existing_nullable=False)
        batch_op.alter_column('dept_target',
               existing_type=sa.JSON().with_variant(sqlite.JSON(), 'sqlite'),
               type_=sa.TEXT(),
               existing_nullable=False)
