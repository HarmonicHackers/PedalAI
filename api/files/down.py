from fastapi import APIRouter
from session import Session
from fastapi.responses import StreamingResponse

router = APIRouter()


def stream_file(filepath: str):
    with open(filepath, "rb") as f:
        yield from f


@router.get("/{session_id}/download")
async def download(session_id: str):
    session = Session.load(session_id)
    track_filepath = session.tracks[0].path
    return StreamingResponse(
        stream_file(track_filepath), media_type="audio/mpeg"
    )