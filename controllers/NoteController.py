from fastapi import APIRouter
from models.Note import NoteCreate, NoteDB
from services.NoteService import create_note_service

router = APIRouter()

@router.post("/notes", response_model=NoteDB, status_code=201)
async def create_note(body: NoteCreate):
    return create_note_service(body)
