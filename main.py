from __future__ import print_function
from google_auth_oauthlib.flow import Flow

from typing import List, Optional
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from fastapi import FastAPI,Request,Depends,HTTPException,status,Response,Cookie
from api_functions.secure import access_token, decode_jwt
from plugins.gmail.mail import send_mapped_message, send_message
from plugins.sheetAccess.sheets import create_google_sheet, get_clean_sheet
from sqlalchemy.orm import Session
from sql_data import crud, models, schemas
from sql_data.database import SessionLocal, engine
from sql_data.dependencies import authenticate_user


models.Base.metadata.create_all(bind=engine)

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
# get app details

@app.get('/')
async def index():
    return {
         "name": "Coverkin",
        "description": "",
        "version": "0.0.1",
        "team": ""
    }

# token creation endpoint 
@app.post('/token')
def get_token(form :OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):
    user = authenticate_user(db,username=form.username,password=form.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Invalid username or password'
        )
    return access_token(user_id=user.email)

#create new  user
@app.post("/user/", response_model=schemas.User)
def create_user(
            user: schemas.UserCreate,
            db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


# return all events of current user
@app.get("/events/", response_model=List[schemas.Event])
def get_events( 
                user:schemas.User = Depends(get_current_user),
                token: str = Depends(oauth_scheme),
                db: Session = Depends(get_db)):

    events = crud.get_events(db, email=user.email)
    return events

#create new  event
@app.post("/event/",response_model=schemas.Event)
def create_events(
                event_name:str,
                title: Optional[str],
                sheet: Optional[ schemas.SheetBase  ] = None,
                user:schemas.User = Depends(get_current_user),
                token:str = Depends(oauth_scheme) ,
                db: Session = Depends(get_db)):

    #checks similar event name

    user_events = crud.get_user_event_by_name(db,name=event_name,email=user.email)

    if user_events:
        raise HTTPException(status_code=409, detail="Event Name Already Exists")
    
    #if sheet id is given in the api call

    if sheet is None:
        sheet = schemas.SheetBase
        newspreadsheet = create_google_sheet(user_id=user.email,sheet_name=title)
        sheet.id = newspreadsheet["spreadsheetId"]
        title = newspreadsheet["properties"]
        title = title['title']
        
        user_sheets = crud.get_sheet_by_id(db,id=sheet.id )
        if user_sheets:
            raise HTTPException(status_code=409, detail="Sheet Already Exists")
        
        # create sheet in database
        crud.create_sheet(
                db,
                id=sheet.id,
                user_id=user.email)

    else:
        user_sheets = crud.get_sheet_by_id(db,id=sheet.id)
        if not user_sheets:
            raise HTTPException(status_code=404, detail="Sheet not found")
            
    return crud.create_event(db, email=user.email, name=event_name, sheet_id=sheet.id )

# get sheet data
@app.post('/event/sheet/{id}')
def get_sheet_data(
        id: str,
        # colums that are used 
        colums_used : List[int],
        token:str = Depends(oauth_scheme),
        user:schemas.User = Depends(get_current_user),
        # db :Session=Depends(get_db)
        ):

    return get_clean_sheet(user_id=user.email,sheet_id=id,columns_used=colums_used)

# Send Mass mail
@app.post('/event/mail/mass/{id}')
def send_mass_mail(
        mail_id:str,
        mail : schemas.Mail,        
        token:str = Depends(oauth_scheme),
        # user:schemas.User = Depends(get_current_user),
        db :Session=Depends(get_db)):
 
    return send_message(to=mail.recivers_address,subject=mail.subject,user_id=mail_id,message=mail.mail_content)

# Send mapped mail
@app.post('/event/mail/mapped/{id}')
def send_mapped_mail(
        #mail id in which user sends mail
        mail_id:str,        
        mail : schemas.MailBase, 
        sheet: schemas.Sheet_Details,       
        token:str = Depends(oauth_scheme),
        user:schemas.User = Depends(get_current_user),
        db :Session=Depends(get_db)):
    
    sheet_data = get_clean_sheet(user_id=user.email,sheet_id=sheet.sheet_id,columns_used=sheet.colums_used)    
    return send_mapped_message(
            subject=mail.subject,
            user_id=mail_id,
            message=mail.mail_content,
            map_data=sheet_data,
            mail_col=sheet.mail_col
            )
            

# delete a given event
@app.delete('/event/',response_model=schemas.Event)
def delelte_events(
        id: str,
        token:str = Depends(oauth_scheme),
        user:schemas.User = Depends(get_current_user),
        db :Session=Depends(get_db)
        
    ):
    
    return crud.delete_sheet(db,id,user_id=user.email)

# get sheets of user
@app.get("/sheet/{email}", response_model=List[schemas.SheetFull])
def get_sheet(
    email:str,
    token:str = Depends(oauth_scheme),
    db: Session = Depends(get_db)):
    user_sheets = crud.get_sheets_of_user(db,email=email )
    return user_sheets

#create new  sheet
@app.post("/sheet/",response_model=schemas.SheetFull)
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

SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

@app.get('/oauth2callback')
def oauth2callback_for_google(
                state:str,
                code:str,
                scope:str,
                request: Request
                ):
    CLIENT_SECRETS_FILE = 'plugins/googleapi/Credentials/keys.json'
    flow = Flow.from_client_secrets_file(
      CLIENT_SECRETS_FILE, scopes=None, state=state)
    
    flow.redirect_uri = request.url_for('oauth2callback_for_google')
    flow.fetch_token(code=code)
    credentials = flow.credentials
    return {"Authentication complete":credentials}


#test drive api
@app.get("/drive/")
def create_drive(
    request: Request,
    response:Response
):
    CLIENT_SECRETS_FILE = 'plugins/googleapi/Credentials/keys.json'
    API_SERVICE_NAME = 'drive'
    API_VERSION = 'v2'
    flow = Flow.from_client_secrets_file(
      CLIENT_SECRETS_FILE, scopes=SCOPES)
    flow.redirect_uri = request.url_for('oauth2callback_for_google')
      # Enable offline access so that you can refresh an access token without
      # re-prompting the user for permission. Recommended for web server apps.
      # Enable incremental authorization. Recommended as a best practice.
    authorization_url, state = flow.authorization_url(
      access_type='offline',
      include_granted_scopes='true')

    response.set_cookie(key="state", value=state)
    return {
            'redirect_url':authorization_url
            }


