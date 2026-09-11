#!/bin/sh
set -eu

# Containers are ephemeral, so create the Wren profile from Railway/Docker
# environment variables on every start before the MCP server is initialized.
uv run wren profile add us-open-census --from-file wren-snowflake-connection.yml

# The API is private to this container; Next.js is the only public process.
uv run python -m src.app &
exec sh -c 'cd frontend && exec node node_modules/next/dist/bin/next start -H 0.0.0.0 -p "$PORT"'
