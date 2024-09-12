"""empty message

Revision ID: 9f4b9360f5fd
Revises: 14015c1514a4
Create Date: 2024-09-12 15:30:29.781343

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column

# revision identifiers, used by Alembic.
revision = '9f4b9360f5fd'
down_revision = '14015c1514a4'
branch_labels = None
depends_on = None


def upgrade():
    # Add admin_id and admin_pw columns
    with op.batch_alter_table('employees', schema=None) as batch_op:
        batch_op.add_column(sa.Column('admin_id', sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column('admin_pw', sa.String(length=50), nullable=True))

    # Create a table object for the employees table
    employees_table = table('employees',
        column('name', sa.String),
        column('admin_id', sa.String),
        column('admin_pw', sa.String)
    )

    # Update the admin user with admin credentials
    op.execute(
        employees_table.update().
        where(employees_table.c.name == 'admin').
        values(admin_id='admin', admin_pw='admin1234')
    )


def downgrade():
    with op.batch_alter_table('employees', schema=None) as batch_op:
        batch_op.drop_column('admin_pw')
        batch_op.drop_column('admin_id')