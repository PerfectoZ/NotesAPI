from fastapi import FastAPI
from controllers.NoteController import router as NoteRouter
from controllers.UserController import router as UserRouter
import uvicorn
from dotenv import load_dotenv

load_dotenv("app.env")

app = FastAPI()
app.include_router(NoteRouter, prefix="/api/v1")
app.include_router(UserRouter, prefix="/api/v1")

uvicorn.run(app, host="0.0.0.0", port=8080, log_level="debug")