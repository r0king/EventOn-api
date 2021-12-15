from datetime import timedelta,datetime
from typing import Optional
import jwt

SECRET_KEY = "09d25e0s1ucu9k3m2y3d8icc2ktgwefrew3syf0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

def access_token(user_id:str):
    
    ACCESS_TOKEN_EXPIRE_MINUTES = 300
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    token = create_access_token({"user id":user_id},expires_delta=access_token_expires)
    return {
        'access_token':token,
        'token_type' : 'bearer'
    }

def decode_jwt(token:str):

    return jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):

    
    ALGORITHM = "HS256"

    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
        
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

