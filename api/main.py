import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from session.track import Track
from files import up, down
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


@app.get("/")
async def home():
    s = Session()
    s.original = None
    s.last_modified = None
    s.save()
    return {"session_id": s.id}


if __name__ == "__main__":
    load_dotenv()
    uvicorn.run(app, host="0.0.0.0", port=4000)
