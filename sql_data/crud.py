from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import user

from . import models, schemas

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_sheet_of_user(db:Session, user:schemas.UserBase):
    return db.query(models.Sheet).filter(models.Sheet.owner_id == user.id).all()

def create_user(db:Session,user:schemas.UserCreate):
    sample_hashed_pass = user.password + 'abcd'
    new_user = models.User(email = user.email,hashed_password = sample_hashed_pass)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def create_sheet(db:Session,sheet:schemas.Sheet,user_id:str):
    
    new_sheet = models.User(**sheet.dict(),owner_id=user_id)
    db.add(new_sheet)
    db.commit()
    db.refresh(new_sheet)
    return new_sheet