from typing import List, Optional
from pydantic import BaseModel


class SheetBase(BaseModel):
    id: str

class SheetName(SheetBase):
    title:str


class Sheet(SheetBase):
    pass

class SheetFull(SheetBase):
    owner_id :str

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    is_active: bool
    sheets: List[Sheet] = []

    class Config:
        orm_mode = True

class EventBase(BaseModel):
    name :str

class EventSheet(EventBase):
    sheet_id : str

class Event(EventSheet):
    email : str

    class Config:
        orm_mode = True


class Mail(BaseModel):

    recivers_address : List[str] = None
    subject : str
    mail_content : str
