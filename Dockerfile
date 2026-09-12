FROM node:22-bookworm-slim

# The Python OpenAI client validates api.openai.com over HTTPS. The slim Node
# image does not include a trusted CA bundle by default.
RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    AGENT_PORT=7777 \
    NEXT_TELEMETRY_DISABLED=1

# One container runs both the public Next.js UI and the local Python API.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
RUN uv python install 3.13

# Cache Python and Node dependencies independently of application source.
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

COPY frontend/package.json frontend/package-lock.json ./frontend/
RUN npm ci --prefix frontend

COPY . ./
RUN uv sync --frozen --no-dev
# Agno starts Wren through uvx because their MCP SDK major versions differ.
# Pre-create that exact isolated environment while building the image: without
# this, a fresh --rm container downloads and installs Wren on its first boot,
# which can exceed MCPTools' initialization timeout.
RUN uvx --from "wrenai[main,mcp,snowflake,memory]==0.14.0" --with "mcp<2" wren --help
# The MCP server uses semantic schema retrieval. Build its derived local
# LanceDB index into the image so a fresh container never falls back to a
# full-schema response on the first question.
RUN uv run wren memory index
RUN npm run build --prefix frontend
RUN chmod +x docker/entrypoint.sh

EXPOSE 3000

# Railway routes public traffic to Next.js on $PORT. The API stays private on
# 127.0.0.1:$AGENT_PORT inside this same container.
CMD ["./docker/entrypoint.sh"]
