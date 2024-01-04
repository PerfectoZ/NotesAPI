from fastapi import APIRouter, Depends
from models.Note import NoteCreate, NoteDB, NoteUpdate
from services.NoteService import NoteService
from services.UserService import UserService
from pymongo import MongoClient

router = APIRouter()
noteService = NoteService(MongoClient("mongodb://localhost:27017/"))
userService = UserService(MongoClient("mongodb://localhost:27017/"))

@router.post("/notes", response_model=NoteDB, status_code=201)
async def create_note(body: NoteCreate, user = Depends(userService.get_current_user)):
    return noteService.create_note_service(body, user)

@router.get("/notes/{id}", response_model=NoteCreate, status_code=200)
async def get_note(id: int, user = Depends(userService.get_current_user)):
    return noteService.get_note_service(id, user)

@router.get("/notes", response_model=None, status_code=200)
async def get_all_notes(user = Depends(userService.get_current_user)):
    return noteService.get_all_notes_service(user["username"])

@router.put("/notes/{id}", response_model=None, status_code=202)
async def update_note(id: int, body: NoteUpdate, user = Depends(userService.get_current_user)):
    return noteService.update_note_service(id, body, user)

@router.delete("/notes/{id}", response_model=None, status_code=200)
async def delete_node(id: int, user = Depends(userService.get_current_user)):
    return noteService.delete_note_service(id, user)