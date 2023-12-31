"""add knowledge_base, research_topic, research_context, vector_store 

Revision ID: 20658262aa85
Revises: a66a432bf8a8
Create Date: 2023-08-23 16:06:38.310730

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "20658262aa85"
down_revision: Union[str, None] = "a66a432bf8a8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "knowledge_base",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("lfn", sa.String(), nullable=False),
        sa.Column("protocol", sa.Enum("S3", "NAS", "LOCAL", name="protocolenum"), nullable=False),
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("deleted", sa.Boolean(), nullable=True),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.CheckConstraint("CREATED_AT IS NOT NULL", name="KNOWLEDGE_BASE_CREATED_NN"),
        sa.CheckConstraint("DELETED IS NOT NULL", name="KNOWLEDGE_BASE_DELETED_NN"),
        sa.CheckConstraint("UPDATED_AT IS NOT NULL", name="KNOWLEDGE_BASE_UPDATED_NN"),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.prada_user_uuid"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("lfn"),
        mysql_engine="InnoDB",
    )
    op.create_table(
        "research_topic",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("prada_tagger_node_id", sa.String(), nullable=True),
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("deleted", sa.Boolean(), nullable=True),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.CheckConstraint("CREATED_AT IS NOT NULL", name="RESEARCH_TOPIC_CREATED_NN"),
        sa.CheckConstraint("DELETED IS NOT NULL", name="RESEARCH_TOPIC_DELETED_NN"),
        sa.CheckConstraint("UPDATED_AT IS NOT NULL", name="RESEARCH_TOPIC_UPDATED_NN"),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.prada_user_uuid"],
        ),
        sa.PrimaryKeyConstraint("id"),
        mysql_engine="InnoDB",
    )
    op.create_table(
        "research_context",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("research_topic_id", sa.Integer(), nullable=False),
        sa.Column("deleted", sa.Boolean(), nullable=True),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.CheckConstraint("CREATED_AT IS NOT NULL", name="RESEARCH_CONTEXT_CREATED_NN"),
        sa.CheckConstraint("DELETED IS NOT NULL", name="RESEARCH_CONTEXT_DELETED_NN"),
        sa.CheckConstraint("UPDATED_AT IS NOT NULL", name="RESEARCH_CONTEXT_UPDATED_NN"),
        sa.ForeignKeyConstraint(
            ["research_topic_id"],
            ["research_topic.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        mysql_engine="InnoDB",
    )
    op.create_table(
        "research_topic_knowledge_base_association",
        sa.Column("research_topic_id", sa.Integer(), nullable=True),
        sa.Column("document_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["document_id"],
            ["knowledge_base.id"],
        ),
        sa.ForeignKeyConstraint(
            ["research_topic_id"],
            ["research_topic.id"],
        ),
    )
    op.create_table(
        "document_research_context_association",
        sa.Column("document_id", sa.Integer(), nullable=True),
        sa.Column("research_context_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["document_id"],
            ["knowledge_base.id"],
        ),
        sa.ForeignKeyConstraint(
            ["research_context_id"],
            ["research_context.id"],
        ),
    )
    op.create_table(
        "vector_store",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("lfn", sa.String(), nullable=False),
        sa.Column("protocol", sa.Enum("S3", "NAS", "LOCAL", name="protocolenum"), nullable=False),
        sa.Column("research_context_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.CheckConstraint("CREATED_AT IS NOT NULL", name="VECTOR_STORE_CREATED_NN"),
        sa.CheckConstraint("UPDATED_AT IS NOT NULL", name="VECTOR_STORE_UPDATED_NN"),
        sa.ForeignKeyConstraint(
            ["research_context_id"],
            ["research_context.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("lfn"),
        mysql_engine="InnoDB",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("vector_store")
    op.drop_table("document_research_context_association")
    op.drop_table("research_topic_knowledge_base_association")
    op.drop_table("research_context")
    op.drop_table("research_topic")
    op.drop_table("knowledge_base")
    # ### end Alembic commands ###
