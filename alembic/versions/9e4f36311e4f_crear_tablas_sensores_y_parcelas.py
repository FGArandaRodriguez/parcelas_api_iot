"""crear tablas sensores y parcelas

Revision ID: 9e4f36311e4f
Revises: 
Create Date: 2025-03-24 10:03:00.588623

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9e4f36311e4f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('parcelas',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('parcela_id', sa.Integer(), nullable=True),
    sa.Column('nombre', sa.Text(), nullable=True),
    sa.Column('ubicacion', sa.Text(), nullable=True),
    sa.Column('responsable', sa.Text(), nullable=True),
    sa.Column('tipo_cultivo', sa.Text(), nullable=True),
    sa.Column('latitud', sa.Numeric(), nullable=True),
    sa.Column('longitud', sa.Numeric(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_parcelas_parcela_id'), 'parcelas', ['parcela_id'], unique=True)
    op.create_table('sensor_nodo_general',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('humedad', sa.Numeric(), nullable=True),
    sa.Column('temperatura', sa.Numeric(), nullable=True),
    sa.Column('lluvia', sa.Integer(), nullable=True),
    sa.Column('sol', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sensor_parcela_historico',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('parcela_id', sa.Integer(), nullable=True),
    sa.Column('humedad', sa.Numeric(), nullable=True),
    sa.Column('temperatura', sa.Numeric(), nullable=True),
    sa.Column('lluvia', sa.Integer(), nullable=True),
    sa.Column('sol', sa.Integer(), nullable=True),
    sa.Column('ultimo_riego', sa.TIMESTAMP(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['parcela_id'], ['parcelas.parcela_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sensor_parcela_historico')
    op.drop_table('sensor_nodo_general')
    op.drop_index(op.f('ix_parcelas_parcela_id'), table_name='parcelas')
    op.drop_table('parcelas')
    # ### end Alembic commands ###
