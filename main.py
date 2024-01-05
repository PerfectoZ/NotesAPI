from fastapi import FastAPI
import uvicorn
import dotenv
dotenv.load_dotenv()

from controllers.NoteController import router as NoteRouter
from controllers.UserController import router as UserRouter

app = FastAPI()
app.include_router(NoteRouter, prefix="/api/v1")
app.include_router(UserRouter, prefix="/api/v1")