from fastapi import FastAPI,APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from app import models,schemas
from app.database import get_db
from app.auth import hash_password
from fastapi.security import OAuth2PasswordRequestForm
from app.auth import create_access_token,verify_password

router = APIRouter()

@router.get("/")
def users_health():
    return {"message":"Users router is working"}

@router.post("/",response_model=schemas.UserOut,status_code=status.HTTP_201_CREATED)
def create_user(user:schemas.UserCreate,db:Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(
        models.User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail = "Email already registered"
        )
    
    new_user = models.User(
        email = user.email,
        hashed_password = hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.post("/login")
def login(form_data:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.email==form_data.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credentials"
        )
    if not verify_password(form_data.password,user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credentials"
        )
    access_token = create_access_token(data={"user_id":user.id})
    print("FORM USERNAME:", form_data.username)
    print("FORM PASSWORD:", form_data.password)


    return {"access_token":access_token,"token_type":"bearer"}

from app.auth import get_current_user

@router.get("/me", response_model=schemas.UserOut)
def read_current_user(current_user = Depends(get_current_user)):
    return current_user
