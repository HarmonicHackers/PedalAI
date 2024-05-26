from typing import Any, List, Tuple
from agents import get_pedal_effects_from_text, get_plugins_from_tool_calls
from session import Session
from session import Track
from fastapi import File, Request, UploadFile, APIRouter


from pedalboard import Pedalboard
from pedalboard.io import AudioFile

router = APIRouter()


counter = 0


def get_audio_part(
    samplerate: float, samples: Any, start: float, end: float
) -> Any:
    start_frame = samplerate * start
    end_frame = samplerate * end
    return samples[:, start_frame:end_frame], start_frame, end_frame


def replace_audio_part(
    samples: Any, modified: Any, start_frame: float, end_frame: float
):
    samples[:, start_frame:end_frame] = modified
    return samples


from mistralai.models.chat_completion import ToolCall


def apply_plugins(
    start: float,
    end: float,
    plugins: List[ToolCall],
    session: Session,
    session_id: str,
    is_consecutive=False,
):
    plugins_from_tool_calls = get_plugins_from_tool_calls(plugins)
    print(plugins_from_tool_calls)

    pedal = Pedalboard(plugins_from_tool_calls)

    track_filepath = (
        session.original.path
        if not is_consecutive
        else session.last_modified.path
    )
    print(track_filepath)

    samplerate = 44100

    with AudioFile(track_filepath).resampled_to(samplerate) as f:
        audio = f.read(f.frames)
        start_timestamp = round(((start / 100) * f.frames) / samplerate)
        end_timestamp = round(((end / 100) * f.frames) / samplerate)
        print(start_timestamp, end_timestamp)
        audio_part, start_frame, end_frame = get_audio_part(
            samplerate, audio, start_timestamp, end_timestamp
        )

    effected = pedal(audio_part, samplerate)
    audio = replace_audio_part(audio, effected, start_frame, end_frame)

    filepath = "pedalAi/sessions/" + session_id + "/modified.wav"

    with AudioFile(filepath, "w", samplerate=samplerate, num_channels=2) as f:
        f.write(audio)
        length = f.frames / f.samplerate

    with open(filepath, "rb") as f:
        samples = f.read()

    new_track = Track("modified", length, "unknown", samples, "test.wav")

    session.last_modified = new_track
    session.save()


def dummy_chain(
    messages: List[dict], session_id: str, start: float, end: float
) -> Tuple[List[Any], str]:
    print(messages)
    text = messages[-1]["content"]
    print(text)
    session = Session.load(session_id)
    chat_message, function_calls, tool_recommendations = (
        get_pedal_effects_from_text(text)
    )

    session.plugins.extend(
        [{"start": start, "end": end, "plugins": function_calls}]
    )

    print("session.plugins", session.plugins)
    for i, plugin in enumerate(session.plugins):
        print(plugin)
        apply_plugins(
            plugin["start"],
            plugin["end"],
            plugin["plugins"],
            session,
            session_id,
            is_consecutive=i != 0,
        )

    return {"role": "assistant", "content": chat_message}, tool_recommendations


@router.post("/{session_id}/chat/completions")
async def chat(session_id: str, r: Request):
    data = await r.json()
    messages = data["messages"]

    percentage_begin = data["percentage_begin"]
    percentage_end = data["percentage_end"]

    # call to chain.invoke(messages)
    message, tool_recommendations = dummy_chain(
        messages, session_id, percentage_begin, percentage_end
    )
    return {"message": message, "tool_recommendations": tool_recommendations}
