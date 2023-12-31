"""add notes for docs, research topics, conversations

Revision ID: fe278579d45d
Revises: cd6cbc865534
Create Date: 2023-08-23 19:58:44.985073

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "fe278579d45d"
down_revision: Union[str, None] = "cd6cbc865534"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "document_note",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("document_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["document_id"],
            ["knowledge_base.id"],
        ),
        sa.ForeignKeyConstraint(
            ["id"],
            ["note.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        mysql_engine="InnoDB",
    )
    op.create_table(
        "research_topic_note",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("research_topic_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["id"],
            ["note.id"],
        ),
        sa.ForeignKeyConstraint(
            ["research_topic_id"],
            ["research_topic.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        mysql_engine="InnoDB",
    )
    op.create_table(
        "conversation_note",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("conversation_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["conversation_id"],
            ["conversation.id"],
        ),
        sa.ForeignKeyConstraint(
            ["id"],
            ["note.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        mysql_engine="InnoDB",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("conversation_note")
    op.drop_table("research_topic_note")
    op.drop_table("document_note")
    # ### end Alembic commands ###
