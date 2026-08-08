#!/usr/bin/env python3
"""Convert the source Markdown seed table into js/seeds.js.

Usage:
    python tools/build_seed_data.py
"""
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "minecraft_java_unique_biome_terrain_seeds_251.md"
OUTPUT = ROOT / "js" / "seeds.js"

ROW_PATTERN = re.compile(
    r"^\|\s*Java,\s*(26\.2|26\.1|1\.21)\s*\|\s*(.*?)\s*\|\s*`(-?\d+)`\s*\|?\s*$"
)
EXPECTED_COUNTS = {"26.2": 85, "26.1": 65, "1.21": 101}


def parse_rows(markdown: str) -> list[dict[str, str | int]]:
    rows: list[dict[str, str | int]] = []
    for line_number, line in enumerate(markdown.splitlines(), start=1):
        match = ROW_PATTERN.match(line)
        if not match:
            continue
        version, description, seed = match.groups()
        rows.append(
            {
                "id": len(rows) + 1,
                "version": version,
                "description": description.strip(),
                "seed": seed,
                "sourceLine": line_number,
            }
        )
    return rows


def validate(rows: list[dict[str, str | int]]) -> None:
    counts = Counter(str(row["version"]) for row in rows)
    seeds = [str(row["seed"]) for row in rows]
    if counts != Counter(EXPECTED_COUNTS):
        raise ValueError(f"Unexpected version counts: {dict(counts)}")
    if len(seeds) != len(set(seeds)):
        raise ValueError("Duplicate seed values found")
    if len(rows) != 251:
        raise ValueError(f"Expected 251 rows, found {len(rows)}")


def main() -> None:
    rows = parse_rows(SOURCE.read_text(encoding="utf-8"))
    validate(rows)
    payload = json.dumps(rows, ensure_ascii=False, indent=2)
    OUTPUT.write_text(
        "// Generated from data/minecraft_java_unique_biome_terrain_seeds_251.md\n"
        "// Seed values are strings to preserve signed 64-bit integers exactly.\n"
        f"window.MINECRAFT_SEEDS = Object.freeze({payload});\n",
        encoding="utf-8",
    )
    print(f"Generated {OUTPUT.relative_to(ROOT)} with {len(rows)} seeds")


if __name__ == "__main__":
    main()
