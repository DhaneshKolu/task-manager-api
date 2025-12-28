from pydantic import BaseModel,EmailStr
from typing import Optional

class UserBase(BaseModel):
    email : EmailStr

class UserCreate(UserBase):
    password:str

class UserOut(UserBase):
    id : int

    class config:
        orm_mode=True

class TaskBase(BaseModel):
    title:str
    description:Optional[str]=None
    completed : bool=False

class TaskCreate(TaskBase):
    pass

class TaskOut(TaskBase):
    id:int
    owner_id:int

    class config:
        orm_mode=True
