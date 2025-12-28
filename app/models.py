from sqlalchemy import Column,String,Integer,Boolean,ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key = True,index=True)
    email = Column(String,index=True,nullable = False)
    hashed_password = Column(String,nullable = False)

    tasks = relationship("Task",back_populates="owner")

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer,primary_key=True,index=True)
    title = Column(String,index=True)
    description = Column(String,nullable=True)
    completed = Column(String,nullable=False)


    owner_id = Column(Integer,ForeignKey("users.id"))

    owner = relationship("User",back_populates="tasks")