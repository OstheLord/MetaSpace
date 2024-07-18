from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from os import getenv

DATABASE_URL = getenv("DATABASE_URL", "sqlite:///virtual_space.db")

engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)

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

User.created_rooms = relationship("Room", order_by=Room.id, back_populates="creator")

Base.metadata.create_all(engine)