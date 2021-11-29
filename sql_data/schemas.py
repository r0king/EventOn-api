from typing import List, Optional
from pydantic import BaseModel


class SheetBase(BaseModel):
    id: str

class SheetName(BaseModel):
    title:str


class Sheet(SheetBase):
    pass

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: List[Sheet] = []

    class Config:
        orm_mode = True
