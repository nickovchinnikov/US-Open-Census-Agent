# syntax=docker/dockerfile:1

# Build Next.js separately so the final image contains its standalone server,
# not the whole development node_modules directory.
FROM node:22-bookworm-slim AS frontend-build
WORKDIR /app/frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

FROM node:22-bookworm-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:0.11.7 /uv /uvx /bin/

ENV PYTHONUNBUFFERED=1 \
    UV_LINK_MODE=copy \
    UV_NO_CACHE=1 \
    HF_HOME=/opt/huggingface \
    AGENT_PORT=7777 \
    NEXT_TELEMETRY_DISABLED=1

# The app only needs Agno and the OpenAI client. Wren lives in the isolated
# environment below because its MCP 1.x requirement conflicts with Agno's
# MCP 2.x requirement.
COPY pyproject.toml uv.lock ./
RUN uv python install 3.13 \
    && uv sync --frozen --no-dev --no-install-project

# Railway has no GPU. The PyPI Linux torch wheel pulls ~7 GB of CUDA runtime
# packages; install the matching CPU wheel explicitly before Wren's resolver.
# The image is deployed on Railway's linux/amd64 builders.
RUN uv venv /opt/wren-mcp --python 3.13 \
    && uv pip install --python /opt/wren-mcp/bin/python \
      'https://download.pytorch.org/whl/cpu/torch-2.14.0%2Bcpu-cp313-cp313-manylinux_2_28_x86_64.whl' \
    && uv pip install --python /opt/wren-mcp/bin/python \
      'wrenai[main,mcp,snowflake,memory]==0.14.0' 'mcp<2'

COPY . ./

# Keep runtime fully offline. These assets are only ~0.5 GB with CPU-only
# PyTorch, while avoiding a multi-minute Hugging Face download on the first
# MCP request (which would exceed Agno's initialization timeout).
RUN HF_HUB_OFFLINE=0 TRANSFORMERS_OFFLINE=0 \
      /opt/wren-mcp/bin/python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')" \
    && HF_HUB_OFFLINE=0 TRANSFORMERS_OFFLINE=0 /opt/wren-mcp/bin/wren memory index \
    && chmod +x docker/entrypoint.sh

ENV HF_HUB_OFFLINE=1 \
    TRANSFORMERS_OFFLINE=1

COPY --from=frontend-build /app/frontend/.next/standalone ./frontend/
COPY --from=frontend-build /app/frontend/.next/static ./frontend/.next/static

EXPOSE 3000
CMD ["./docker/entrypoint.sh"]
