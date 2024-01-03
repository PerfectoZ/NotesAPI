from fastapi import HTTPException
from pydantic import (
    BaseModel,
    validator,
    EmailStr
)
from bson import ObjectId

class UserCreate(BaseModel):
    username: str
    password: str
    email: EmailStr

    @validator("username")
    @classmethod
    def non_empty_title(cls, value: str):
        if not value or value.isspace():
            raise HTTPException(status_code=400, detail="Username cannot be null or blank")
        return value

    @validator("email")
    @classmethod
    def non_empty_email(cls, value: str):
        if not value or value.isspace():
            raise HTTPException(status_code=400, detail="Email cannot be null or blank")
        return value

    @validator("password")
    @classmethod
    def non_empty_password(cls, value: str):
        if not value or value.isspace():
            raise HTTPException(status_code=400, detail="Password cannot be null or blank")
        return value
class UserDB(UserCreate):
    id: ObjectId

    class Config:
        arbitrary_types_allowed = True

class UserLogin(BaseModel):
    username: str
    password: str

    @validator("username")
    @classmethod
    def non_empty_title(cls, value: str):
        if not value or value.isspace():
            raise HTTPException(status_code=400, detail="Username cannot be null or blank")
        return value

    @validator("password")
    @classmethod
    def non_empty_password(cls, value: str):
        if not value or value.isspace():
            raise HTTPException(status_code=400, detail="Password cannot be null or blank")
        return value