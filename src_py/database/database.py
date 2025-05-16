from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
from contextlib import contextmanager
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Get database URL from environment variable or use SQLite as default
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///agentverse.db')

# Create engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@contextmanager
def get_db() -> Session:
    """
    Context manager for database sessions.
    Usage:
        with get_db() as db:
            db.query(...)
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

def init_db():
    """Initialize the database by creating all tables."""
    from .models import Base
    Base.metadata.create_all(bind=engine)

# Initialize database tables
init_db()

# Create a new bounty
if __name__ == "__main__":
    from src_py.database.repository import BountyRepository
    bounty = BountyRepository.create(
        sponsor_address="0x...",
        reward=1.0,
        deadline=int(datetime.utcnow().timestamp()) + 86400  # 24 hours from now
    )

    # Get active bounties
    active_bounties = BountyRepository.get_active() 