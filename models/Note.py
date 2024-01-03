from pydantic import BaseModel

class NoteCreate(BaseModel):
    title: str
    body: str

class NoteDB(NoteCreate):
    id: int
