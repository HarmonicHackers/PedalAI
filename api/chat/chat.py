from typing import Any, List, Tuple
from agents import get_pedal_effects_from_text
from session import Session
from session import Track
from fastapi import File, Request, UploadFile, APIRouter


from pedalboard import Pedalboard
from pedalboard.io import AudioFile

router = APIRouter()


counter = 0


def dummy_chain(
    messages: List[dict], session_id: str
) -> Tuple[List[Any], str]:
    print(messages)
    text = messages[-1]["content"]
    print(text)
    list_of_effects = get_pedal_effects_from_text(text)
    print(list_of_effects)
    pedal = Pedalboard(list_of_effects)

    session = Session.load(session_id)
    session.plugins = list_of_effects
    track_filepath = session.original.path
    print(track_filepath)

    samplerate = 44100

    with AudioFile(track_filepath).resampled_to(samplerate) as f:
        audio = f.read(f.frames)

    effected = pedal(audio, samplerate)

    filepath = "pedalAi/sessions/" + session_id + "/modified.wav"

    with AudioFile(filepath, "w", samplerate=samplerate, num_channels=2) as f:
        f.write(effected)

    new_track = Track(
        "modified", samplerate / len(f.frames), "unknown", effected, "test.wav"
    )

    session.last_modified = new_track
    session.save()

    return {"role": "assistant", "content": "DONE"}


@router.post("/{session_id}/chat/completions")
async def chat(session_id: str, r: Request):
    data = await r.json()
    messages = data["messages"]
    # call to chain.invoke(messages)
    message = dummy_chain(messages, session_id)
    return {"message": message}
