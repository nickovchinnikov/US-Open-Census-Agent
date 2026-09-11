# Census Agent UI

Next.js + CopilotKit UI for the Agno agent already defined in `../src/app.py`.
The browser only talks to the local Next.js route. That route proxies AG-UI to
the Agno endpoint, so OpenAI, Snowflake, and Wren credentials never move to the
frontend.

## Run locally

From the repository root, use two terminals:

```bash
# Terminal 1 — Agno + AG-UI backend
uv run python -m src.app
```

```bash
# Terminal 2 — CopilotKit UI
cd frontend
cp .env.example .env.local
npm install
npm run dev
```

Open `http://localhost:3000`.

`AGENT_URL` defaults to `http://127.0.0.1:7777/agui`, which is the endpoint
mounted by `AGUI(agent=agent)` in this project. Override it in `.env.local` for
a deployed agent, for example:

```env
AGENT_URL=https://your-agent.example.com/agui
```

The CopilotKit runtime agent is intentionally named `default`: its v2 provider
uses that ID for internal listeners. It still proxies to the Census agent above.

## Production

Set `AGENT_URL` in the frontend hosting environment. Do not use a
`NEXT_PUBLIC_` prefix: the URL belongs to the server-side CopilotKit bridge.
