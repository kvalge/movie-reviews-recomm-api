"""Add countries table and cast_and_crew_countries junction table

Revision ID: add_countries_cast_crew
Revises: d1e2f3a4b5c6
Create Date: 2025-01-16 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'add_countries_cast_crew'
down_revision: Union[str, Sequence[str], None] = 'd1e2f3a4b5c6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create countries table
    op.create_table('countries',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('code', sa.String(length=2), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('code')
    )
    op.create_index(op.f('ix_countries_id'), 'countries', ['id'], unique=False)
    op.create_index(op.f('ix_countries_code'), 'countries', ['code'], unique=False)
    
    # Create cast_and_crew_countries junction table
    op.create_table('cast_and_crew_countries',
        sa.Column('cast_and_crew_id', sa.Integer(), nullable=False),
        sa.Column('country_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['cast_and_crew_id'], ['cast_and_crew.id'], ),
        sa.ForeignKeyConstraint(['country_id'], ['countries.id'], ),
        sa.PrimaryKeyConstraint('cast_and_crew_id', 'country_id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('cast_and_crew_countries')
    op.drop_index(op.f('ix_countries_code'), table_name='countries')
    op.drop_index(op.f('ix_countries_id'), table_name='countries')
    op.drop_table('countries') 