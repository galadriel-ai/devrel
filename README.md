# DevRel Agent

## Description

This is a Developer Relations agent that acts as a Senior DevRel for Galadriel. It uses:

- `gpt-4o` model from OpenAI
- `ToolCallingAgent` which processes messages and responds based on provided code and documentation knowledge
- `GradioClient` which implements
  - Public interface for interacting with the agent
  - Handles both input and output communication
- `AgentRuntime` which connects the client to agent and runs the agent execution

The agent acts as a knowledgeable DevRel professional, equipped with understanding of Galadriel's codebase and documentation to assist developers and build community engagement.

## Running the agent

1. Setup local env and install `galadriel`.

```shell
python3 -m venv venv
source venv/bin/activate
pip install galadriel
```

2. Rename `template.env` to `.env` and add your OpenAI API Key.

3. Ensure you have the required knowledge files:
   - `digest_code.txt` - containing code-related knowledge
   - `digest_docs.txt` - containing documentation knowledge

4. Run the agent:

```shell
python agent.py
```

The agent will start with a Gradio interface accessible via a public URL, allowing you to interact with the DevRel agent directly.