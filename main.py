from fastapi import FastAPI
from controllers.NoteController import router as NoteRouter

app = FastAPI()
app.include_router(NoteRouter, prefix="/api/v1")