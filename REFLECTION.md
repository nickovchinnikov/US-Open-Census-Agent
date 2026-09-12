# Reflection

## Development process and architecture

I started by exploring the Snowflake Marketplace dataset. The main challenge was not SQL itself, but data semantics.

My first choice was to keep the whole solution Snowflake-native, but the required agent functionality was not available in my account setup. I kept Snowflake as the source of truth and moved the conversational layer outside it.

I evaluated several open-source options and chose Wren as the semantic SQL layer. It gave me schema-aware access, a reviewable semantic model, and reusable query examples without requiring me to build a Census-specific planner from scratch.

The final architecture is:

1. Snowflake — source of truth.
2. Wren — semantic layer and SQL execution.
3. Agno — agent orchestration, MCP integration, history, and guardrails.
4. Next.js/CopilotKit — browser UI, with credentials kept server-side.

I chose a semantic layer instead of a fully deterministic SQL planner mainly because of the 24-hour limit. A deterministic planner would provide stronger guarantees, but would take considerably more time to implement and validate. I compensated by adding explicit rules around Census grain, aggregation, unsupported requests, and provenance.

A meaningful part of the work was integration and deployment: resolving MCP dependency conflicts, reducing cold-start overhead, and packaging the frontend and backend into a single container. I intentionally kept the UI simple and focused on a working end-to-end flow.

There was also a non-engineering blocker: an OpenAI API payment was still not credited after 10 hours, apparently due to a payment-system issue. Without API access the project could not run, so I had to find an alternative token.

## Scope trade-offs

I deliberately limited the implementation to the 2019 Census data. Multi-year support would require validating variable availability and semantics across years, handling schema differences, and defining which measures are meaningfully comparable over time. Given the 24-hour constraint, I prioritised correctness, provenance, and robust validation within one year over broader temporal coverage with weaker guarantees. Requests for unsupported years fail explicitly rather than falling back to a potentially misleading comparison.

## Testing

I evaluate final results rather than generated SQL strings.

Each test contains a human-reviewed golden query. The harness executes it against Snowflake, extracts the agent's final `run_sql` result, and compares normalised dataframes using ordering and tolerance rules. This allows different valid SQL implementations while checking the actual analytical result.

The evaluation set covers counts, percentages, rankings, joins, county-level aggregation, and invalid aggregation cases. I also added unit tests for the comparison logic.

Manual adversarial testing covered direct and indirect prompt injection, system-prompt and secret exfiltration, arbitrary SQL execution, SQL statement smuggling, authority spoofing, multi-turn policy poisoning, and attempts to override Census aggregation semantics. In the tested scenarios, no out-of-scope SQL was executed and semantic constraints were preserved. The exact prompts, observed outcomes, known issues, and limits of this testing are documented in [TEST.md](TEST.md); these tests are not intended to constitute a complete security assessment.

The latest saved evaluation passed **35 of 37 cases (95%)**, with **13.02 seconds average latency**.

Failures were used as a feedback loop: inspect the SQL and result, identify whether the problem was in the semantic model or agent instructions, fix it, and rerun the affected cases.

The current test set is still limited. It covers only part of the Census schema, and negative tests showed that the model can still call tools for unsupported requests. This is the clearest sign that prompt-only validation is not enough.

## Edge cases and failure modes

The main risk is not a SQL error, but a statistically plausible-looking wrong answer.

Typical examples are averaging CBG median income to estimate a county median, summing percentages, or selecting a variable from the wrong Census universe.

The agent is instructed to reject unsupported requests, clarify missing dimensions, and avoid inventing results when data or tools fail. Examples include unsupported years, forecasts, salary data, safety rankings, and geographies not represented by the dataset.

I added basic Agno guardrails, but did not attempt a complete security hardening. A production version should also use a read-only Snowflake account, SQL validation, execution limits, rate limiting, authentication where needed, and structured audit logs.

## What I would improve

* Add structured logging, tracing, observability, and SLOs.
* Move year, geography, metric, and scope validation out of prompts and into deterministic checks.
* Add a query-plan validator for read-only SQL, approved tables and columns, Census grain, and aggregation rules.
* Manually review and expand the golden dataset with paraphrases, multi-turn cases, ambiguous geography, NULLs, zero denominators, ties, margin-of-error requests, and regression cases.
* Enforce the 60-second end-to-end deadline and track latency and tool-failure metrics.
* Add integration and browser tests for AG-UI, conversation state, guardrail failures, and Snowflake/Wren outages.
* Replace container-local SQLite with durable session storage if the service needs persistence or horizontal scaling.

## Use of AI-assisted development

I used AI-assisted coding tools to speed up implementation and help build the evaluation dataset. I remained responsible for the architecture, Census modelling and aggregation rules, evaluation design, debugging, and final verification.

## Candidate experience feedback

I also want to document one concern about the exercise itself.

The assignment required a publicly deployed application and encouraged the use of AI development tools, but no development environment, infrastructure credits, API budget, or other resources were provided.

In order to complete the assignment within the 24-hour window and meet the requested deployment and quality bar, I incurred approximately $20 in infrastructure/API costs and upgraded my AI development tooling for 99 PLN.

The larger cost, however, was time: I worked on the exercise almost continuously for more than 18 hours, from approximately 10:00 AM until nearly 5:00 AM the following morning.

I think the combination of a production-quality bar, public deployment, unfamiliar dataset exploration, testing, guardrails, infrastructure setup, and a strict 24-hour deadline makes this a very demanding take-home exercise. Completing it to the requested standard required both substantial unpaid time and personal out-of-pocket spending.

*I would recommend either reducing the scope, extending the time window, or providing development/infrastructure credits for future candidates.*
