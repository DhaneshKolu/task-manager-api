from passlib.context import CryptContext
from datetime import datetime,timedelta,timezone
from jose import JWTError, jwt

from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from fastapi import Depends,HTTPException,status
from app import models

oauth2_secure = OAuth2PasswordBearer(tokenUrl="/users/login")

SECRET_KEY = "g712h9127921hiq02178212yfvtr51r278272"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRY_TIME = 30

pwd_context = CryptContext(schemes=["argon2"],deprecated = "auto")


def hash_password(password:str)->str:
    return pwd_context.hash(password)

def verify_password(plain_password,hashed_password)->bool:
    return pwd_context.verify(plain_password,hashed_password)

def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEN_EXPIRY_TIME)
    to_encode.update({"exp":expire})
    jwt_encoded = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return jwt_encoded

def get_current_user(
        token:str=Depends(oauth2_secure),
        db:Session = Depends(get_db)
):
    credentials_exceptions = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate":"Bearer"}
    )

    try:
        to_decode = jwt.decode(token,SECRET_KEY,algorithms = [ALGORITHM])
        payload = to_decode
        user_id:int = payload.get("user_id")
        if user_id is None:
            raise credentials_exceptions
    except JWTError:
        raise credentials_exceptions
    
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise credentials_exceptions
    return user
