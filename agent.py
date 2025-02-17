import asyncio
import os
from pathlib import Path
import threading
from dotenv import load_dotenv
from gitingest import ingest
from galadriel import AgentRuntime, ToolCallingAgent
from galadriel.clients import GradioClient
from galadriel.core_agent import LiteLLMModel
from galadriel.domain.prompts import format_prompt
import logging
from prompt import PROMPT

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()  # This will output to console
    ]
)
logger = logging.getLogger(__name__)
load_dotenv(dotenv_path=Path(".") / ".env", override=True)
model = LiteLLMModel(model_id="gpt-4o", api_key=os.getenv("OPENAI_API_KEY"))

prompt = format_prompt.execute(PROMPT, {"code_knowledge": "", "documentation_knowledge": ""})
agent = ToolCallingAgent(
    model=model,
    tools=[],
    prompt_template=prompt,
    flush_memory=True
)

# Set up Gradio client and runtime
gradio_client = GradioClient()
runtime = AgentRuntime(
    agent=agent,
    inputs=[gradio_client],
    outputs=[gradio_client],
)

def _update_prompt(agent):
    """
    This function updates the prompt for the agent.
    """
    try:
        logger.info("Updating prompt...")
        # Get code and documentation
        summary_code, tree_code, content_code = ingest(source="https://github.com/galadriel-ai/galadriel",
                                        exclude_patterns=[".github/", "*.gitignore", "*.sh", "*.toml", "*.yml",
                                                        "/tests", "/scripts", "/galadriel/docker"])
        summary_docs, tree_docs, content_docs = ingest(source="https://github.com/galadriel-ai/docs",
                                        include_patterns="galadriel-network/*")
        logger.info(f"Code summary: {summary_code}")
        logger.info(f"Documentation summary: {summary_docs}")
        # Format new prompt
        prompt = None
        if len(tree_code + content_code) > 1000 and len(tree_docs + content_docs) > 1000:
            prompt = format_prompt.execute(PROMPT, {
                "code_knowledge": tree_code + content_code,
                "documentation_knowledge": tree_docs + content_docs
            })
        else:
            logger.error("Not enough code or documentation to update prompt")

        # Update agent with new prompt template
        if prompt and agent.prompt_template != prompt:
            agent.prompt_template = prompt
    except Exception as e:
        logger.error(f"Error updating prompt: {str(e)}", exc_info=True) 

def _update_prompt_periodically(agent):
    """
    This function tries to update the prompt periodically (every 1h) by ingesting the latest code and documentation.
    It then formats a new prompt and updates the agent with the new prompt.
    """
    _update_prompt(agent)
    threading.Timer(3600, _update_prompt_periodically, args=[agent]).start()

# Run the agent and start periodic prompt update
def main():
    # Start the initial prompt update
    _update_prompt_periodically(agent)
    
    # Run the agent
    asyncio.run(runtime.run())

asyncio.run(main())
