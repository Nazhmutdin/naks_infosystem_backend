"""acst table initialization

Revision ID: 4628494c9cde
Revises: ade3188eeef1
Create Date: 2024-11-13 13:34:23.179783

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "4628494c9cde"
down_revision: Union[str, None] = "ade3188eeef1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "acst_table",
        sa.Column("ident", sa.UUID(), nullable=False),
        sa.Column("acst_number", sa.String(), nullable=False),
        sa.Column("certification_date", sa.Date(), nullable=False),
        sa.Column("expiration_date", sa.Date(), nullable=False),
        sa.Column("company", sa.String(), nullable=False),
        sa.Column("gtd", sa.ARRAY(sa.String()), nullable=False),
        sa.Column("method", sa.String(), nullable=True),
        sa.Column("detail_types", sa.ARRAY(sa.String()), nullable=True),
        sa.Column("joint_types", sa.ARRAY(sa.String()), nullable=True),
        sa.Column("materials", sa.ARRAY(sa.String()), nullable=True),
        sa.Column("thikness_from", sa.Float(), nullable=True),
        sa.Column("thikness_before", sa.Float(), nullable=True),
        sa.Column("diameter_from", sa.Float(), nullable=True),
        sa.Column("diameter_before", sa.Float(), nullable=True),
        sa.Column("preheating", sa.Boolean(), nullable=False),
        sa.Column("heat_treatment", sa.Boolean(), nullable=False),
        sa.Column("html", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("ident"),
        sa.UniqueConstraint("acst_number"),
    )
    op.create_index("acst_gtd_idx", "acst_table", ["gtd"], unique=False)
    op.create_index("acst_ident_idx", "acst_table", ["ident"], unique=False)
    op.create_index(
        "acst_idx",
        "acst_table",
        ["acst_number", "certification_date", "expiration_date"],
        unique=False,
    )
    op.create_index("acst_method_idx", "acst_table", ["method"], unique=False)
    op.create_index(
        "diameter_before_idx", "acst_table", ["diameter_before"], unique=False
    )
    op.create_index(
        "diameter_from_idx", "acst_table", ["diameter_from"], unique=False
    )
    op.create_index(
        "thikness_before_idx", "acst_table", ["thikness_before"], unique=False
    )
    op.create_index(
        "thikness_from_idx", "acst_table", ["thikness_from"], unique=False
    )
    op.drop_index("total_rejectedidx", table_name="ndt_table")
    op.create_index(
        "total_rejected_idx", "ndt_table", ["total_rejected"], unique=False
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("total_rejected_idx", table_name="ndt_table")
    op.create_index(
        "total_rejectedidx", "ndt_table", ["total_rejected"], unique=False
    )
    op.drop_index("thikness_from_idx", table_name="acst_table")
    op.drop_index("thikness_before_idx", table_name="acst_table")
    op.drop_index("diameter_from_idx", table_name="acst_table")
    op.drop_index("diameter_before_idx", table_name="acst_table")
    op.drop_index("acst_method_idx", table_name="acst_table")
    op.drop_index("acst_idx", table_name="acst_table")
    op.drop_index("acst_ident_idx", table_name="acst_table")
    op.drop_index("acst_gtd_idx", table_name="acst_table")
    op.drop_table("acst_table")
    # ### end Alembic commands ###