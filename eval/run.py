"""Run a small, strict result-based evaluation for the Census agent."""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import subprocess
import sys
import tomllib
from collections.abc import Mapping
from dataclasses import replace
from datetime import UTC, datetime
from pathlib import Path
from statistics import mean
from typing import Any

from agno.eval import Case, arun_cases
from agno.scorer import AnyRunOutput, Score

from eval.comparison import ComparisonOptions, compare_results
from src.app import create_census_agent, wren

ROOT = Path(__file__).resolve().parent.parent


def table(value: Any) -> dict[str, Any]:
    """Use one Wren table shape everywhere: ``{columns, rows, truncated}``."""
    if isinstance(value, Mapping) and "rows" in value:
        return dict(value)
    if isinstance(value, Mapping):
        return {"columns": list(value), "rows": [dict(value)], "truncated": False}
    if isinstance(value, list):
        columns = list(value[0]) if value and isinstance(value[0], Mapping) else []
        return {"columns": columns, "rows": value, "truncated": False}
    raise ValueError("Wren did not return a table")


class AgentResultError(ValueError):
    def __init__(self, message: str, tool: dict[str, Any]) -> None:
        super().__init__(message)
        self.tool = tool


def golden_result(sql: str, row_limit: int) -> dict[str, Any]:
    completed = subprocess.run(
        ["wren", "--sql", sql, "--output", "json", "--quiet", "--limit", str(row_limit)],
        cwd=ROOT,
        env=os.environ.copy(),
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode:
        raise RuntimeError(completed.stderr.strip() or "golden SQL failed")
    output = completed.stdout.strip()
    if not output:
        return {"columns": [], "rows": [], "truncated": False}
    try:
        value = json.loads(output)
    except json.JSONDecodeError:
        value = [json.loads(line) for line in output.splitlines() if line.strip()]
    return table(value)


def agent_result(run: AnyRunOutput) -> tuple[dict[str, Any], str]:
    """Read the final run_sql result: the prompt requires it to be the answer query."""
    last_tool: dict[str, Any] | None = None
    for tool in reversed(getattr(run, "tools", []) or []):
        if not (getattr(tool, "tool_name", "") or "").casefold().endswith("run_sql"):
            continue
        evidence = {
            "name": getattr(tool, "tool_name", "run_sql"),
            "sql": str((getattr(tool, "tool_args", None) or {}).get("sql", "")),
            "tool_call_error": bool(getattr(tool, "tool_call_error", False)),
            "raw_result": getattr(tool, "result", None),
        }
        last_tool = evidence
        if evidence["tool_call_error"]:
            continue
        raw = getattr(tool, "result", None)
        if raw is None:
            continue
        try:
            if isinstance(raw, str):
                raw = json.loads(raw)
            return table(raw), evidence["sql"]
        except (TypeError, ValueError, json.JSONDecodeError) as error:
            raise AgentResultError(f"final run_sql result is not a table: {error}", evidence) from error
    raise AgentResultError("agent did not finish with a successful run_sql result", last_tool or {})


class ResultScorer:
    """Minimal Agno scorer: run golden SQL, compare two dataframes, retain evidence."""

    def __init__(self, options: ComparisonOptions, row_limit: int) -> None:
        self.options = options
        self.row_limit = row_limit
        self.details: dict[str, dict[str, Any]] = {}

    async def ascore(self, run: AnyRunOutput, expected: Any = None) -> Score:
        case_id = expected["id"]
        try:
            actual, sql = agent_result(run)
        except AgentResultError as error:
            detail = {
                "execution_success": 0,
                "result_match": 0,
                "reason": str(error),
                "agent_tool": error.tool,
            }
        except Exception as error:
            detail = {"execution_success": 0, "result_match": 0, "reason": f"agent result error: {type(error).__name__}: {error}"}
        else:
            contract = expected["contract"]
            options = replace(self.options, top_k=int(contract.get("top_k", self.options.top_k)))
            try:
                golden = await asyncio.to_thread(golden_result, expected["sql"], self.row_limit)
                comparison = compare_results(golden, actual, options, columns=contract["expected_columns"])
            except Exception as error:
                detail = {
                    "execution_success": 1,
                    "result_match": 0,
                    "reason": f"golden result error: {type(error).__name__}: {error}",
                    "agent_result": actual,
                    "agent_sql": sql,
                }
            else:
                detail = {
                    "execution_success": 1,
                    "result_match": int(comparison.matched),
                    "reason": comparison.reason,
                    "golden_result": golden,
                    "agent_result": actual,
                    "agent_sql": sql,
                    "comparison": comparison.to_dict(),
                }
        self.details[case_id] = detail
        return Score(
            value=float(detail["result_match"]),
            passed=bool(detail["execution_success"] and detail["result_match"]),
            reason=detail["reason"],
            detail=detail,
        )


def load_dataset(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    valid = isinstance(data, list) and all(
        {"id", "question", "sql", "contract"} <= set(item)
        and isinstance(item["contract"], Mapping)
        and isinstance(item["contract"].get("expected_columns"), list)
        and item["contract"]["expected_columns"]
        for item in data
    )
    if not valid:
        raise ValueError("each dataset case needs id, question, sql, and contract.expected_columns")
    return data


def case_input(item: Mapping[str, Any]) -> str:
    columns = ", ".join(item["contract"]["expected_columns"])
    contract = item["contract"]
    output_rule = f"Finish with one run_sql table containing exactly these columns, in this order: {columns}."
    if contract.get("tie_policy") == "first_by_census_block_group":
        output_rule += " If multiple rows tie, return exactly one: the lexicographically first CENSUS_BLOCK_GROUP."
    if contract.get("top_k"):
        output_rule += f" Return exactly the top {int(contract['top_k'])} rows."
    return f"{item['question']}\n\nFor this evaluation: {output_rule}"


def tags(item: Mapping[str, Any]) -> tuple[str, ...]:
    metadata = item.get("metadata", {})
    return tuple(metadata.get("tags", [])) if isinstance(metadata, Mapping) else ()


def report(suite: Any, dataset: list[dict[str, Any]], scorer: ResultScorer, config: dict[str, Any]) -> dict[str, Any]:
    cases: list[dict[str, Any]] = []
    by_id = {item["id"]: item for item in dataset}
    for result in suite.results:
        detail = scorer.details.get(result.name, {"execution_success": 0, "result_match": 0, "reason": result.error})
        cases.append(
            {
                "id": result.name,
                "question": by_id[result.name]["question"],
                "passed": result.passed,
                "execution_success": detail["execution_success"],
                "result_match": detail["result_match"],
                "latency_seconds": getattr(getattr(result.response, "metrics", None), "duration", None),
                "reason": detail["reason"],
                "comparison": detail.get("comparison"),
                "golden_result": detail.get("golden_result"),
                "agent_result": detail.get("agent_result"),
                "agent_sql": detail.get("agent_sql"),
                "agent_tool": detail.get("agent_tool"),
            }
        )
    latencies = [case["latency_seconds"] for case in cases if case["latency_seconds"] is not None]
    return {
        "model": config["agent"]["model"],
        "created_at": datetime.now(UTC).isoformat(),
        "summary": {
            "total": len(cases),
            "passed": sum(case["passed"] for case in cases),
            "execution_rate": mean(case["execution_success"] for case in cases),
            "result_accuracy": mean(case["result_match"] for case in cases),
            "avg_latency_seconds": mean(latencies) if latencies else None,
        },
        "cases": cases,
    }


def markdown(data: dict[str, Any]) -> str:
    summary = data["summary"]
    lines = [
        "# Census eval",
        "",
        f"Model: `{data['model']}`  ",
        f"Cases: {summary['passed']}/{summary['total']} passed  ",
        f"Execution: {summary['execution_rate']:.0%}  ",
        f"Result accuracy: {summary['result_accuracy']:.0%}  ",
        f"Average latency: {summary['avg_latency_seconds']:.2f}s" if summary["avg_latency_seconds"] is not None else "Average latency: n/a",
        "",
        "## Failures",
        "",
    ]
    failures = [case for case in data["cases"] if not case["passed"]]
    lines.extend(f"- `{case['id']}`: {case['reason']}" for case in failures)
    return "\n".join(lines) + "\n"


def args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=ROOT / "eval" / "config.toml")
    parser.add_argument("--model")
    parser.add_argument("--name")
    parser.add_argument("--tag")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--run-name")
    return parser.parse_args()


async def run(cli: argparse.Namespace) -> tuple[dict[str, Any], Path]:
    config_path = cli.config if cli.config.is_absolute() else ROOT / cli.config
    with config_path.open("rb") as file:
        config = tomllib.load(file)
    if cli.model:
        config["agent"]["model"] = cli.model
    dataset_path = ROOT / config["run"].get("dataset", "eval/dataset.json")
    selected = [item for item in load_dataset(dataset_path) if (not cli.name or item["id"] == cli.name) and (not cli.tag or cli.tag in tags(item))]
    if cli.limit is not None:
        if cli.limit < 1:
            raise ValueError("--limit must be at least 1")
        selected = selected[: cli.limit]
    if not selected:
        raise ValueError("no cases selected")

    agent = create_census_agent(
        model_id=config["agent"]["model"],
        temperature=config["agent"].get("temperature"),
        max_output_tokens=config["agent"].get("max_output_tokens"),
        reasoning_effort=config["agent"].get("reasoning_effort"),
        database=None,
        add_history_to_context=False,
    )
    scorer = ResultScorer(ComparisonOptions.from_mapping(config.get("comparison")), config["run"].get("query_row_limit", 1000))
    cases = [
        Case(name=item["id"], agent=agent, input=case_input(item), expected=item, scorer=scorer, tags=tags(item), timeout_seconds=config["run"].get("case_timeout_seconds", 120))
        for item in selected
    ]
    await wren.connect()
    try:
        suite = await arun_cases(cases)
    finally:
        await wren.close()

    output_root = cli.output_dir or ROOT / config["run"].get("results_dir", "eval/results")
    name = cli.run_name or f"{datetime.now(UTC):%Y%m%dT%H%M%SZ}-{config['agent']['model']}"
    return report(suite, selected, scorer, config), output_root / name


def main() -> int:
    try:
        data, output = asyncio.run(run(args()))
    except (OSError, ValueError, RuntimeError, tomllib.TOMLDecodeError) as error:
        print(f"Eval failed: {error}", file=sys.stderr)
        return 2
    output.mkdir(parents=True, exist_ok=True)
    (output / "report.json").write_text(json.dumps(data, indent=2, ensure_ascii=False, default=str) + "\n", encoding="utf-8")
    (output / "report.md").write_text(markdown(data), encoding="utf-8")
    print(f"{data['summary']['passed']}/{data['summary']['total']} passed — {output}")
    return 0 if data["summary"]["passed"] == data["summary"]["total"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
