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


# FIXME: Env problems in MCP...
WREN_ENV = {
    name: value
    for name in (
        "SNOWFLAKE_ACCOUNT",
        "SNOWFLAKE_USER",
        "SNOWFLAKE_PASSWORD",
        "SNOWFLAKE_DATABASE",
        "SNOWFLAKE_SCHEMA",
        "SNOWFLAKE_WAREHOUSE",
        # The Docker image preloads Wren's SentenceTransformer model here.
        # Forward its explicit cache location to the restricted MCP subprocess.
        "HF_HOME",
        "HF_HUB_OFFLINE",
        "TRANSFORMERS_OFFLINE",
        # Optional: useful only when deliberately changing to a private or
        # gated Hugging Face model. The default Wren model is public.
        "HF_TOKEN",
    )
    if (value := os.environ.get(name)) is not None
}


# Agno requires MCP 2.x, while Wren 0.14's MCP server uses the MCP 1.x API.
# Run Wren in an isolated uvx environment so the two requirements do not clash.
wren = MCPTools(
    command="uvx --from 'wrenai[main,mcp,snowflake,memory]==0.14.0' --with 'mcp<2' wren serve mcp",
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

def create_census_agent(
    *,
    model_id: str = "gpt-5.4-mini",
    temperature: float | None = None,
    max_output_tokens: int | None = None,
    reasoning_effort: str | None = None,
    database: SqliteDb | None = db,
    add_history_to_context: bool = True,
) -> Agent:
    """Build the Census agent for the application or an isolated eval run.

    Eval callers can select an OpenAI Responses model without mutating the
    production agent or sharing conversational history between cases.
    """
    model_options = {"id": model_id}
    if temperature is not None:
        model_options["temperature"] = temperature
    if max_output_tokens is not None:
        model_options["max_output_tokens"] = max_output_tokens
    if reasoning_effort is not None:
        model_options["reasoning_effort"] = reasoning_effort

    return Agent(
        id="census-agent",
        name="Census Agent",
        model=OpenAIResponses(**model_options),
        tools=[wren],
        db=database,
        add_history_to_context=add_history_to_context,
        # Keep conversational continuity without re-sending potentially large Wren
        # schema/query outputs from earlier runs to the model.
        num_history_runs=2 if add_history_to_context else None,
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


agent = create_census_agent()

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
