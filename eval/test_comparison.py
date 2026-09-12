from __future__ import annotations

import unittest

from eval.comparison import ComparisonOptions, compare_results


class ResultComparisonTests(unittest.TestCase):
    def test_tolerant_numbers_and_normalised_text(self) -> None:
        expected = {"columns": ["County", "rate"], "rows": [{"County": "Marion", "rate": 8.41}]}
        actual = {"columns": ["county", "rate"], "rows": [{"county": " marion ", "rate": 8.4105}]}
        self.assertTrue(compare_results(expected, actual, ComparisonOptions(absolute_tolerance=0.001)).matched)

    def test_row_order_is_ignored(self) -> None:
        expected = {"columns": ["county"], "rows": [["Lake"], ["Allen"]]}
        actual = {"columns": ["county"], "rows": [["allen"], ["lake"]]}
        self.assertTrue(compare_results(expected, actual).matched)

    def test_extra_column_fails_with_pandas_diff(self) -> None:
        expected = {"columns": ["county"], "rows": [["Lake"]]}
        actual = {"columns": ["county", "state"], "rows": [["Lake", "IN"]]}
        result = compare_results(expected, actual)
        self.assertFalse(result.matched)
        self.assertIn("shape", result.reason)

    def test_top_k_compares_only_first_rows(self) -> None:
        expected = {"columns": ["county"], "rows": [["Lake"], ["Allen"], ["Wrong"]]}
        actual = {"columns": ["county"], "rows": [["allen"], ["lake"], ["Other"]]}
        self.assertTrue(compare_results(expected, actual, ComparisonOptions(top_k=2)).matched)

    def test_contract_columns_exclude_evidence_columns(self) -> None:
        expected = {"columns": ["county", "workers", "rate"], "rows": [["Lake", 10, 8.41]]}
        actual = {"columns": ["county", "rate"], "rows": [["Lake", 8.4105]]}
        result = compare_results(expected, actual, ComparisonOptions(absolute_tolerance=0.001), columns=["county", "rate"])
        self.assertTrue(result.matched)

    def test_missing_contract_column_is_clear_failure(self) -> None:
        expected = {"columns": ["county", "rate"], "rows": [["Lake", 8.41]]}
        actual = {"columns": ["county", "other_rate"], "rows": [["Lake", 8.41]]}
        result = compare_results(expected, actual, columns=["county", "rate"])
        self.assertFalse(result.matched)
        self.assertIn("missing required answer columns: rate", result.reason)

    def test_unordered_rows_with_tolerated_float_difference_keep_their_keys(self) -> None:
        expected = {"columns": ["county", "rate"], "rows": [["San Francisco County", 34.767345], ["Los Angeles County", 5.813891]]}
        actual = {"columns": ["county", "rate"], "rows": [["Los Angeles County", 5.81], ["San Francisco County", 34.77]]}
        self.assertTrue(compare_results(expected, actual, columns=["county", "rate"]).matched)


if __name__ == "__main__":
    unittest.main()
