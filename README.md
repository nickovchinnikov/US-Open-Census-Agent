# US Open Census Agent

This project uses Wren AI to model and query the Snowflake database
`US_OPEN_CENSUS_DATA_NEIGHBORHOOD_INSIGHTS_FREE_DATASET`.

## Live demo

The public application is available at
[us-open-census-agent-production.up.railway.app](https://us-open-census-agent-production.up.railway.app/).
No application-level authentication is required.

## Connection setup

Copy the values for the Snowflake account, user, password, and schema into `.env`.
This project's connection profile uses password authentication and Snowflake's
default warehouse.
The `.env` file is ignored by Git; `.env _template` is the safe shareable template.

Once the values are in place, create and bind the Wren profile using the included
secret-free `wren-snowflake-connection.yml`:

```bash
uv sync
uv run wren profile add us-open-census --from-file wren-snowflake-connection.yml
uv run wren context init --empty
uv run wren context set-profile us-open-census
```

Then generate Wren MDL models from the selected Snowflake tables before querying.


`models/` contains the generated and validated Wren MDL semantic layer. It is committed intentionally to make the agent's data model reviewable and reproducible.

## Local Docker run

Prerequisite: Docker Desktop or Docker Engine must be running. Create a root
`.env` file with the OpenAI and Snowflake settings:

```env
OPENAI_API_KEY=sk-...
SNOWFLAKE_ACCOUNT=your-account-identifier
SNOWFLAKE_USER=your-user
SNOWFLAKE_PASSWORD=your-password
SNOWFLAKE_DATABASE=US_OPEN_CENSUS_DATA_NEIGHBORHOOD_INSIGHTS_FREE_DATASET
SNOWFLAKE_SCHEMA=PUBLIC
SNOWFLAKE_WAREHOUSE=your-warehouse
```

When passing this file via Docker's `--env-file`, do not wrap values in quotes:
Docker treats those quotes as part of the value. In particular,
`SNOWFLAKE_ACCOUNT` must contain only the Snowflake account identifier.

Build the image from the repository root:

```bash
docker build -t us-open-census-agent .
```

Run it with the settings from `.env`:

```bash
docker run --rm \
  --name us-open-census-agent \
  --env-file .env \
  -e PORT=3000 \
  -p 3000:3000 \
  us-open-census-agent
```

Open [http://localhost:3000](http://localhost:3000). The Python API runs only
inside the container on port 7777; it is reached by the web application and is
not published on the host. Stop the application with `Ctrl+C`.

## Web chat UI

The ready-to-run CopilotKit + AG-UI frontend lives in [`frontend/`](frontend/).
Start the Agno backend with `uv run python -m src.app`, then follow the short
setup in [`frontend/README.md`](frontend/README.md) to open the UI at
`http://localhost:3000`.

## Production deployment (Railway)

Deploy this repository as **one Railway service**, connected to GitHub with
autodeploy enabled for `master`. Railway detects the root
[`Dockerfile`](Dockerfile), which builds both applications into one image:

- Next.js serves the public UI on Railway's automatically supplied `PORT`.
- The Python Agno API runs privately in the same container on port `7777`.
- The UI reaches it through `http://127.0.0.1:7777/agui`; no public backend
  domain and no Railway `AGENT_URL` variable are needed.
- The container creates the required Wren `us-open-census` profile on startup
  from the Snowflake variables below.

Add these service variables in Railway: `OPENAI_API_KEY`,
`SNOWFLAKE_ACCOUNT`, `SNOWFLAKE_USER`, `SNOWFLAKE_PASSWORD`,
`SNOWFLAKE_DATABASE`, `SNOWFLAKE_SCHEMA`, and `SNOWFLAKE_WAREHOUSE`.
Optionally set `COPILOTKIT_TELEMETRY_DISABLED=true`.

The image preloads Wren's public semantic-memory model
`sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` during its
build, then runs it offline. `HF_TOKEN` is therefore **not** needed for the
default configuration and must never be added to the Dockerfile. Set it only
as a Railway/Docker secret if you intentionally switch to a private or
gated Hugging Face model; it is forwarded to the Wren MCP subprocess.

## Result-based agent evaluation

The eval suite grades database results rather than generated SQL strings. It
compares the final agent `run_sql` result with golden SQL using pandas dataframe
comparison, including configured float tolerance and optional row-order ignore.

### Latest result

The latest full result-based evaluation, using `gpt-5.4-mini`, completed all
executions and passed **35 of 37 cases** (**95%** result accuracy), with an
average latency of **13.02 seconds**. The two remaining failures are recorded
in the committed [evaluation report](eval/results/20260912T010025Z-gpt-5.4-mini/report.md)
and are retained as regression cases rather than omitted from the result.

Configure the model and evaluation parameters in
[`eval/config.toml`](eval/config.toml). Then run the full suite:

```bash
uv run python -m eval.run
```

Each run creates both a machine-readable `report.json` and a readable
`report.md` in `eval/results/<timestamp>-<model>/`. The process returns a
non-zero exit code if any case fails, making it suitable for CI.

Useful overrides:

```bash
# Benchmark a different OpenAI Responses model.
uv run python -m eval.run --model gpt-5.6-mini --run-name gpt-5-6-mini

# Iterate on a single query or a tagged slice.
uv run python -m eval.run --name which-indiana-counties-had-the-highest-unemployment-rate-in
uv run python -m eval.run --tag source:verified-census-query

# Fast deterministic sample: the first 10 selected dataset records.
uv run python -m eval.run --limit 10

# Reuse a previous golden-result cache when the underlying dataset is unchanged.
uv run python -m eval.run --no-refresh-golden-results
```
