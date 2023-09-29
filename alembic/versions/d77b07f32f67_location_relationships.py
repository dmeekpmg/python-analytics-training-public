"""location relationships

Revision ID: d77b07f32f67
Revises: 8ae23a4a47f9
Create Date: 2023-09-20 11:12:32.561961

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd77b07f32f67'
down_revision: Union[str, None] = '8ae23a4a47f9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('locations', schema=None) as batch_op:
        batch_op.create_foreign_key("locations_route_id", 'routes', ['route_id'], ['id'])
        batch_op.create_foreign_key("locations_trip_id", 'trips', ['trip_id'], ['id'])

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('locations', schema=None) as batch_op:
        batch_op.drop_constraint("locations_route_id", type_='foreignkey')
        batch_op.drop_constraint("locations_trip_id", type_='foreignkey')

    # ### end Alembic commands ###