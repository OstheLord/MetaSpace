import os
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, scoped_session
from sqlalchemy.exc import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import logging

# Logging Configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///virtual_space.db")

engine = create_engine(DATABASE_URL, echo=True, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password. hash, password)

    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}')>"

class Room(Base):
    __tablename__ = 'rooms'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    creator_id = Column(Integer, ForeignKey('users.id'))
    creator = relationship("User", back_populates="created_rooms")
    interactive_elements = Column(String, nullable=True)
    capacity = Column(Integer, default=10)
    status = Column(String, default="open", nullable=False)

User.created_rooms = relationship("Room", order_by=Room.id, back_populates="creator")

Base.metadata.create_all(engine)

def db_session():
    """Context manager for database session."""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

def add_user(username, email, password):
    with db_session() as session:
        try:
            new_user = User(username=username, email=email)
            new_user.set_password(password)
            session.add(new_user)
        except SQLAlchemyError as e:
            logger.error(f"Error adding user: {e}")
            raise

def main():
    # Example usage
    try:
        add_user("Test", "test@example.com", "securepassword123")
        logging.info("User added successfully.")
    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()