from sqlalchemy import create_engine

from app.core.config import settings
from app.db.models import Base


def create_tables():
    """Create all tables in the database."""
    engine = create_engine(settings.DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    print("All tables created successfully!")


if __name__ == "__main__":
    create_tables()
