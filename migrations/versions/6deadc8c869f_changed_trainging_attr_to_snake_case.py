"""changed Trainging Attr to Snake_case

Revision ID: 6deadc8c869f
Revises: 
Create Date: 2024-09-04 13:53:25.388827

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6deadc8c869f'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    with op.batch_alter_table('trainings') as batch_op:
        # Instead of adding columns, drop the old camelCase columns
        batch_op.drop_column('trainingName')
        batch_op.drop_column('trainingDesc')
        batch_op.drop_column('trainingStart')
        batch_op.drop_column('trainingEnd')
        batch_op.drop_column('resourceUser')
        batch_op.drop_column('maxPhishingMail')
        batch_op.drop_column('agentStartDate')
        batch_op.drop_column('createdAt')
        batch_op.drop_column('updatedAt')

def downgrade():
    with op.batch_alter_table('trainings') as batch_op:
        # In case you need to revert the migration, add the camelCase columns back
        batch_op.add_column(sa.Column('trainingName', sa.String(100), nullable=False))
        batch_op.add_column(sa.Column('trainingDesc', sa.Text(), nullable=False))
        batch_op.add_column(sa.Column('trainingStart', sa.Date(), nullable=False))
        batch_op.add_column(sa.Column('trainingEnd', sa.Date(), nullable=False))
        batch_op.add_column(sa.Column('resourceUser', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('maxPhishingMail', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('agentStartDate', sa.Date(), nullable=True))
        batch_op.add_column(sa.Column('createdAt', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('updatedAt', sa.DateTime(), nullable=True))
