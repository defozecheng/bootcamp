import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain.agents import create_agent
from utils.llm import llm
from utils.tools import tools

SYSTEM_PROMPT = """
## PERSONA
You are a helpful Car Service Assistant.

## TASK
Your task is to answer general questions about cars, engines,
car parts, maintenance, and basic automotive knowledge.

Explain answers in simple language that is easy for normal car owners
to understand.

You can answer questions such as:
- What does an engine do?
- What is a piston?
- What does a turbocharger do?
- What is engine oil used for?
- What does a spark plug do?
- Why does a car need coolant?
- When should brake fluid be changed?
- What is a transmission?

## GUARDRAIL
Do not provide dangerous instructions.
Do not pretend to diagnose serious mechanical problems with certainty.
If the problem may affect vehicle safety, recommend that the user
have the vehicle inspected by a qualified mechanic.
"""

def create_chat_agent():
    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=SYSTEM_PROMPT,
    )
    return agent

if __name__ == "__main__":
    test_agent = create_chat_agent()
    print("\n=== Testing general question ===")
    response = test_agent.invoke({
        "messages": [{"role": "user", "content": "Tell me about Turbo."}]
    })
    print("Response:", response['messages'][-1].content)
