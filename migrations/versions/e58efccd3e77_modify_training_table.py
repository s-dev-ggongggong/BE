"""modify_training_table

Revision ID: e58efccd3e77
Revises: c9aacb6ad5d7
Create Date: 2023-07-11 12:34:56.789012

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e58efccd3e77'
down_revision = 'c9aacb6ad5d7'
branch_labels = None
depends_on = None


def upgrade():
    # Create a new table with the desired structure
    op.create_table('new_trainings',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('trainingName', sa.String(length=100), nullable=False),
        sa.Column('trainingDesc', sa.Text(), nullable=False),
        sa.Column('trainingStart', sa.Date(), nullable=False),
        sa.Column('trainingEnd', sa.Date(), nullable=False),
        sa.Column('resourceUser', sa.Integer(), nullable=False),
        sa.Column('maxPhishingMail', sa.Integer(), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('agentStartDate', sa.Date(), nullable=True),
        sa.Column('department', sa.String(length=50), nullable=False),
        sa.Column('createdAt', sa.DateTime(), nullable=True),
        sa.Column('updatedAt', sa.DateTime(), nullable=True),
        sa.Column('agentId', sa.Integer(), nullable=True),
        sa.Column('userId', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['agentId'], ['agents.id'], ),
        sa.ForeignKeyConstraint(['userId'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Copy data from the old table to the new one
    op.execute('''
        INSERT INTO new_trainings (id, trainingName, trainingDesc, trainingStart, trainingEnd, 
                                   resourceUser, maxPhishingMail, status, agentId)
        SELECT id, trainingName, trainingDesc, trainingStart, trainingEnd, 
               resourceUser, maxPhishingMail, status, agentId
        FROM trainings
    ''')

    # Drop the old table
    op.drop_table('trainings')

    # Rename the new table to 'trainings'
    op.rename_table('new_trainings', 'trainings')


def downgrade():
    # Create the original table structure
    op.create_table('old_trainings',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('trainingName', sa.String(length=100), nullable=False),
        sa.Column('trainingDesc', sa.String(length=500), nullable=False),
        sa.Column('trainingStart', sa.DateTime(), nullable=True),
        sa.Column('trainingEnd', sa.DateTime(), nullable=True),
        sa.Column('resourceUser', sa.Integer(), nullable=False),
        sa.Column('maxPhishingMail', sa.Integer(), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=True),
        sa.Column('date', sa.Date(), nullable=True),
        sa.Column('agentId', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['agentId'], ['agents.id'], ),
        sa.ForeignKeyConstraint(['resourceUser'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Copy data back to the old structure
    op.execute('''
        INSERT INTO old_trainings (id, trainingName, trainingDesc, trainingStart, trainingEnd, 
                                   resourceUser, maxPhishingMail, status, agentId)
        SELECT id, trainingName, trainingDesc, trainingStart, trainingEnd, 
               resourceUser, maxPhishingMail, status, agentId
        FROM trainings
    ''')

    # Drop the new table
    op.drop_table('trainings')

    # Rename the old structure table to 'trainings'
    op.rename_table('old_trainings', 'trainings')