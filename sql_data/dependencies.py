from sqlalchemy.orm import Session
from sql_data.crud import get_user
from .models import User

def authenticate_user(db:Session ,username: str, password: str):
    user = get_user(db,user_id=username)
    if not user:
        return False 
    if not user.verify_password(password):
        return False
    return user