"""research_context-non-null-goal, unique_lfn

Revision ID: 53a8997487a2
Revises: d9841daf0019
Create Date: 2023-08-21 15:57:33.996946

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '53a8997487a2'
down_revision: Union[str, None] = 'd9841daf0019'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'documents', ['lfn'])
    op.alter_column('research_contexts', 'research_id',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.create_unique_constraint(None, 'vector_stores', ['lfn'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'vector_stores', type_='unique')
    op.alter_column('research_contexts', 'research_id',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_constraint(None, 'documents', type_='unique')
    # ### end Alembic commands ###