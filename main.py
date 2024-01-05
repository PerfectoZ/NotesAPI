from fastapi import FastAPI
from controllers.NoteController import router as NoteRouter
from controllers.UserController import router as UserRouter
import uvicorn
import dotenv

dotenv.load_dotenv()

app = FastAPI()
app.include_router(NoteRouter, prefix="/api/v1")
app.include_router(UserRouter, prefix="/api/v1")