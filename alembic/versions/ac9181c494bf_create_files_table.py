"""Create files table

Revision ID: ac9181c494bf
Revises: f893421b714f
Create Date: 2025-03-25 14:45:25.589333

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ac9181c494bf'
down_revision = 'f893421b714f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('files',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('folder_name', sa.String(length=255), nullable=False),
    sa.Column('filename', sa.String(length=255), nullable=False),
    sa.Column('file_type', sa.String(length=100), nullable=True),
    sa.Column('file_size', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_files_id'), 'files', ['id'], unique=False)
    op.alter_column('roles', 'name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_constraint('fk_users_roles', 'users', type_='foreignkey')



def downgrade() -> None:
    op.create_foreign_key('fk_users_roles', 'users', 'roles', ['role_id'], ['id'], ondelete='CASCADE')
    op.alter_column('roles', 'name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.drop_index(op.f('ix_files_id'), table_name='files')
    op.drop_table('files')
