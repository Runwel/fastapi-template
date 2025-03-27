"""Add advanced file management features

Revision ID: 16dee9c26ef4
Revises: 8f1c3cb71322
Create Date: 2025-03-26 14:32:57.238827

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '16dee9c26ef4'
down_revision = '8f1c3cb71322'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('audit_logs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('action', sa.String(length=50), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('file_id', sa.Integer(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['file_id'], ['files.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_audit_logs_id'), 'audit_logs', ['id'], unique=False)
    op.add_column('files', sa.Column('tags', sa.String(length=255), nullable=True))
    op.add_column('files', sa.Column('expiry_link', sa.String(length=255), nullable=True))
    op.add_column('files', sa.Column('updated_at', sa.DateTime(), nullable=True))
    op.alter_column('files', 'version',
               existing_type=sa.INTEGER(),
               nullable=True,
               existing_server_default=sa.text('1'))


def downgrade() -> None:
    op.alter_column('files', 'version',
               existing_type=sa.INTEGER(),
               nullable=False,
               existing_server_default=sa.text('1'))
    op.drop_column('files', 'updated_at')
    op.drop_column('files', 'expiry_link')
    op.drop_column('files', 'tags')
    op.drop_index(op.f('ix_audit_logs_id'), table_name='audit_logs')
    op.drop_table('audit_logs')
