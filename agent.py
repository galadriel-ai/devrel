import asyncio
import os
from pathlib import Path

from dotenv import load_dotenv

from galadriel import AgentRuntime, ToolCallingAgent
from galadriel.clients import GradioClient
from galadriel.core_agent import LiteLLMModel
from galadriel.domain.prompts import format_prompt
from prompt import PROMPT

load_dotenv(dotenv_path=Path(".") / ".env", override=True)
model = LiteLLMModel(model_id="gpt-4o", api_key=os.getenv("OPENAI_API_KEY"))

# Read code and documentation digests
with open("output_code.txt", "r") as f:
    code_knowledge = f.read()

with open("output_docs.txt", "r") as f:
    documentation_knowledge = f.read()

prompt = format_prompt.execute(PROMPT, {
    "code_knowledge": code_knowledge,
    "documentation_knowledge": documentation_knowledge
})

# Add agent with GPT-4o model and DuckDuckGo search tool
agent = ToolCallingAgent(
    model=model,
    tools=[],
    prompt_template=prompt,
    flush_memory=True
)
#agent.prompt_templates["system_prompt"] = PROMPT
gradio_client = GradioClient()
# Set up the runtime
runtime = AgentRuntime(
    agent=agent,
    inputs=[gradio_client],
    outputs=[gradio_client],
)

# Run the agent
asyncio.run(runtime.run())
