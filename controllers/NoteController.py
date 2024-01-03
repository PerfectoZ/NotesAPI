from fastapi import APIRouter
from models.Note import NoteCreate, NoteDB, NoteUpdate
from services.NoteService import (
    create_note_service,
    get_note_service,
    get_all_notes_service,
    update_note_service
)

router = APIRouter()

@router.post("/notes", response_model=NoteDB, status_code=201)
async def create_note(body: NoteCreate):
    return create_note_service(body)

@router.get("/notes/{id}", response_model=NoteCreate, status_code=200)
async def get_note(id: int):
    return get_note_service(id)

@router.get("/notes", status_code=200)
async def get_all_notes():
    return get_all_notes_service()

@router.put("/notes/{id}", status_code=202)
async def update_note(id: int, body: NoteUpdate):
    return update_note_service(id, body)