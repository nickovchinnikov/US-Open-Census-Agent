"use client";

import {
  CopilotChat,
  CopilotKit,
  useAgent,
  useCopilotKit,
  useDefaultRenderTool,
} from "@copilotkit/react-core/v2";

const SUGGESTIONS = [
  "What is the median household income in California?",
  "Compare poverty rates across Indiana counties.",
];

function InternalToolActivity() {
  // Keep the data-access process understandable without exposing MCP names,
  // SQL, tool arguments, or raw tool results.
  useDefaultRenderTool({
    render: ({ name, status }) => {
      const activity = {
        list_models: "Checking available Census data",
        describe_model: "Reviewing the data definition",
        run_sql: "Calculating the result",
      }[name] ?? "Analyzing the data request";

      const isComplete = status === "complete";

      return (
        <div
          className={`tool-activity${isComplete ? " is-complete" : ""}`}
          aria-live="polite"
        >
          <span className="tool-activity-icon" aria-hidden="true" />
          <span>{activity}</span>
          <span className="tool-activity-status">
            {isComplete ? "Done" : "In progress"}
          </span>
        </div>
      );
    },
  });

  return null;
}

function QuickQuestions() {
  const { agent } = useAgent({ agentId: "default" });
  const { copilotkit } = useCopilotKit();

  const askQuestion = async (message: string) => {
    if (agent.isRunning) return;

    agent.addMessage({
      id: crypto.randomUUID(),
      role: "user",
      content: message,
    });
    await copilotkit.runAgent({ agent });
  };

  return (
    <div className="suggestions" aria-label="Example questions">
      {SUGGESTIONS.map((suggestion) => (
        <button
          key={suggestion}
          type="button"
          className="suggestion"
          disabled={agent.isRunning}
          onClick={() => void askQuestion(suggestion)}
        >
          {suggestion}
        </button>
      ))}
    </div>
  );
}

export default function Home() {
  return (
    <CopilotKit
      runtimeUrl="/api/copilotkit"
      useSingleEndpoint
    >
      <main className="app-shell">
        <section className="chat-panel" aria-label="Census analyst chat">
          <header className="topbar">
            <div className="brand">
              <div className="brand-mark" aria-hidden="true">US</div>
              <div>
                <p className="eyebrow">US OPEN CENSUS</p>
                <h1>Census Data Analyst</h1>
              </div>
            </div>
            <div className="status" title="Queries use the Wren semantic layer">
              <span className="status-dot" /> Grounded data access
            </div>
          </header>

          <div className="intro">
            <h2>Ask questions your data can answer.</h2>
            <p>
              The agent checks the Wren semantic model, then queries the connected
              Census dataset. It will say when a measure cannot be derived safely.
            </p>
            <QuickQuestions />
          </div>

          <div className="chat-frame">
            <InternalToolActivity />
            <CopilotChat agentId="default" className="copilot-chat" />
          </div>
        </section>
      </main>
    </CopilotKit>
  );
}
