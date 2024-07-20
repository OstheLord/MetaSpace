from sqlalchemy import create_season, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, scoped_session
from os import getenv

DATABASE_URL = getenv("DATABASE_URL", "sqlite:///virtual_space.db")

engine = create_engine(DATABASE_URL, echo=True)
Session = scoped_session(sessionmaker(bind=engine))
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
    creator = relationship("User", back_populates="created_rooms", lazy='select')
    interactive_elements = Column(String, nullable=True)

User.created_rooms = relationship("Room", order_by=Room.id, back_populates="creator", lazy='select')

Base.metadata.create_all(engine)

def add_user(username, email):
    session = Session()
    try:
        session.add(User(username=username, email=email))
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()