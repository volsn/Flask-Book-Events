"""empty message

Revision ID: 946a1cd19559
Revises: a9048c0b1208
Create Date: 2021-08-25 11:09:39.621203

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '946a1cd19559'
down_revision = 'a9048c0b1208'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('guest_event',
    sa.Column('guest_id', sa.Integer(), nullable=True),
    sa.Column('event_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['event_id'], ['events.id'], ),
    sa.ForeignKeyConstraint(['guest_id'], ['guests.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('guest_event')
    # ### end Alembic commands ###