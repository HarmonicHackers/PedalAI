from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
import os

# Model & API key environment variable
model = "mistral-large-latest"
api_key = os.environ.get("MISTRAL_API_KEY")

# Check if the API key is set & raise an error if not
if not api_key:
    raise ValueError("Please set the MISTRAL_API_KEY environment variable.")

audio_effects_jsons = [
    {  # Reverb
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
    {  # Bitcrush
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
    {  # Gain
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
    {  # Chorus
        "type": "function",
        "function": {
            "name": "chorus_effect",
            "description": "Add a chorus effect to the audio.",
            "parameters": {
                "type": "object",
                "properties": {
                    "rate_hz": {
                        "type": "number",
                        "description": "The speed of the chorus effect’s low-frequency oscillator (LFO), in Hertz. Must be between 0 Hz and 100 Hz.",
                        "default": 1.0,
                    },
                    "depth": {
                        "type": "number",
                        "description": "The depth of the chorus effect. Controls the amount of modulation.",
                        "default": 0.25,
                    },
                    "centre_delay_ms": {
                        "type": "number",
                        "description": "The centre delay time of the modulation, in milliseconds.",
                        "default": 7.0,
                    },
                    "feedback": {
                        "type": "number",
                        "description": "The feedback volume of the chorus effect.",
                        "default": 0.0,
                    },
                    "mix": {
                        "type": "number",
                        "description": "The mix between the dry signal and the wet signal of the effect. A value of 1 means full wet signal.",
                        "default": 0.5,
                    },
                },
                "required": [
                    "rate_hz",
                    "depth",
                ],
            },
        },
    },
    {  # Clipping
        "type": "function",
        "function": {
            "name": "clipping_effect",
            "description": "Add a clipping effect to the audio.",
            "parameters": {
                "type": "object",
                "properties": {
                    "threshold_db": {
                        "type": "number",
                        "description": "The threshold (in decibels) at which the signal will be clipped.",
                        "default": -6.0,
                    }
                },
                "required": ["threshold_db"],
            },
        },
    },
    {  # Compressor
        "type": "function",
        "function": {
            "name": "compressor_effect",
            "description": "Add a compressor effect to the audio.",
            "parameters": {
                "type": "object",
                "properties": {
                    "threshold_db": {
                        "type": "number",
                        "description": "The threshold (in decibels) at which the compressor will start to reduce the signal volume.",
                        "default": 0,
                    },
                    "ratio": {
                        "type": "number",
                        "description": "The ratio of input to output signal above the threshold.",
                        "default": 1,
                    },
                    "attack_ms": {
                        "type": "number",
                        "description": "The attack time (in milliseconds) for the compressor to start reducing the volume after the threshold is exceeded.",
                        "default": 1.0,
                    },
                    "release_ms": {
                        "type": "number",
                        "description": "The release time (in milliseconds) for the compressor to stop reducing the volume after the signal falls below the threshold.",
                        "default": 100,
                    },
                },
                "required": [
                    "threshold_db",
                    "ratio",
                    "attack_ms",
                    "release_ms",
                ],
            },
        },
    },
    {  # Delay
        "type": "function",
        "function": {
            "name": "delay_effect",
            "description": "Add a delay effect to the audio.",
            "parameters": {
                "type": "object",
                "properties": {
                    "delay_seconds": {
                        "type": "number",
                        "description": "The delay time in seconds.",
                        "default": 0.5,
                    },
                    "feedback": {
                        "type": "number",
                        "description": "The feedback percentage of the delay effect.",
                        "default": 0.0,
                    },
                    "mix": {
                        "type": "number",
                        "description": "The mix between the dry signal and the wet signal of the effect.",
                        "default": 0.5,
                    },
                },
                "required": ["delay_seconds", "feedback", "mix"],
            },
        },
    },
    {  # Distortion
        "type": "function",
        "function": {
            "name": "distortion_effect",
            "description": "Add a distortion effect to the audio.",
            "parameters": {
                "type": "object",
                "properties": {
                    "drive_db": {
                        "type": "number",
                        "description": "The amount of drive applied to the signal in decibels.",
                        "default": 25,
                    }
                },
                "required": ["drive_db"],
            },
        },
    },
    # Add more effects here...
]


def get_pedal_effects_from_text(text):
    import functools, json
    from pedalboard import (
        Reverb,
        Gain,
        Bitcrush,
        Chorus,
        Clipping,
        Compressor,
        Delay,
        Distortion,
    )

    # Define the default chat messages
    default_messages = [
        ChatMessage(  # System message (AI assistant introduction)
            role="system",
            content="You are a helpful music assistant with access to a music track. You must use function calling to apply effects to the latter track!",
        ),
        ChatMessage(  # User input
            role="user",
            content=text,
        ),
    ]

    # Initialize the list that will store the suggested effects
    suggested_effects_list = []

    # Define a wrapper function that appends all the effects to the list
    def wrapper(func, **kwargs):
        suggested_effects_list.append(func(**kwargs))

    # Create a dictionary that maps the function names to the actual functions
    functions_effects_map = {
        "reverb_effect": functools.partial(wrapper, Reverb),
        "bitcrush_effect": functools.partial(wrapper, Bitcrush),
        "gain_effect": functools.partial(wrapper, Gain),
        "chorus_effect": functools.partial(wrapper, Chorus),
        "clipping_effect": functools.partial(wrapper, Clipping),
        "compressor_effect": functools.partial(wrapper, Compressor),
        "delay_effect": functools.partial(wrapper, Delay),
        "distortion_effect": functools.partial(wrapper, Distortion),
    }

    # Create the Mistral client and send the default chat messages
    client = MistralClient(api_key=api_key)
    response = client.chat(
        model=model,
        messages=default_messages,
        tools=audio_effects_jsons,
        tool_choice="any",  # Make model sends at least one tool call
        temperature=0.1,  # Creativity level
    )

    # print(response.choices[0].message.content)

    # Iterate over the tool calls and apply the effects
    for tool_call in response.choices[0].message.tool_calls:
        func_name = tool_call.function.name
        func_params = json.loads(tool_call.function.arguments)

        # Call the function with the parameters using the map & wrapper
        functions_effects_map[func_name](**func_params)

    # Return the suggested effects list (list of effect objects to apply to the audio track later on)
    return suggested_effects_list
