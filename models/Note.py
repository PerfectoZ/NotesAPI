from fastapi import HTTPException
from pydantic import (
    BaseModel,
    field_validator
)
from typing import Optional

class NoteCreate(BaseModel):
    title: Optional[str] = None
    body: Optional[str] = None

    @field_validator("title", mode='before')
    @classmethod
    def non_empty_title(cls, value: str):
        if not value or value.isspace():
            raise HTTPException(status_code=400, detail="Title cannot be null or blank")
        return value

    @field_validator("body", mode='before')
    @classmethod
    def non_empty_body(cls, value: str):
        if not value or value.isspace():
            raise HTTPException(status_code=400, detail="Body cannot be null or blank")
        return value

class NoteUpdate(NoteCreate):
    pass

class NoteDB(NoteCreate):
    id: int
