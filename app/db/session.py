# --- Database session for all models ---

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config.core import settings

engine = create_engine(
    settings.DATABASE_URL,
    echo=True,
)

SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)

# Dependency to use in FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()