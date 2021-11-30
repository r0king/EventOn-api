
import os
from fastapi.params import Body
from typing import List, Optional
from fastapi import FastAPI,Request,Depends,HTTPException
from plugins.sheetAccess.sheets import NewSheet
from sqlalchemy.orm import Session

from sql_data import crud, models, schemas
from sql_data.database import SessionLocal, engine
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

#create new  user
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.get("/events/", response_model=List[schemas.Event])
def get_events(email: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    
    events = crud.get_events(db, email=email)
    return events

#create new  event
@app.post("/events/", response_model=List[schemas.Sheet])
def create_events(
                sheet: schemas.SheetBase,
                user_id:str,
                event_name:str,
                db: Session = Depends(get_db)):

    user_sheets = crud.get_sheet_by_id(db,id=sheet.id)
    if not user_sheets:
        raise HTTPException(status_code=400, detail="Sheet Not Created")

    return crud.create_event(db,sheet_id=sheet.id,name=event_name,email=user_id)

@app.get("/sheets/{email}", response_model=List[schemas.SheetFull])
def get_sheet(email:str,db: Session = Depends(get_db)):
    user_sheets = crud.get_sheets_of_user(db,email=email )
    return user_sheets

#create new  sheet
@app.post("/sheets/",response_model=schemas.SheetFull)
def create_sheet(sheet: schemas.SheetName, user_id:str, db: Session = Depends(get_db)):
    user_sheets = crud.get_sheet_by_id(db,id=sheet.id )
    if user_sheets:
        raise HTTPException(status_code=400, detail="Sheet Already Exists")
    return crud.create_sheet(db,sheet=sheet,user_id=user_id)


# @app.get("/create-sheet/")
# def read_root(user_id:str,request: Request, db: Session = Depends(get_db)):

#     newspreadsheet = NewSheet(user_id=user_id,sheet_name='Student List')
#     return newspreadsheet
