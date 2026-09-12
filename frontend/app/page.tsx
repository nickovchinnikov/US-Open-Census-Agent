"use client";

import {
  CopilotChat,
  CopilotKit,
  useAgent,
  useCopilotKit,
  useDefaultRenderTool,
} from "@copilotkit/react-core/v2";

const SUGGESTIONS = [
  "How many males aged 22 to 24 lived in Wabash County, Indiana in 2019?",
  "What is the average (mean) household income in Indiana?",
  "Which Indiana counties had the highest unemployment rate in 2019?",
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

        <section className="workspace" aria-label="Census analyst chat">
          <aside className="question-rail">
            <div>
              <p className="rail-kicker">Start a query</p>
              <h2>What would you like to learn?</h2>
              <p className="rail-copy">
                Ask about people, households, places, or changes across the 2019 Census dataset.
              </p>
            </div>
            <QuickQuestions />
            <p className="rail-note">
              Answers are checked against the Census semantic model before data is returned.
            </p>
          </aside>

          <div className="chat-stage">
            <div className="chat-heading">
              <div>
                <p className="rail-kicker">Data conversation</p>
                <h2>Census analyst</h2>
              </div>
              <span className="chat-heading-note">2019 Census data</span>
            </div>
            <div className="chat-frame">
              <InternalToolActivity />
              <CopilotChat agentId="default" className="copilot-chat" />
            </div>
          </div>
        </section>
      </main>
    </CopilotKit>
  );
}
