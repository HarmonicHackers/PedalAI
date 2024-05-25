from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
import os

model = "mistral-large-latest"
api_key = os.environ.get("MISTRAL_API_KEY")

tools = [
    {
        "type": "function",
        "function": {
            "name": "reverb_effect",
            "description": "Add a reverb effect to the audio.",
            "parameters": {
                "type": "object",
                "properties": {
                    "room_size": {
                        "type": "number",
                        "description": "The room size, between 0 and 1.",
                    },
                    "damping": {
                        "type": "number",
                        "description": "The damping.",
                    },
                    "wet_level": {
                        "type": "number",
                        "description": "The wet level.",
                    },
                    "dry_level": {
                        "type": "number",
                        "description": "The dry level.",
                    },
                    "freeze_mode": {
                        "type": "number",
                        "description": "The freeze mode.",
                    },
                },
                "required": ["room_size"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "bitcrush_effect",
            "description": "Add a bitcrush effect to the audio.",
            "parameters": {
                "type": "object",
                "properties": {
                    "bit_depth": {
                        "type": "number",
                        "description": "The bit depth.",
                    }
                },
                "required": ["bit_depth"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "gain_effect",
            "description": "Add a gain effect to the audio.",
            "parameters": {
                "type": "object",
                "properties": {
                    "gain_db": {
                        "type": "number",
                        "description": "The gain in decibels.",
                    }
                },
                "required": ["gain_db"],
            },
        },
    },
]


def get_pedal_effects_from_text(text):
    print(text)

    messages = [
        ChatMessage(
            role="system",
            content="You are a music assistant with access to a music track. You must use function calling!",
        ),
        ChatMessage(
            role="user",
            content=text,
        ),
    ]

    from pedalboard import Reverb, Gain, Bitcrush

    array = []

    def wrapper(func, **kwargs):
        array.append(func(**kwargs))

    import functools

    names_to_functions = {
        "reverb_effect": functools.partial(wrapper, Reverb),
        "bitcrush_effect": functools.partial(wrapper, Bitcrush),
        "gain_effect": functools.partial(wrapper, Gain),
    }

    client = MistralClient(api_key=api_key)
    response = client.chat(
        model=model, messages=messages, tools=tools, tool_choice="any", temperature=0.1
    )
    import json

    print(response.choices[0].message.content)

    for tool_call in response.choices[0].message.tool_calls:
        function_name = tool_call.function.name
        function_params = json.loads(tool_call.function.arguments)
        print(function_name, function_params)
        function_result = names_to_functions[function_name](**function_params)

    return array


effects = get_pedal_effects_from_text(
    "Add effects to this song to make it sound like it's played in a cathedral."
)
print(effects)
effects = get_pedal_effects_from_text(
    "Add effects to this song to make it sound like it's underwater."
)
print(effects)
