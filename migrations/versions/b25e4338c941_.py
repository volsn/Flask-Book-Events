"""empty message

Revision ID: b25e4338c941
Revises: 2b671dc0e4fc
Create Date: 2021-08-31 09:47:23.375406

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b25e4338c941'
down_revision = '2b671dc0e4fc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('guest_event', sa.Column('id', sa.Integer(), nullable=False))
    op.drop_constraint('guest_event_guest_id_fkey', 'guest_event', type_='foreignkey')
    op.drop_constraint('guest_event_event_id_fkey', 'guest_event', type_='foreignkey')
    op.create_foreign_key(None, 'guest_event', 'events', ['event_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'guest_event', 'guests', ['guest_id'], ['id'], ondelete='CASCADE')
    op.add_column('participant_event', sa.Column('id', sa.Integer(), nullable=False))
    op.drop_constraint('participant_event_participant_id_fkey', 'participant_event', type_='foreignkey')
    op.drop_constraint('participant_event_event_id_fkey', 'participant_event', type_='foreignkey')
    op.create_foreign_key(None, 'participant_event', 'participants', ['participant_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'participant_event', 'events', ['event_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'participant_event', type_='foreignkey')
    op.drop_constraint(None, 'participant_event', type_='foreignkey')
    op.create_foreign_key('participant_event_event_id_fkey', 'participant_event', 'events', ['event_id'], ['id'])
    op.create_foreign_key('participant_event_participant_id_fkey', 'participant_event', 'participants', ['participant_id'], ['id'])
    op.drop_column('participant_event', 'id')
    op.drop_constraint(None, 'guest_event', type_='foreignkey')
    op.drop_constraint(None, 'guest_event', type_='foreignkey')
    op.create_foreign_key('guest_event_event_id_fkey', 'guest_event', 'events', ['event_id'], ['id'])
    op.create_foreign_key('guest_event_guest_id_fkey', 'guest_event', 'guests', ['guest_id'], ['id'])
    op.drop_column('guest_event', 'id')
    # ### end Alembic commands ###
