from typing import Any, List, Tuple
from fastapi import File, Request, UploadFile, APIRouter


router = APIRouter()


def dummy_chain(messages: List[dict]) -> Tuple[List[Any], str]:
    print(messages)
    return {"role": "assistant", "content": "Hello I am pedalAI assistant"}


@router.post("/chat/completions")
async def chat(r: Request):
    data = await r.json()
    messages = data["messages"]
    # call to chain.invoke(messages)
    message = dummy_chain(messages)
    return {"message": message}
