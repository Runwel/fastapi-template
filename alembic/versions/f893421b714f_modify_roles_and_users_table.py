"""Modify roles and users table

Revision ID: f893421b714f
Revises: fd628fcbabe7
Create Date: 2025-03-25 07:00:26.238074

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f893421b714f'
down_revision = 'fd628fcbabe7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Alter the 'name' column in roles to be NOT NULL
    op.alter_column('roles', 'name', existing_type=sa.String(), nullable=False)
    
    # Ensure role_id in users has a proper foreign key constraint
    op.create_foreign_key(
        'fk_users_roles', 'users', 'roles', ['role_id'], ['id'], ondelete='CASCADE'
    )


def downgrade() -> None:
    # Revert role_id foreign key constraint change
    op.drop_constraint('fk_users_roles', 'users', type_='foreignkey')
    
    # Revert the change to the 'name' column in roles
    op.alter_column('roles', 'name', existing_type=sa.String(), nullable=True)