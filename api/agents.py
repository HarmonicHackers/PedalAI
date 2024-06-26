from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
import os

# import weave
import functools, json
from groq import Groq
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

# Model & API key environment variable
model = "mistral-large-latest"
api_key = os.environ.get("MISTRAL_API_KEY")
# weave.init("Pedal-AI")
groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

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
                        "description": "The room size, between 0 and 1. 1 usually is too large, one should only use it for very large rooms.",
                    },
                    "damping": {
                        "type": "number",
                        "description": "The damping. A high value will make the reverb sound more muffled, between 0 and 1.",
                    },
                    "wet_level": {
                        "type": "number",
                        "description": "The wet level. A value of 1 means full wet signal.",
                    },
                    "dry_level": {
                        "type": "number",
                        "description": "The dry level. A value of 1 means full dry signal.",
                    },
                    "freeze_mode": {
                        "type": "number",
                        "description": "The freeze mode. A value of 1 means the reverb will freeze.",
                    },
                },
                "required": ["room_size", "damping"],
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
                        "default": 8,
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
                        "default": "3.0",
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
    {
        "type": "function",
        "function": {
            "name": "do_nothing",
            "description": "Does nothing",
            "parameters": {},
        },
    },
    # Add more effects here...
]

from mistralai.models.chat_completion import ToolCall


def get_plugins_from_tool_calls(tool_calls: list[ToolCall]):
    import functools, json

    # Initialize the list that will store the suggested effects
    suggested_effects_list = []

    # Define a wrapper function that appends all the effects to the list
    def wrapper(func, **kwargs):
        suggested_effects_list.append(func(**kwargs))

    def do_nothing():
        pass

    # Create a dictionary that maps the function names to the actual functions
    functions_effects_map = {
        "do_nothing": do_nothing,
        "reverb_effect": functools.partial(wrapper, Reverb),
        "bitcrush_effect": functools.partial(wrapper, Bitcrush),
        "gain_effect": functools.partial(wrapper, Gain),
        "chorus_effect": functools.partial(wrapper, Chorus),
        "clipping_effect": functools.partial(wrapper, Clipping),
        "compressor_effect": functools.partial(wrapper, Compressor),
        "delay_effect": functools.partial(wrapper, Delay),
        "distortion_effect": functools.partial(wrapper, Distortion),
    }

    # Iterate over the tool calls and apply the effects
    for tool_call in tool_calls:
        func_name = tool_call.function.name
        func_params = json.loads(tool_call.function.arguments)

        # Call the function with the parameters using the map & wrapper
        func_result = functions_effects_map[func_name](**func_params)
        # print(func_result)

    return suggested_effects_list


def get_pedal_effects_from_text(text):

    # Define the default chat messages
    default_messages = [
        ChatMessage(  # System message (AI assistant introduction)
            role="system",
            content="You are a helpful music assistant with access to a music track. You must use function calling to apply effects to the latter track! Make sure to not provide too strong effects and not too much at the same time (max 3,4)",
        ),
        ChatMessage(  # User input
            role="user",
            content=text,
        ),
    ]
    print("ROOT MESSAGES", default_messages)

    # Create the Mistral client and send the default chat messages
    client = MistralClient(api_key=api_key)
    response = client.chat(
        model=model,
        messages=default_messages,
        tools=audio_effects_jsons,
        tool_choice="any",  # Make model sends at least one tool call
        temperature=0.1,  # Creativity level
    )

    function_calls = response.choices[0].message.tool_calls

    def get_tools_explanation(effects):
        tools_explanation = (
            "I have applied the following effects to the audio track: "
        )
        for effect in effects:
            tools_explanation += f"{effect.function.name} "
        return tools_explanation

    def get_desc_text(effects):
        describing_text = get_tools_explanation(effects)

        tools_we_wave_name = [
            audio_effects_jsons[i]["function"]["description"]
            for i in range(len(audio_effects_jsons))
        ]

        joining_tools = "\n".join(tools_we_wave_name)

        messages = [
            ChatMessage(
                role="system",
                # content="Give some expressive opinion in 2 sentences on what the user asked, and what effect the user could ask for. Example: 'Oh nice good idea, try applying this!'",
                content="Justify what you did according to the user preference and make some recommandations. Example: 'Oh nice good idea, try applying this!. Write only two sentence'"
                + "Here is every tool we have:\n"
                + joining_tools,
            ),
            ChatMessage(role="user", content=text),
            ChatMessage(role="user", content=describing_text),
        ]
        print(messages)

        reponse = groq_client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=messages,
            temperature=0,
        )
        describing_text = reponse.choices[0].message.content

        return describing_text

    describing_text = get_desc_text(function_calls)

    def get_recommandation(desciption):
        messages = [
            ChatMessage(
                role="system",
                # content="Give some expressive opinion in 2 sentences on what the user asked, and what effect the user could ask for. Example: 'Oh nice good idea, try applying this!'",
                content="Use every recommendations and additional effects mentioned, you cannot recommend the effect you are currently applying",
            ),
            ChatMessage(role="user", content=desciption),
        ]
        print(messages)

        mistral_response = client.chat(
            model=model,
            messages=messages,
            tools=audio_effects_jsons,
            tool_choice="any",  # Make model sends at least one tool call
            temperature=0.1,  # Creativity level
        )

        tool_calls = mistral_response.choices[0].message.tool_calls
        return tool_calls

    tool_recommendations = get_recommandation(describing_text)
    print("tool_recommendations", tool_recommendations)

    # Return the suggested effects list (list of effect objects to apply to the audio track later on)
    return describing_text, function_calls, tool_recommendations
