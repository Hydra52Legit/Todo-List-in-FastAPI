from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas
from auth import get_db, get_current_user
from typing import Optional

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("/", response_model=list[schemas.Task])
def get_tasks(
    project_id: Optional[int] = None,
    completed: Optional[bool] = None,
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    query = db.query(models.Task).join(models.Project).filter(models.Project.user_id == current_user.id)
    
    if project_id:
        project = db.query(models.Project).filter(
            models.Project.id == project_id,
            models.Project.user_id == current_user.id
        ).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        query = query.filter(models.Task.project_id == project_id)
    
    if completed is not None:
        query = query.filter(models.Task.completed == completed)
    
    return query.all()

@router.post("/", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    # Проверяем, что проект принадлежит пользователю
    project = db.query(models.Project).filter(
        models.Project.id == task.project_id,
        models.Project.user_id == current_user.id
    ).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    db_task = models.Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.get("/{task_id}", response_model=schemas.Task)
def get_task(task_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    task = db.query(models.Task).join(models.Project).filter(
        models.Task.id == task_id,
        models.Project.user_id == current_user.id
    ).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/{task_id}", response_model=schemas.Task)
def update_task(task_id: int, task_update: schemas.TaskUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    task = db.query(models.Task).join(models.Project).filter(
        models.Task.id == task_id,
        models.Project.user_id == current_user.id
    ).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    update_data = {k: v for k, v in task_update.dict().items() if v is not None}
    for key, value in update_data.items():
        setattr(task, key, value)
    
    db.commit()
    db.refresh(task)
    return task

@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    task = db.query(models.Task).join(models.Project).filter(
        models.Task.id == task_id,
        models.Project.user_id == current_user.id
    ).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(task)
    db.commit()
    return {"ok": True}

@router.patch("/{task_id}/complete")
def complete_task(task_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    task = db.query(models.Task).join(models.Project).filter(
        models.Task.id == task_id,
        models.Project.user_id == current_user.id
    ).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task.completed = True
    db.commit()
    return {"ok": True, "completed": True}