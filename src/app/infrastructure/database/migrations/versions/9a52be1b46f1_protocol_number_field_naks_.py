"""protocol_number field for personal_naks_certifiaction_table

Revision ID: 9a52be1b46f1
Revises: fb7f3c8fa601
Create Date: 2024-12-16 13:40:22.262418

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "9a52be1b46f1"
down_revision: Union[str, None] = "fb7f3c8fa601"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "personal_naks_certification_table",
        sa.Column("protocol_number", sa.String(), nullable=False),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("personal_naks_certification_table", "protocol_number")
    # ### end Alembic commands ###