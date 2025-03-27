"""Add versioning to files

Revision ID: 8f1c3cb71322
Revises: ac9181c494bf
Create Date: 2025-03-26 07:41:23.744991

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8f1c3cb71322'
down_revision = 'ac9181c494bf'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # ✅ Create the files table with advanced features
    op.create_table(
        'files',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('folder_name', sa.String(255), nullable=False),
        sa.Column('filename', sa.String(255), nullable=False),
        sa.Column('file_type', sa.String(100), nullable=True),
        sa.Column('file_size', sa.Integer, nullable=True),
        sa.Column('version', sa.Integer, default=1, nullable=False),                      # Versioning
        sa.Column('tags', sa.ARRAY(sa.String(50)), nullable=True),                        # Tags
        sa.Column('expiry_date', sa.DateTime(), nullable=True),                           # Expiry Links
        sa.Column('created_at', sa.DateTime(), default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), default=sa.func.now(), onupdate=sa.func.now()), 
        sa.Column('user_id', sa.Integer, nullable=False),                                 # User authentication
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE')            # FK constraint
    )

    # ✅ Create the audit log table
    op.create_table(
        'file_audit_logs',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('file_id', sa.Integer, nullable=False),
        sa.Column('user_id', sa.Integer, nullable=False),
        sa.Column('action', sa.String(50), nullable=False),                               # upload, download, delete
        sa.Column('timestamp', sa.DateTime(), default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['file_id'], ['files.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE')
    )

    # ✅ Create necessary indexes
    op.create_index('ix_files_folder_name', 'files', ['folder_name'])
    op.create_index('ix_files_filename', 'files', ['filename'])
    op.create_index('ix_files_tags', 'files', ['tags'], postgresql_using='gin')
    op.create_index('ix_files_created_at', 'files', ['created_at'])
    op.create_index('ix_audit_logs_timestamp', 'file_audit_logs', ['timestamp'])


def downgrade() -> None:
    # ✅ Rollback: Drop the tables and indexes
    op.drop_index('ix_files_folder_name', table_name='files')
    op.drop_index('ix_files_filename', table_name='files')
    op.drop_index('ix_files_tags', table_name='files')
    op.drop_index('ix_files_created_at', table_name='files')
    op.drop_index('ix_audit_logs_timestamp', table_name='file_audit_logs')

    op.drop_table('file_audit_logs')
    op.drop_table('files')
