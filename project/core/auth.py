from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi  import HTTPException
from datetime import datetime
from project.database import get_db
from project import crud ,schemas,models
#copy
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt,JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

#copy
SECRET_KEY = "55224-7723-#@!%"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 3
REFRESH_TOKEN_EXPIRE_DAYS = 2



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#copy 
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")
#copy
def check_exist_user(db:Session,email_phonenumber:str,password:str): # check the user use  in time login email or phone number
    if '@'in email_phonenumber:
        user=crud.Check_user_email(db,email_phonenumber)
    else:
        user=crud.Check_user_Phone_number(db,email_phonenumber)
    # user=Check_user_email(db,email)
    if not user or not verify_password(password, user.password):
        return False
    return user 
def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=3)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=3)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

#check user for login
def check_exist_user_email(db:Session,email:str):
    user=crud.Check_user_email(db,email)
    return user

#To create Acess token by refersh Token
def get_access_token_use_refresh_token(token:schemas.refresh_Token,db:Session):
  try:
        payload = jwt.decode(token.refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        user=db.query(models.User).filter(models.User.refresh_token==token.refresh_token).first()
        if user:
            user_id = payload.get("sub")
            if user_id is None:
                return HTTPException(status_code=401, detail="Invalid token")
        
            access_token = create_access_token({"sub": user_id})
        
            return {"access_token": access_token}
  
        else:
            raise HTTPException(HTTPException(status_code=401, detail="Invalid token"))
           
    
  except JWTError as e:
        raise HTTPException(status_code=401, detail="Invalid token")

#To get current user
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate the ": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise error
    except JWTError:
        raise error
    user=crud.Check_exist_user_id(db,user_id)
    # user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise error
    return user

#copy
def hash_password(password):
    password = str(password)
    hashed_password = pwd_context.hash(password)
    return hashed_password

def verify_password(plain_password: str, hashed_password: str) :
    return pwd_context.verify(plain_password, hashed_password)

def Check_OTP_valid(db:Session,OTP:str):
    user=crud.Otp_check(db,OTP)
    if not user:
        raise HTTPException(status_code=400,detail="Invalid  OTP")
    if datetime.now() > user.expires_at:
        raise HTTPException(status_code=400, detail="OTP has expired")
    return user