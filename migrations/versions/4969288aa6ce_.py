"""---> Todo : Add completed column

Revision ID: 4969288aa6ce
Revises: 0ca18a599b79
Create Date: 2022-04-03 16:15:25.298474

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4969288aa6ce'
down_revision = '0ca18a599b79'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('todos', sa.Column('completed', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###
    op.execute("UPDATE todos SET completed = False WHERE completed IS NULL")

    op.alter_column("todos", "completed", nullable=False)

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('todos', 'completed')
    # ### end Alembic commands ###
