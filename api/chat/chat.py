from typing import Any, List, Tuple
from fastapi import File, Request, UploadFile, APIRouter


router = APIRouter()


def dummy_chain(prompt: str) -> Tuple[List[Any], str]:
    return ([], "")


@router.post("/chat/completions")
async def chat(r: Request):
    data = await r.json()
    prompt = data["content"]
    # call to chain.invoke(prompt)
    filters, response = dummy_chain(prompt)
    return {"filters": filters, "response": response}
