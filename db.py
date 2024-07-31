from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
import os
from contextlib import contextmanager

# Load environment variables from .env file
load_dotenv()

# Fetch the database connection URL from environment variables
DATABASE_CONNECTION_URL = os.getenv("DATABASE_URL")

# Create an SQLAlchemy engine for connecting to the database
database_engine = create_engine(DATABASE_CONNECTION_URL)

# Create a configured "Session" class for database session operations
DatabaseSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=database_engine)

@contextmanager
def db_session():
    """Provide a transactional scope around a series of operations."""
    session = DatabaseSessionLocal()
    try:
        yield session
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        print(f"An error occurred: {e}")
    finally:
        session.close()

# Example usage:
# with db_session() as session:
#    result = session.query(YourModel).filter(YourModel.id == some_id).first()