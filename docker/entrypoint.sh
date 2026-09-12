#!/bin/sh
set -eu

# Containers are ephemeral, so create the Wren profile from Railway/Docker
# environment variables on every start. Do not test Snowflake here: validation
# can block the public web server for minutes when an account's network policy
# rejects the deploy host. Wren reports any real connection error on the query.
/opt/wren-mcp/bin/wren profile add us-open-census \
  --from-file wren-snowflake-connection.yml --no-validate

# The API is private to this container; Next.js is the only public process.
uv run python -m src.app &
# Next's standalone launcher honors HOSTNAME. Docker sets it to the container
# ID by default, while Railway requires the public server to bind all IPv4
# interfaces rather than that internal name.
exec env HOSTNAME=0.0.0.0 node frontend/server.js
