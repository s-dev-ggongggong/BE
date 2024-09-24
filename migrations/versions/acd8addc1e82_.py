"""empty message

Revision ID: acd8addc1e82
Revises: d03b82083c64
Create Date: 2024-09-24 15:37:33.191979

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite
import json

from sqlalchemy import TypeDecorator, Text

# revision identifiers, used by Alembic.
revision = 'acd8addc1e82'
down_revision = 'd03b82083c64'
branch_labels = None
depends_on = None


class JSONEncodedDict(TypeDecorator):
    impl = Text
    cache_ok = True  # 캐시 키 사용 허용

    def process_bind_param(self, value, dialect):
        return json.dumps(value) if value else None

    def process_result_value(self, value, dialect):
        return json.loads(value) if value else None
    
    
def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('complete_trainings', schema=None) as batch_op:
        batch_op.alter_column('dept_target',
               existing_type=sqlite.JSON(),
               type_=JSONEncodedDict(),
               existing_nullable=False)
        batch_op.alter_column('role_target',
               existing_type=sqlite.JSON(),
               type_=JSONEncodedDict(),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('complete_trainings', schema=None) as batch_op:
        batch_op.alter_column('role_target',
               existing_type= JSONEncodedDict(),
               type_=sqlite.JSON(),
               existing_nullable=False)
        batch_op.alter_column('dept_target',
               existing_type=JSONEncodedDict(),
               type_=sqlite.JSON(),
               existing_nullable=False)

    # ### end Alembic commands ###
