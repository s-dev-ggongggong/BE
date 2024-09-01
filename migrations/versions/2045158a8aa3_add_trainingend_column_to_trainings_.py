"""Add trainingEnd column to trainings table

Revision ID: 2045158a8aa3
Revises: 68f7919c27cc
Create Date: 2024-09-02 02:04:09.171495

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2045158a8aa3'
down_revision = '68f7919c27cc'
branch_labels = None
depends_on = None


def upgrade():
    print("Apply upgrade")
    op.create_table('formField',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('form_id', sa.Integer(), nullable=False),
        sa.Column('field_name', sa.String(length=120), nullable=False),
        sa.Column('field_type', sa.String(length=50), nullable=False),
        sa.ForeignKeyConstraint(['form_id'], ['form.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.add_column('trainings', sa.Column('trainingEnd', sa.DateTime(), nullable=False))
    op.add_column('trainings', sa.Column('maxPhishingMail', sa.Integer(), nullable=True))


def downgrade():
    print("Downgrade")
    op.drop_table('formField')
    op.drop_column('trainings', 'trainingEnd')
    op.drop_column('trainings', 'maxPhishingMail')
