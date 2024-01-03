from fastapi import APIRouter
from models.Note import NoteCreate, NoteDB, NoteUpdate
from services.NoteService import NoteService
from pymongo import MongoClient

router = APIRouter()
noteService = NoteService(MongoClient("mongodb://localhost:27017/"))

@router.post("/notes", response_model=NoteDB, status_code=201)
async def create_note(body: NoteCreate):
    return noteService.create_note_service(body)

@router.get("/notes/{id}", response_model=NoteCreate, status_code=200)
async def get_note(id: int):
    return noteService.get_note_service(id)

@router.get("/notes", response_model=None, status_code=200)
async def get_all_notes():
    return noteService.get_all_notes_service()

@router.put("/notes/{id}", response_model=None, status_code=202)
async def update_note(id: int, body: NoteUpdate):
    return noteService.update_note_service(id, body)

@router.delete("/notes/{id}", response_model=None, status_code=200)
async def delete_node(id: int):
    return noteService.delete_note_service(id)