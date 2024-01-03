from fastapi import HTTPException
from pydantic import (
    BaseModel,
    Field,
    field_validator
)

class NoteCreate(BaseModel):
    title: str
    body: str

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

class NoteDB(NoteCreate):
    id: int
