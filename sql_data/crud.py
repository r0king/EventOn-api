from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import user

from . import models, schemas

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_sheets_of_user(db:Session, user:schemas.UserBase):
    # return db.query(models.Sheet).filter(models.Sheet.owner_id == user.email).all()
    return db.query(models.Sheet).limit(10).all()

def get_sheets_by_id(db:Session, id:str):
    return db.query(models.Sheet).filter(models.Sheet.id == id).all()

def create_user(db:Session,user:schemas.UserCreate):
    sample_hashed_pass = user.password + 'abcd'
    new_user = models.User(email = user.email,hashed_password = sample_hashed_pass)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def create_sheet(db:Session,sheet:schemas.SheetName,user_id:str):
    
    new_sheet = models.Sheet(**sheet.dict(),owner_id=user_id)
    db.add(new_sheet)
    db.commit()
    db.refresh(new_sheet)
    return new_sheet