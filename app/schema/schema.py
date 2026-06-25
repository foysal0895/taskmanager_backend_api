import datetime
from pydantic import BaseModel

class UserRegisterRequest(BaseModel):
    first_name:str
    last_name:str
    email:str
    phone:str
    password:str


class UserRegisterResponse(BaseModel):
    id:int
    first_name: str
    last_name:str
    email:str
    phone:str
    created_at:str
    updated_at:str


class UserLoginRequest(BaseModel):
    email:str
    password:str


class UserLoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"



class TaskCreateRequest(BaseModel):
    title: str
    description: str | None = None


class TaskUpdateRequest(BaseModel):
    title: str
    description: str

class TaskStatusUpdateRequest(BaseModel):
    status: str


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    status: str

    class Config:
        from_attributes = True