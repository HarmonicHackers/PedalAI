from fastapi import APIRouter
from chat.chat import apply_plugins
from session import Session

router = APIRouter()


@router.post("/{session_id}/rollback")
async def rollback(session_id: str):
    session = Session.load(session_id)
    session.rollback()
    if len(session.plugins) == 0:
        apply_plugins(0, 100, [], session, session_id)
    else:
        for i, plugin in enumerate(session.plugins):
            apply_plugins(
                plugin["start"],
                plugin["end"],
                plugin["plugins"],
                session,
                session_id,
                is_consecutive=i != 0,
            )
    session.save()
    return {"plugins": len(session.plugins)}
