"""Remove duplicate attr in trainings;
l

Revision ID: b9c08ed0e27d
Revises: 6deadc8c869f
Create Date: 2024-09-04 14:03:27.156953

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b9c08ed0e27d'
down_revision = '6deadc8c869f'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('trainings') as batch_op:
        # Drop the duplicate columns
        batch_op.drop_column('department')
        batch_op.drop_column('agent_id')
        batch_op.drop_column('employee_id')
        batch_op.drop_column('training_name')
        batch_op.drop_column('training_desc')
        batch_op.drop_column('training_start')
        batch_op.drop_column('training_end')
        batch_op.drop_column('max_phishing_mail')
        batch_op.drop_column('created_at')

def downgrade():
    with op.batch_alter_table('trainings') as batch_op:
        # Add the dropped columns back in case of a downgrade
        batch_op.add_column(sa.Column('department', sa.String(length=50), nullable=False))
        batch_op.add_column(sa.Column('agent_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('employee_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('training_name', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('training_desc', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('training_start', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('training_end', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('max_phishing_mail', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('created_at', sa.DateTime(), nullable=True))
