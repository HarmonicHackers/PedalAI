import os
from fastapi import APIRouter
from session import Session

# from fastapi.responses import StreamingResponse

router = APIRouter()


# def stream_file(filepath: str):
#     with open(filepath, "rb") as f:
#         yield from f


from fastapi.responses import FileResponse


@router.get("/{session_id}/download")
async def download(session_id: str):
    session = Session.load(session_id)
    track_filepath = session.original.path
    if os.path.exists(os.path.join(session.save_path, "modified.wav")):
        track_filepath = session.last_modified.path
    print(track_filepath)
    return FileResponse(track_filepath, media_type="audio/wav")
