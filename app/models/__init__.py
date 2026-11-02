# --- Model import from app/models/ - to be imported by alembic env.py ---

from app.models.user import User
from app.models.post import Post
 
__all__ = ["User", "Post"]