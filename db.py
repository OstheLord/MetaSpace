from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Fetch the database connection URL from environment variables
DATABASE_CONNECTION_URL = os.getenv("DATABASE_URL")

# Create an SQLAlchemy engine for connecting to the database
database_engine = create_engine(DATABASE_CONNECTION_URL)

# Create a configured "Session" class for database session operations
DatabaseSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=database_engine)