
import os
from fastapi.params import Body
from typing import List, Optional
<<<<<<< HEAD
from fastapi import FastAPI,Request,Depends,HTTPException
from plugins.sheetAccess.sheets import create_google_sheet
from sqlalchemy.orm import Session

from sql_data import crud, models, schemas
from sql_data.database import SessionLocal, engine
models.Base.metadata.create_all(bind=engine)
=======
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from fastapi import FastAPI,Request,Depends,HTTPException,status
from api_functions.secure import access_token, decode_jwt
from plugins.sheetAccess.sheets import create_google_sheet
from sqlalchemy.orm import Session
import jwt
from sql_data import crud, models, schemas
from sql_data.database import SessionLocal, engine
from sql_data.dependencies import authenticate_user
models.Base.metadata.create_all(bind=engine)
from datetime import datetime, timedelta
>>>>>>> dev

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# @app.get("/users/", response_model=List[schemas.User])
# def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     users = crud.get_users(db, skip=skip, limit=limit)
#     return users

<<<<<<< HEAD
#create new  user
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
=======
oauth_scheme = OAuth2PasswordBearer(tokenUrl='token')

async def get_current_user(db: Session = Depends(get_db),token: str = Depends(oauth_scheme)):
    try:
        payload = decode_jwt(token=token)
        user = crud.get_user(db=db,user_id=payload.get('user id'))
        if not user:
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Invalid user'
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Invalid username or password'
        )

    return user

@app.post('/token')
def get_token(form :OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):
    user = authenticate_user(db,username=form.username,password=form.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Invalid username or password'
        )
    return access_token(user_id=user.email)

@app.get('/')
async def index():
    return {
         "name": "Coverkin",
        "description": "Symertry SSO general API",
        "version": "0.0.1",
        "origin": "Float Business Accelerator",
        "team": "Monsoon '21 Batch"
    }

#create new  user
@app.post("/users/", response_model=schemas.User)
def create_user(
            user: schemas.UserCreate,
            db: Session = Depends(get_db)):
>>>>>>> dev
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.get("/events/", response_model=List[schemas.Event])
<<<<<<< HEAD
def get_events(email: str, db: Session = Depends(get_db)):
=======
def get_events(
                email: str,
                user:schemas.User = Depends(get_current_user),
                token:str = Depends(oauth_scheme),
                db: Session = Depends(get_db)):
>>>>>>> dev
    
    events = crud.get_events(db, email=email)
    return events

#create new  event
@app.post("/events/",response_model=schemas.Event)
def create_events(
                email:str,
                event_name:str,
                title: Optional[str],
<<<<<<< HEAD
                sheet: Optional[ schemas.SheetBase  ] = None ,
=======
                sheet: Optional[ schemas.SheetBase  ] = None,
                token:str = Depends(oauth_scheme) ,
>>>>>>> dev
                db: Session = Depends(get_db)):
    
    user_events = crud.get_user_event_by_name(db,name=event_name,email=email)
    if user_events:
        raise HTTPException(status_code=409, detail="Event Name Already Exists")
    
    if sheet is None:
        sheet = schemas.SheetBase
        newspreadsheet = create_google_sheet(user_id=email,sheet_name=title)
        sheet.id = newspreadsheet["spreadsheetId"]
        title = newspreadsheet["properties"]
        title = title['title']
        
        user_sheets = crud.get_sheet_by_id(db,id=sheet.id )
        if user_sheets:
            raise HTTPException(status_code=409, detail="Sheet Already Exists")
        
        crud.create_sheet(
                db,
                id=sheet.id,
                user_id=email)

    else:
        user_sheets = crud.get_sheet_by_id(db,id=sheet.id)
        if not user_sheets:
            raise HTTPException(status_code=404, detail="Sheet not found")
            
    return crud.create_event(db, email=email, name=event_name, sheet_id=sheet.id )

@app.delete('/events/',response_model=schemas.Event)
def delelte_events(
        id: str,
        token:str = Depends(oauth_scheme),
        db :Session=Depends(get_db)
        
    ):
    return crud.delete_sheet(db,id)


@app.get("/sheets/{email}", response_model=List[schemas.SheetFull])
def get_sheet(
    email:str,
    token:str = Depends(oauth_scheme),
    db: Session = Depends(get_db)):
    user_sheets = crud.get_sheets_of_user(db,email=email )
    return user_sheets

#create new  sheet
@app.post("/sheets/",response_model=schemas.SheetFull)
def create_sheet(
        sheet: schemas.SheetName,
        user_id:str, 
        token:str = Depends(oauth_scheme),
        db: Session = Depends(get_db)):
    user_sheets = crud.get_sheet_by_id(db,id=sheet.id )
    if user_sheets:
        raise HTTPException(status_code=409, detail="Sheet Already Exists")
    return crud.create_sheet(
                db,
                id=sheet.id,
                user_id=user_id)
