"""Small, deterministic dataframe comparison for eval results."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import asdict, dataclass
from typing import Any

import pandas as pd
from pandas.testing import assert_frame_equal


@dataclass(frozen=True)
class ComparisonOptions:
    absolute_tolerance: float = 1e-3
    relative_tolerance: float = 1e-3
    ignore_row_order: bool = True
    top_k: int = 0

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any] | None) -> ComparisonOptions:
        value = value or {}
        return cls(
            absolute_tolerance=float(value.get("absolute_tolerance", cls.absolute_tolerance)),
            relative_tolerance=float(value.get("relative_tolerance", cls.relative_tolerance)),
            ignore_row_order=bool(value.get("ignore_row_order", cls.ignore_row_order)),
            top_k=int(value.get("top_k", cls.top_k)),
        )


@dataclass(frozen=True)
class ResultComparison:
    matched: bool
    reason: str
    expected_rows: int
    actual_rows: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _table_to_frame(table: Mapping[str, Any]) -> pd.DataFrame:
    """Convert Wren's ``{columns, rows}`` result to a normalised dataframe."""
    columns = [str(column).strip().casefold() for column in table.get("columns", [])]
    rows = table.get("rows", [])
    if rows and isinstance(rows[0], Mapping):
        rows = [{str(key).strip().casefold(): value for key, value in row.items()} for row in rows]
    frame = pd.DataFrame(rows, columns=columns)
    frame.columns = [str(column).strip().casefold() for column in frame.columns]
    for column in frame.select_dtypes(include="object"):
        frame[column] = frame[column].map(
            lambda value: " ".join(value.split()).casefold() if isinstance(value, str) else value
        )
    return frame


def _sort_rows(frame: pd.DataFrame) -> pd.DataFrame:
    if frame.empty:
        return frame.reset_index(drop=True)
    # Do not hash the whole row: a tolerated float difference changes the hash
    # and can pair rows with different keys (for example, different counties).
    keys = frame.map(lambda value: "" if pd.isna(value) else str(value))
    order = keys.sort_values(list(keys.columns), kind="stable").index
    return frame.loc[order].reset_index(drop=True)


def _answer_columns(frame: pd.DataFrame, columns: Sequence[str] | None) -> pd.DataFrame:
    """Keep only the columns explicitly required by a dataset contract."""
    if not columns:
        return frame
    required = [str(column).strip().casefold() for column in columns]
    missing = [column for column in required if column not in frame.columns]
    if missing:
        raise ValueError(f"missing required answer columns: {', '.join(missing)}")
    return frame.loc[:, required]


def compare_results(
    expected: Mapping[str, Any],
    actual: Mapping[str, Any],
    options: ComparisonOptions | None = None,
    columns: Sequence[str] | None = None,
) -> ResultComparison:
    """Compare Wren results using pandas' tested dataframe assertion."""
    options = options or ComparisonOptions()
    if expected.get("truncated") or actual.get("truncated"):
        return ResultComparison(False, "result was truncated", len(expected.get("rows", [])), len(actual.get("rows", [])))
    try:
        expected_frame = _answer_columns(_table_to_frame(expected), columns)
        actual_frame = _answer_columns(_table_to_frame(actual), columns)
    except ValueError as error:
        return ResultComparison(False, str(error), len(expected.get("rows", [])), len(actual.get("rows", [])))
    if options.top_k > 0:
        expected_frame = expected_frame.head(options.top_k)
        actual_frame = actual_frame.head(options.top_k)
    if options.ignore_row_order:
        expected_frame = _sort_rows(expected_frame)
        actual_frame = _sort_rows(actual_frame)
    try:
        assert_frame_equal(
            expected_frame,
            actual_frame,
            check_dtype=False,
            check_exact=False,
            atol=options.absolute_tolerance,
            rtol=options.relative_tolerance,
        )
    except AssertionError as error:
        return ResultComparison(False, str(error), len(expected_frame), len(actual_frame))
    return ResultComparison(True, "dataframes match", len(expected_frame), len(actual_frame))
