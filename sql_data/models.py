from typing import List
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from passlib.hash import bcrypt

from .database import Base




class User(Base):

    __tablename__ = "users"

    email = Column(String, primary_key=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    
    items = relationship("Sheet", back_populates="owner")
    events = relationship("Event", back_populates="owner")
    
    def verify_password(self,password):
        return bcrypt.verify(password, self.hashed_password)
    
class Sheet(Base):

    __tablename__ = "sheet"


    id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True)
    owner_id = Column(String, ForeignKey("users.email"))

    owner = relationship("User", back_populates="items")
    event = relationship('Event',back_populates='sheet')

class Event(Base):

    __tablename__ = "events"
    sheet_id = Column(String, ForeignKey('sheet.id') , primary_key=True, index=True)
    name = Column(String)
    email = Column(String, ForeignKey("users.email"))

    owner = relationship("User", back_populates="events")
    sheet = relationship("Sheet",back_populates='event')
