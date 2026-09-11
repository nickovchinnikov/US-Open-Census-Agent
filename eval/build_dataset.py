#!/usr/bin/env python3
"""Build a JSONL evaluation dataset from Markdown files with YAML front matter.

Each input file must contain ``nl`` (the question) and ``sql`` (the reference
query).  For example:

    ---
    nl: How many occupied housing units are there in Suffolk County?
    sql: SELECT ...
    source: user
    tags:
      - source:verified-census-query
    ---

The default output has one JSON object per line:

    {
      "id": "how-many-occupied-housing-units-are-there-in-suffolk-county",
      "question": "...",
      "sql":: "...",
      "metadata": {"source": "user", "tags": [...], "source_file": "..."}
    }

Run from the repository root:

    python eval/build_dataset.py

Use ``--format json`` when a consumer expects one JSON array instead of JSONL.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path
from typing import Any

try:
    import yaml
except ModuleNotFoundError as exc:  # pragma: no cover - depends on environment
    raise SystemExit(
        "PyYAML is required to read the Markdown front matter. "
        "Install the project dependencies first (for example: uv sync)."
    ) from exc


REQUIRED_FIELDS = ("nl", "sql")


class DatasetBuildError(ValueError):
    """Raised when an input example cannot be converted safely."""


def parse_front_matter(path: Path) -> dict[str, Any]:
    """Read and validate the YAML front matter in one Markdown example."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        raise DatasetBuildError(f"{path}: expected YAML front matter starting with '---'.")

    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        raise DatasetBuildError(f"{path}: the opening delimiter must be on its own line.")

    closing_index = next(
        (index for index, line in enumerate(lines[1:], start=1) if line.strip() == "---"),
        None,
    )
    if closing_index is None:
        raise DatasetBuildError(f"{path}: missing closing YAML front-matter delimiter.")

    try:
        front_matter = yaml.safe_load("".join(lines[1:closing_index]))
    except yaml.YAMLError as exc:
        raise DatasetBuildError(f"{path}: invalid YAML front matter: {exc}") from exc

    if not isinstance(front_matter, dict):
        raise DatasetBuildError(f"{path}: front matter must be a mapping/object.")

    for field in REQUIRED_FIELDS:
        value = front_matter.get(field)
        if not isinstance(value, str) or not value.strip():
            raise DatasetBuildError(f"{path}: required field '{field}' must be a non-empty string.")

    return front_matter


def build_record(path: Path, raw_dir: Path) -> dict[str, Any]:
    """Map one source file to the schema used by the evaluation runner."""
    example = parse_front_matter(path)
    metadata = {key: value for key, value in example.items() if key not in REQUIRED_FIELDS}
    metadata["source_file"] = path.relative_to(raw_dir.parent).as_posix()

    return {
        "id": path.stem,
        "question": example["nl"].strip(),
        "sql": example["sql"].strip(),
        "metadata": metadata,
    }


def collect_records(raw_dir: Path) -> list[dict[str, Any]]:
    """Build ordered records and reject duplicate ids before writing anything."""
    paths = sorted(raw_dir.glob("*.md"))
    if not paths:
        raise DatasetBuildError(f"{raw_dir}: no Markdown files found.")

    records = [build_record(path, raw_dir) for path in paths]
    ids = [record["id"] for record in records]
    duplicates = sorted({item for item in ids if ids.count(item) > 1})
    if duplicates:
        raise DatasetBuildError(f"Duplicate dataset ids: {', '.join(duplicates)}")
    return records


def serialise(records: list[dict[str, Any]], output_format: str) -> str:
    if output_format == "jsonl":
        return "".join(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n" for record in records)
    if output_format == "json":
        return json.dumps(records, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    raise ValueError(f"Unsupported format: {output_format}")


def write_atomically(output: Path, content: str) -> None:
    """Replace the output only after all parsing and serialization has succeeded."""
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        dir=output.parent,
        prefix=f".{output.name}.",
        suffix=".tmp",
        delete=False,
    ) as temporary:
        temporary.write(content)
        temporary_path = Path(temporary.name)

    try:
        os.replace(temporary_path, output)
    except BaseException:
        temporary_path.unlink(missing_ok=True)
        raise


def parse_args() -> argparse.Namespace:
    repository_root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=repository_root / "eval" / "raw",
        help="Directory containing Markdown examples (default: eval/raw).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=repository_root / "eval" / "dataset.jsonl",
        help="Dataset file to create (default: eval/dataset.jsonl).",
    )
    parser.add_argument(
        "--format",
        choices=("jsonl", "json"),
        default="jsonl",
        help="Output encoding: one JSON object per line or one JSON array (default: jsonl).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    raw_dir = args.input_dir.resolve()
    output = args.output.resolve()

    try:
        records = collect_records(raw_dir)
        write_atomically(output, serialise(records, args.format))
    except (DatasetBuildError, OSError) as exc:
        print(f"Dataset build failed: {exc}", file=sys.stderr)
        return 1

    print(f"Wrote {len(records)} examples to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
