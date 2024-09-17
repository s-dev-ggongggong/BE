"""update admin

Revision ID: ceaafba069dd
Revises: 9e95d0d59b51
Create Date: 2024-09-17 13:40:46.972054

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column

# revision identifiers, used by Alembic.
revision = 'ceaafba069dd'
down_revision = '9e95d0d59b51'
branch_labels = None
depends_on = None



def upgrade():
    # Define a table representation
    employees = table('employees',
        column('id', sa.Integer),
        column('name', sa.String),
        column('admin_id', sa.String),
        column('admin_pw', sa.String)
    )
    op.execute(
        employees.update().
        where(employees.c.name == 'ADMIN').
        values({'admin_id': 'admin', 'admin_pw': 'admin1234'})
    )



def downgrade():
    # Define a table representation
    employees = table('employees',
        column('id', sa.Integer),
        column('name', sa.String),
        column('admin_id', sa.String),
        column('admin_pw', sa.String)
    )

    # Revert the changes
    op.execute(
        employees.update().
        where(employees.c.name == 'ADMIN').
        values({'admin_id': None, 'admin_pw': None})
    )