"""Ensure supply all Training model attr

Revision ID: 59b7d7066bc7
Revises: b9c08ed0e27d
Create Date: 2024-09-04 14:07:16.875087

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime

# revision identifiers, used by Alembic.
revision = '59b7d7066bc7'
down_revision = 'b9c08ed0e27d'
branch_labels = None
depends_on = None


def column_exists(table_name, column_name):
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    columns = [col['name'] for col in inspector.get_columns(table_name)]
    return column_name in columns


def upgrade():
    with op.batch_alter_table('trainings') as batch_op:
        # Only add columns that don't already exist
        if not column_exists('trainings', 'training_name'):
            batch_op.add_column(sa.Column('training_name', sa.String(length=100), nullable=False, server_default='default_name'))
        if not column_exists('trainings', 'training_desc'):
            batch_op.add_column(sa.Column('training_desc', sa.Text, nullable=False, server_default='default_desc'))
        if not column_exists('trainings', 'training_start'):
            batch_op.add_column(sa.Column('training_start', sa.Date, nullable=False, server_default='2023-01-01'))
        if not column_exists('trainings', 'training_end'):
            batch_op.add_column(sa.Column('training_end', sa.Date, nullable=False, server_default='2023-01-02'))
        if not column_exists('trainings', 'department'):
            batch_op.add_column(sa.Column('department', sa.String(length=50), nullable=False, server_default='General'))
        if not column_exists('trainings', 'max_phishing_mail'):
            batch_op.add_column(sa.Column('max_phishing_mail', sa.Integer, nullable=False, server_default='0'))
        if not column_exists('trainings', 'created_at'):
            batch_op.add_column(sa.Column('created_at', sa.DateTime, default=datetime.utcnow))


def downgrade():
    with op.batch_alter_table('trainings') as batch_op:
        # Drop columns if they exist
        if column_exists('trainings', 'training_name'):
            batch_op.drop_column('training_name')
        if column_exists('trainings', 'training_desc'):
            batch_op.drop_column('training_desc')
        if column_exists('trainings', 'training_start'):
            batch_op.drop_column('training_start')
        if column_exists('trainings', 'training_end'):
            batch_op.drop_column('training_end')
        if column_exists('trainings', 'department'):
            batch_op.drop_column('department')
        if column_exists('trainings', 'max_phishing_mail'):
            batch_op.drop_column('max_phishing_mail')
        if column_exists('trainings', 'created_at'):
            batch_op.drop_column('created_at')
