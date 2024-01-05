from fastapi import FastAPI
from controllers.NoteController import router as NoteRouter
from controllers.UserController import router as UserRouter
import uvicorn
from dotenv import load_dotenv

app = FastAPI()
app.include_router(NoteRouter, prefix="/api/v1")
app.include_router(UserRouter, prefix="/api/v1")

if __name__ == "__main__":
    # load_dotenv()
    uvicorn.run(app, host="127.0.0.1", port=8081, log_level="debug")