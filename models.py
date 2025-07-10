from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Models cho Authentication
class UserRegister(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Models cho Task
class TaskBase(BaseModel):
    title: str

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    completed: Optional[bool] = None

class Task(TaskBase):
    id: int
    user_id: int
    completed: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Models cho Response
class TaskListResponse(BaseModel):
    tasks: list[Task]
    total: int
    limit: int
    offset: int 