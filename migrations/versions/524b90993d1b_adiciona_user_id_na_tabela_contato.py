"""Adiciona user_id na tabela contato

Revision ID: 524b90993d1b
Revises: d0e3a054cae4
Create Date: 2026-08-20 04:33:46.392675
"""

from alembic import op
import sqlalchemy as sa


revision = '524b90993d1b'
down_revision = 'd0e3a054cae4'
branch_labels = None
depends_on = None


def upgrade():


    with op.batch_alter_table('contato', schema=None) as batch_op:

        batch_op.add_column(
            sa.Column('user_id', sa.Integer(), nullable=False)
        )

        batch_op.create_foreign_key(
            'fk_contato_user_id',
            'user',
            ['user_id'],
            ['id']
        )

    with op.batch_alter_table('user', schema=None) as batch_op:

        batch_op.create_unique_constraint(
            'uq_user_email',
            ['email']
        )


def downgrade():

    with op.batch_alter_table('user', schema=None) as batch_op:

        batch_op.drop_constraint(
            'uq_user_email',
            type_='unique'
        )

    with op.batch_alter_table('contato', schema=None) as batch_op:

        batch_op.drop_constraint(
            'fk_contato_user_id',
            type_='foreignkey'
        )

        batch_op.drop_column('user_id')

    op.drop_table('post')