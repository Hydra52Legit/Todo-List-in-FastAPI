from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class TagBase(BaseModel):
    name: str
    color: Optional[str] = "#808080"  # Hex color code

class TagCreate(TagBase):
    pass

class Tag(TagBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False
    priority: int = 1
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    notes: Optional[str] = None

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    project_id: int 
    tags_ids: Optional[List[int]] = None 

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[int] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    notes: Optional[str] = None
    tag_ids: Optional[List[int]] = None

class Task(TaskBase):
    id: int
    project_id: int
    created_at: datetime
    tags: List[Tag] = []
    
    class Config:
        from_attributes = True
    

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class Project(ProjectBase):
    id: int
    user_id: int
    created_at: datetime
    tasks: List[Task] = []

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    created_at: datetime
    projects: List[Project] = []
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None