from fastapi import APIRouter,Depends,HTTPException,status
from app import schemas
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import get_current_user
from app import models
router = APIRouter()
@router.post("/",response_model=schemas.TaskOut)
def create_task(
    task:schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    new_task = models.Task(**task.model_dump(),owner_id=current_user.id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@router.get("/",response_model=list[schemas.TaskOut])

def get_tasks(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return db.query(models.Task).filter(
            models.Task.owner_id == current_user.id
        ).all()

@router.put("/{task_id}",response_model=schemas.TaskOut)

def tasks_update(
    task_id:int,
    task:schemas.TaskCreate,
    db: Session=Depends(get_db),
    current_user = Depends(get_current_user)
):
    db_task = db.query(models.Task).filter(
        models.Task.id == task_id
    ).first()

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Task not found"
        )
    if db_task.owner_id != current_user.id:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail= "Not authorized to update this task"
        )
    for key,value in task.model_dump().items():
        setattr(db_task,key,value)

    db.commit()
    db.refresh(db_task)
    return db_task

@router.delete("/{task_id}",status_code = status.HTTP_204_NO_CONTENT)

def task_delete(
    task_id:int,
    db:Session=Depends(get_db),
    current_user = Depends(get_current_user)
):
    task_db = db.query(models.Task).filter(
        models.Task.id == task_id
    ).first()

    if not task_db:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Task not found"
        )
    if task_db.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorised to delete this task"
        )
    
    db.delete(task_db)
    db.commit()
    return
         