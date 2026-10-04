#!/usr/bin/env python3
"""Reproduce the October 2026 catalogue migration from reviewed research.

For routine future edits, edit data/minecraft_java_seeds.json instead.
This migration keeps the historical 251-row Markdown untouched.
"""
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

from build_seed_data import VERSIONS, validate

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
CHECKED_AT = "2026-10-04"
EXCLUSIONS = {
    "178707548189246514": "원문의 정확한 시드·Java 버전·특징을 재확인하지 못함",
    "1180506052330500839": "원문의 정확한 시드·Java 버전·특징을 재확인하지 못함",
    "8144877040668690370": "원문의 정확한 시드·Java 버전·특징을 재확인하지 못함",
    "3110000067282134548": "원문 숫자 확인 불가; 동적 지도 URL만으로는 특징을 검증할 수 없음",
    "68147685812": "버전별 100개 편성을 위해 유사한 평탄 생존 섬 가운데 제외; 원문은 확인됨",
    "16965060050": "버전별 100개 편성을 위해 유사한 평탄 생존 섬 가운데 제외; 원문은 확인됨",
    "7196303038988998513": "숫자는 원문에 있으나 Java 26.1 에디션·핵심 지형 근거가 부족해 신규 출처 항목으로 교체",
    "6230119895383733384": "숫자는 원문에 있으나 Java 26.1 에디션·핵심 지형 근거가 부족해 신규 출처 항목으로 교체",
    "-608830374621340378": "숫자는 원문에 있으나 Java 26.1 에디션·핵심 지형 근거가 부족해 신규 출처 항목으로 교체",
    "8015641954194115677": "숫자는 원문에 있으나 Java 26.1 에디션·핵심 지형 근거가 부족해 신규 출처 항목으로 교체",
    "888880641529027638": "숫자는 원문에 있으나 Java 26.1 에디션·핵심 지형 근거가 부족해 신규 출처 항목으로 교체",
    "62384459426931": "숫자는 원문에 있으나 Java 26.1 에디션·핵심 지형 근거가 부족해 신규 출처 항목으로 교체",
    "-862348623794739": "숫자는 원문에 있으나 Java 26.1 에디션·핵심 지형 근거가 부족해 신규 출처 항목으로 교체",
    "4361528937055201680": "숫자는 원문에 있으나 Java 26.1 에디션·핵심 지형 근거가 부족해 신규 출처 항목으로 교체",
    "-8880302588844065321": "흑요석 농장 시드의 부호가 출처 간 충돌해 확인 가능한 신규 Java 26.1 항목으로 교체",
}
ROW_PATTERN = re.compile(r"^\|\s*Java,\s*(26\.2|26\.1|1\.21)\s*\|\s*(.*?)\s*\|\s*`(-?\d+)`\s*\|?\s*$")


def read_json(name: str):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def coordinates_text(value) -> str | None:
    if value is None or isinstance(value, str):
        return value
    label = {"spawn": "스폰", "Spawn": "스폰", "Survival Island": "생존 섬",
             "Village": "마을", "Woodland Mansion": "삼림 대저택",
             "Shipwreck": "난파선", "Mineshaft": "폐광", "Stronghold": "요새"}.get(value.get("label"), value.get("label", "원문 관심 지점"))
    axes = ", ".join(f"{axis.upper()}: {value[axis]}" for axis in ("x", "y", "z") if value.get(axis) is not None)
    return f"{label} · {axes}"


def main() -> None:
    mappings = {row["seed"]: row for row in read_json("research-legacy-sources.json")}
    old_markdown = (DATA / "minecraft_java_unique_biome_terrain_seeds_251.md").read_text(encoding="utf-8")
    rows = []
    excluded = []
    for line in old_markdown.splitlines():
        match = ROW_PATTERN.match(line)
        if not match:
            continue
        version, description, seed = match.groups()
        if seed in EXCLUSIONS:
            excluded.append({"seed": seed, "oldVersion": version, "description": description, "reason": EXCLUSIONS[seed]})
            continue
        mapping = mappings[seed]
        status = mapping["evidenceStatus"]
        if status == "source-listed" and mapping["sourceName"].lower().startswith("ezseed"):
            status = "map-checked"
        corrected_version = mapping.get("recommendedVersion", version)
        source_version = mapping.get("sourceVersion")
        if status == "legacy-collection":
            source_version = f"{source_version or version} (에디션 미상)"
            note = "원문에 에디션이 명시되지 않아 Java 재현 확인이 필요합니다."
        else:
            note = "원문에 명시된 Java 호환 버전 기준. 좌표는 원문의 관심 지점입니다."
        if corrected_version != version:
            note = "기존 26.1 표기를 원문의 1.21.11 호환 범위에 맞춰 정정했습니다."
        if "Pale Garden is not present" in mapping.get("evidenceNotes", ""):
            note = "창백한 정원이 포함된 1.21.x 자료입니다. 정확한 세부 버전은 원문에 명시되지 않았습니다."
        if "conflicting publisher evidence" in mapping.get("evidenceNotes", ""):
            note = "출처 간 시드 부호가 다릅니다. 이 값은 연결된 원문의 음수 표기를 유지하며 게임 재현 확인이 필요합니다."
        if status == "map-checked":
            note = "원문은 지도 계산 기반 자료입니다. 실제 게임에서 지형·스폰을 다시 확인하세요."
        row = {
            "version": corrected_version,
            "description": mapping.get("recommendedDescription", description),
            "seed": mapping.get("correctedSeed", seed),
            "sourceName": mapping["sourceName"],
            "sourceUrl": mapping["sourceUrl"],
            "sourceVersion": source_version,
            "verification": status,
            "coordinates": coordinates_text(mapping.get("coordinates")),
            "checkedAt": CHECKED_AT,
            "evidenceNotes": mapping.get("evidenceNotesKo", mapping.get("koreanNotes", note)),
        }
        rows.append(row)
    newer = read_json("research-26.3.json")["rows"] + read_json("research-older.json")
    keep = ("version", "description", "seed", "sourceName", "sourceUrl", "sourceVersion",
            "verification", "coordinates", "checkedAt", "evidenceNotes", "publisherVerifiedAt", "sourceTitle", "originalCredit")
    for candidate in newer:
        row = {key: candidate[key] for key in keep if key in candidate}
        if row["sourceName"] == "ezseed":
            row["verification"] = "map-checked"
        rows.append(row)
    document = {"schemaVersion": 2, "checkedAt": CHECKED_AT, "seeds": rows}
    validated = validate(document)
    counts = Counter(row["version"] for row in validated)
    if counts != Counter({version: 100 for version in VERSIONS}):
        raise ValueError(f"October migration expected 100 per family, got {dict(counts)}")
    document["seeds"] = validated
    (DATA / "minecraft_java_seeds.json").write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (DATA / "retired_seeds.json").write_text(json.dumps({"checkedAt": CHECKED_AT, "rows": excluded}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Imported {len(validated)} unique seeds ({dict(counts)}); archived {len(excluded)} exclusions")


if __name__ == "__main__":
    main()
