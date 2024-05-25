from langchain_core.tools import tool
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain import hub
from langchain_mistralai import ChatMistralAI

import os

api_key = os.environ.get("MISTRAL_API_KEY")
if not api_key:
    raise ValueError("MISTRAL_API_KEY environment variable not set.")


def call_music_agent(text: str):
    llm = ChatMistralAI(
        model="mistral-large-latest",
        api_key=api_key,
    )

    effects = []

    @tool
    def reverb_effect():
        "Add a reverb effect to the audio."
        print("Adding reverb effect to the audio.")
        effects.append("reverb")
        pass

    @tool
    def gain_effect():
        "Add a reverb effect to the audio."
        print("Adding reverb effect to the audio.")
        effects.append("gain")
        pass

    tools = [
        reverb_effect,
        gain_effect,
    ]

    prompt = hub.pull("hwchase17/openai-tools-agent")
    prompt.pretty_print()

    agent = create_tool_calling_agent(llm, tools, prompt)

    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    result = agent_executor.invoke({"input": text})

    return (result, effects)


ahaha = call_music_agent("Make the song louder")
print(ahaha)
