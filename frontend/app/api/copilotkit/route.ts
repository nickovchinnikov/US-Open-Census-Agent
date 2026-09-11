import { HttpAgent } from "@ag-ui/client";
import {
  CopilotRuntime,
  ExperimentalEmptyAdapter,
  copilotRuntimeNextJSAppRouterEndpoint,
} from "@copilotkit/runtime";
import { NextRequest } from "next/server";

export const runtime = "nodejs";

const agentUrl = process.env.AGENT_URL ?? "http://127.0.0.1:7777/agui";

// The bridge keeps the browser on the same origin and sends AG-UI requests to
// Agno server-to-server. Do not expose Snowflake or model credentials here.
const runtimeInstance = new CopilotRuntime({
  agents: {
    // CopilotKit's v2 provider uses "default" for its internal listeners.
    // This is an alias in the Next.js bridge only; Agno still serves the
    // Census agent at AGENT_URL.
    default: new HttpAgent({ url: agentUrl }) as never,
  },
});

const { handleRequest } = copilotRuntimeNextJSAppRouterEndpoint({
  runtime: runtimeInstance,
  serviceAdapter: new ExperimentalEmptyAdapter(),
  endpoint: "/api/copilotkit",
});

export async function GET(request: NextRequest) {
  return handleRequest(request);
}

export async function POST(request: NextRequest) {
  return handleRequest(request);
}
