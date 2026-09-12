from __future__ import annotations

import asyncio
from types import SimpleNamespace
import unittest

from eval.comparison import ComparisonOptions
from eval.run import ResultScorer, agent_result, case_input


def tool(sql: str, result: object) -> SimpleNamespace:
    return SimpleNamespace(
        tool_name="run_sql",
        tool_args={"sql": sql},
        result=result,
        tool_call_error=False,
    )


class AgentResultTests(unittest.TestCase):
    def test_selects_last_query_matching_output_contract(self) -> None:
        run = SimpleNamespace(
            tools=[
                tool("SELECT answer", [{"answer": 42}]),
                tool("SELECT state_fips", []),
            ]
        )

        result, sql, calls = agent_result(run, ["answer"])

        self.assertEqual(sql, "SELECT answer")
        self.assertEqual(result["rows"], [{"answer": 42}])
        self.assertEqual([call["sql"] for call in calls], ["SELECT answer", "SELECT state_fips"])
        self.assertTrue(calls[0]["matches_output_contract"])
        self.assertFalse(calls[1]["matches_output_contract"])

    def test_unavailable_case_uses_concise_response_without_sql(self) -> None:
        expected = {
            "id": "unavailable-salary",
            "contract": {
                "outcome": "unavailable",
                "expected_response": "Unavailable: salary data is not available in this dataset.",
            },
        }
        run = SimpleNamespace(content="Unavailable: salary data is not available in this dataset.", tools=[])
        scorer = ResultScorer(ComparisonOptions(), row_limit=1000)

        score = asyncio.run(scorer.ascore(run, expected))

        self.assertTrue(score.passed)
        self.assertEqual(scorer.details["unavailable-salary"]["agent_response"], run.content)

    def test_unavailable_case_does_not_receive_a_formatting_hint(self) -> None:
        item = {
            "question": "Which neighborhood in San Francisco is the safest?",
            "contract": {"outcome": "unavailable", "expected_response": "Unavailable: safety data is not available in this dataset."},
        }
        self.assertEqual(case_input(item), item["question"])


if __name__ == "__main__":
    unittest.main()
