"""add like_count

Revision ID: bfb7b21576ab
Revises: c9d102a57c54
Create Date: 2020-05-28 10:10:49.637663

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bfb7b21576ab'
down_revision = 'c9d102a57c54'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comment', sa.Column('like_count', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('comment', 'like_count')
    # ### end Alembic commands ###
