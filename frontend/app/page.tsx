"use client";

import { CopilotChat, CopilotKit } from "@copilotkit/react-core/v2";

const SUGGESTIONS = [
  "What is the median household income in California?",
  "Compare poverty rates across Indiana counties.",
  "Which counties had the highest unemployment rate?",
];

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
            <p className="eyebrow">AG-UI · AGNO · WREN · SNOWFLAKE</p>
            <h2>Ask questions your data can answer.</h2>
            <p>
              The agent checks the Wren semantic model, then queries the connected
              Census dataset. It will say when a measure cannot be derived safely.
            </p>
            <div className="suggestions" aria-label="Example questions">
              {SUGGESTIONS.map((suggestion) => (
                <span key={suggestion} className="suggestion">{suggestion}</span>
              ))}
            </div>
          </div>

          <div className="chat-frame">
            <CopilotChat agentId="default" className="copilot-chat" />
          </div>
        </section>

        <aside className="side-panel" aria-label="Data access details">
          <div className="side-heading">
            <p className="eyebrow">CONNECTION</p>
            <h2>Query with confidence</h2>
          </div>
          <ol className="flow-list">
            <li><span>01</span><div><strong>Question</strong><p>Ask in plain language.</p></div></li>
            <li><span>02</span><div><strong>Semantic model</strong><p>Wren resolves reviewed model names and business rules.</p></div></li>
            <li><span>03</span><div><strong>Verified result</strong><p>Agno streams an answer backed by the Snowflake query.</p></div></li>
          </ol>
          <div className="note">
            <span className="note-icon" aria-hidden="true">✓</span>
            <p>Credentials and model keys remain on the backend.</p>
          </div>
        </aside>
      </main>
    </CopilotKit>
  );
}
