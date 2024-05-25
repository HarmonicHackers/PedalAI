from fastapi import APIRouter
from session import Session

router = APIRouter()


@router.post("/{session_id}/rollback")
async def rollback(session_id: str):
    session = Session.load(session_id)
    session.rollback()
    return {"plugins": len(session.plugins)}
