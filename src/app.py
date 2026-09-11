import os

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.exceptions import InputCheckError
from agno.guardrails import PIIDetectionGuardrail, PromptInjectionGuardrail
from agno.guardrails.base import BaseGuardrail
from agno.models.openai import OpenAIResponses
from agno.os import AgentOS
from agno.os.interfaces.agui import AGUI
from agno.run.agent import RunInput
from agno.tools.mcp import MCPTools
from dotenv import load_dotenv

from .prompts import CENSUS_AGENT_INSTRUCTIONS

load_dotenv()

WREN_ENV = {
    name: value
    for name in (
        "SNOWFLAKE_ACCOUNT",
        "SNOWFLAKE_USER",
        "SNOWFLAKE_PASSWORD",
        "SNOWFLAKE_DATABASE",
        "SNOWFLAKE_SCHEMA",
        "SNOWFLAKE_WAREHOUSE",
    )
    if (value := os.environ.get(name)) is not None
}


class InputLengthGuardrail(BaseGuardrail):
    def __init__(self, max_chars: int = 1000):
        self.max_chars = max_chars

    def check(self, run_input: RunInput) -> None:
        content = run_input.input_content_string()

        if len(content) > self.max_chars:
            raise InputCheckError(
                f"Input is too long. Maximum length is {self.max_chars} characters."
            )

    async def async_check(
        self,
        run_input: RunInput,
    ) -> None:
        self.check(run_input)


# Agno requires MCP 2.x, while Wren 0.14's MCP server uses the MCP 1.x API.
# Run Wren in an isolated uvx environment so the two requirements do not clash.
wren = MCPTools(
    command="uvx --from 'wrenai[main,mcp,snowflake]==0.14.0' --with 'mcp<2' wren serve mcp",
    # The MCP SDK starts subprocesses with a restricted environment. Pass the
    # Snowflake settings explicitly so Wren can resolve its named profile.
    env=WREN_ENV,
    timeout_seconds=60,
    # This project defines MDL models but no Wren cubes. Keep the cube tools
    # out of the agent's tool registry until real cube definitions are added.
    exclude_tools=["query_cube", "list_cubes", "describe_cube"],
)

db = SqliteDb(
    db_file="census-agent.db",
    session_table="census_agent_sessions",
)

agent = Agent(
    id="census-agent",
    name="Census Agent",
    model=OpenAIResponses(id="gpt-5.4-mini"),
    tools=[wren],
    db=db,
    add_history_to_context=True,
    # Keep conversational continuity without re-sending potentially large Wren
    # schema/query outputs from earlier runs to the model.
    num_history_runs=2,
    max_tool_calls_from_history=0,
    store_tool_messages=False,
    pre_hooks=[
        PromptInjectionGuardrail(),
        PIIDetectionGuardrail(
            mask_pii=True,
        ),
        InputLengthGuardrail(max_chars=1000),
    ],
    instructions=CENSUS_AGENT_INSTRUCTIONS,
    markdown=True,
)

agent_os = AgentOS(
    agents=[agent],
    interfaces=[
        AGUI(agent=agent),
    ],
)

app = agent_os.get_app()


if __name__ == "__main__":
    # Next.js owns Railway's public PORT. The API is reached locally by the
    # bundled Next.js server; standalone deployments can still use PORT.
    agent_os.serve(
        app=app,
        host="0.0.0.0",
        port=int(os.environ.get("AGENT_PORT", os.environ.get("PORT", "7777"))),
    )
