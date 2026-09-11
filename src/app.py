from agno.agent import Agent
from agno.models.openai import OpenAIResponses
from agno.os import AgentOS
from agno.os.interfaces.agui import AGUI
from agno.tools.mcp import MCPTools

# Agno requires MCP 2.x, while Wren 0.14's MCP server uses the MCP 1.x API.
# Run Wren in an isolated uvx environment so the two requirements do not clash.
wren = MCPTools(
    command="uvx --from 'wrenai[main,mcp,snowflake]==0.14.0' --with 'mcp<2' wren serve mcp"
)

agent = Agent(
    name="Census Agent",
    model=OpenAIResponses(id="gpt-5.4"),
    tools=[wren],
    instructions="""
You are a Census Q&A model

Rules:
- Wren is the source of truth for available data.
- Use Wren tools to inspect the semantic model and schema.
- Never invent Census variables, physical tables, columns or geography mappings.
- Prefer verified measures present in the Wren model.
- Use Wren to execute SQL against Snowflake.
- If a requested metric cannot be derived correctly, explain why rather than approximating it incorrectly.
""",
)

agent_os = AgentOS(
    agents=[agent],
    interfaces=[
        AGUI(agent=agent),
    ],
)

app = agent_os.get_app()


if __name__ == "__main__":
    agent_os.serve(app=app, port=7777)
