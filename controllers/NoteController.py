import os

from fastapi import APIRouter, Depends
from models.Note import NoteCreate, NoteDB, NoteUpdate, NoteShare
from services.NoteService import NoteService
from services.UserService import UserService
from pymongo import MongoClient

router = APIRouter()
noteService = NoteService(MongoClient(os.environ['DB_URL']))
userService = UserService(MongoClient(os.environ['DB_URL']))

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
async def delete_note(id: int, user = Depends(userService.get_current_user)):
    return noteService.delete_note_service(id, user)

@router.post("/notes/{id}/share", status_code=200)
async def share_note(id: int, body: NoteShare, user = Depends(userService.get_current_user)):
    userService.get_user_by_username(body.model_dump()["toUser"])
    return noteService.share_note_service(id, body, user)

@router.get("/search", status_code=200)
async def search_keywords(query: str = "Python"):
    return noteService.search_keywords_service(query)