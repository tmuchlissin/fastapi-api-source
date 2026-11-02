"""rename posts to articles, rename content to body, add views

Revision ID: cc81b4179258
Revises: 95c4831965f6
Create Date: 2026-11-03 00:16:12.198951

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cc81b4179258'
down_revision: Union[str, Sequence[str], None] = '95c4831965f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # 1. Rename table 'posts' to 'articles'
    op.rename_table('posts', 'articles')
    # 2. Rename column 'content' to 'body' in the new 'articles' table
    op.alter_column('articles', 'content', new_column_name='body')
    # 3. Add new column 'views' with default 0
    op.add_column('articles', sa.Column('views', sa.Integer(), server_default='0', nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    # Reverse everything in opposite order:
    # 3. Drop the added 'views' column
    op.drop_column('articles', 'views')
    # 2. Rename 'body' back to 'content'
    op.alter_column('articles', 'body', new_column_name='content')
    # 1. Rename 'articles' back to 'posts'
    op.rename_table('articles', 'posts')
