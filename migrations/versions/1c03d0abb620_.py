"""empty message

Revision ID: 1c03d0abb620
Revises: ceaafba069dd
Create Date: 2024-09-19 01:01:10.235070

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1c03d0abb620'
down_revision = 'ceaafba069dd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('emails', schema=None) as batch_op:
        batch_op.add_column(sa.Column('department_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_emails_department_id', 'departments', ['department_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('emails', schema=None) as batch_op:
        batch_op.drop_constraint('fk_emails_department_id', type_='foreignkey')
        batch_op.drop_column('department_id')

    # ### end Alembic commands ###
