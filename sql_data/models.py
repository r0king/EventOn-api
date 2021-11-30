from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


from .database import Base




class User(Base):

    __tablename__ = "users"


    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, primary_key=True, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    
    items = relationship("Sheet", back_populates="owner")
    events = relationship('Event',back_populates='user')


class Sheet(Base):

    __tablename__ = "sheet"


    id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True)
    owner_id = Column(String, ForeignKey("users.email"))

    owner = relationship("User", back_populates="items")
    event = relationship('Event',back_populates='sheet',uselist=False)

class Event(Base):

    __tablename__ = "events"
    sheet_id = Column(ForeignKey('sheet.id') , primary_key=True, index=True)
    email = Column(ForeignKey('users.email') , primary_key=True)
    count = Column(Integer , autoincrement=1)
    name = Column(String)

    sheet = relationship("Sheet",back_populates='event')
    user = relationship("User",back_populates='events')

