from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(String, primary_key=True, index=True)
    token = Column(String)
    uid = Column(String)
    displayName = Column(String)
    email = Column(String)
    photoURL = Column(String)