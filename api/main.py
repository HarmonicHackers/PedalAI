import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from files import up, down, undo
from chat import chat
from session import Session


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(up.router)
app.include_router(down.router)
app.include_router(chat.router)
app.include_router(undo.router)


@app.get("/")
async def home():
    # Create a new session & return the session id
    s = Session()
    s.original = None
    s.last_modified = None
    s.save()
    return {"session_id": s.id}


if __name__ == "__main__":
    # Load the Mistral API key from env
    load_dotenv()

    # Start the server on port 4000
    print("Starting server on port 4000 🚀")
    uvicorn.run(app, host="0.0.0.0", port=4000)
