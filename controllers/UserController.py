import os

from fastapi import APIRouter, Depends
from models.User import UserCreate, UserLogin
from services.UserService import UserService
from pymongo import MongoClient

router = APIRouter()
userService = UserService(MongoClient(os.environ['DB_URL']))

@router.post("/users", status_code=201)
async def create_note(body: UserCreate):
    return userService.create_user_service(body)

@router.post("/users/login", status_code=201)
async def login_user(body: UserLogin):
    return userService.login_user_service(body)

@router.get("/users/details")
async def user_details(user: dict = Depends(userService.get_current_user)):
    return user