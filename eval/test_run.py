from __future__ import annotations

from types import SimpleNamespace
import unittest

from eval.run import agent_result


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


if __name__ == "__main__":
    unittest.main()
