from langchain_core.tools import tool
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain import hub
from langchain_mistralai import ChatMistralAI

from pedalboard import Pedalboard
from pedalboard import Reverb, Gain, Bitcrush

import os

api_key = os.environ.get("MISTRAL_API_KEY")
if not api_key:
    raise ValueError("MISTRAL_API_KEY environment variable not set.")


def call_music_agent(text: str):
    llm = ChatMistralAI(
        model="mistral-large-latest",
        api_key=api_key,
    )

    suggested_effects = []

    @tool
    def reverb(
        # room_size: float = 0.5,
        # damping: float = 0.5,
        # wet_level: float = 0.33,
        # dry_level: float = 0.4,
        # width: float = 1.0,
        # freeze_mode: float = 0.0,
    ):
        "Add a reverb effect to the audio."
        reverb_effect = Reverb(
            # room_size=room_size,
            # damping=damping,
            # wet_level=wet_level,
            # dry_level=dry_level,
            # width=width,
            # freeze_mode=freeze_mode,
        )
        suggested_effects.append(reverb_effect)

    @tool
    def gain(gain_db: float = 0.1):
        "Add a gain effect to the audio."
        gain_effect = Gain(gain_db)
        suggested_effects.append(gain_effect)

    @tool
    def bitcrush(bit_depth: int = 8):
        "Add a bitcrush effect to the audio."
        bitcrush_effect = Bitcrush(bit_depth=bit_depth)
        suggested_effects.append(bitcrush_effect)

    tools = [
        reverb,
        gain,
        bitcrush,
    ]

    prompting_agent = hub.pull("hwchase17/openai-tools-agent")
    prompting_agent.pretty_print()
    agent = create_tool_calling_agent(llm, tools, prompting_agent)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    agent_invoke_result = agent_executor.invoke({"input": text})
    return (agent_invoke_result, suggested_effects)


def AI_alter_sound(prompt_text: str):
    agent_invoke_result, suggested_effects = call_music_agent(prompt_text)
    suggested_pedalboard = Pedalboard(suggested_effects)
    print(suggested_effects)
    return suggested_pedalboard


sound_effects = AI_alter_sound(
    "Add effects to this song to make it sound like it's underwater."
)

# sound_effects = AI_alter_sound(
#     "Add effects to this song to make it sound like it's played in a cave."
# )
