#!/usr/bin/env python3
"""Validate source JSON and generate browser data and the source table.

Usage: python tools/build_seed_data.py [--check]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from datetime import date
from pathlib import Path
from urllib.parse import quote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "minecraft_java_seeds.json"
OUTPUT = ROOT / "js" / "seeds.js"
MARKDOWN = ROOT / "data" / "minecraft_java_unique_biome_terrain_seeds.md"
HTML = ROOT / "index.html"
VERSIONS = ("26.3", "26.2", "26.1", "1.21")
EVIDENCE = {
    "publisher-tested": "출처에서 게임 확인",
    "source-listed": "출처에 버전 명시",
    "source-snapshot": "스냅샷 자료",
    "map-checked": "지도 계산 자료",
    "legacy-collection": "기존 목록 · 개별 재확인 전",
}
SEED_PATTERN = re.compile(r"(?:0|-[1-9]\d*|[1-9]\d*)\Z", re.ASCII)


def bounded_text(row: dict, key: str, limit: int, *, nullable: bool = False) -> None:
    value = row.get(key)
    if nullable and value is None:
        return
    if not isinstance(value, str) or not value.strip() or len(value) > limit:
        raise ValueError(f"{row.get('seed')}: invalid {key}")
    if any(ord(char) < 32 for char in value):
        raise ValueError(f"{row.get('seed')}: control character in {key}")


def validate(document: dict) -> list[dict]:
    if not isinstance(document, dict) or document.get("schemaVersion") != 2:
        raise ValueError("Expected source schemaVersion 2")
    date.fromisoformat(document["checkedAt"])
    rows = document.get("seeds")
    if not isinstance(rows, list) or not 1 <= len(rows) <= 1000:
        raise ValueError("Expected 1–1000 seeds")
    seen: set[str] = set()
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("Seed row must be an object")
        seed = row.get("seed")
        if not isinstance(seed, str) or len(seed) > 20 or not SEED_PATTERN.fullmatch(seed):
            raise ValueError(f"Invalid canonical integer seed: {seed!r}")
        if not -(2**63) <= int(seed) < 2**63:
            raise ValueError(f"Seed outside Java signed 64-bit range: {seed}")
        if seed in seen:
            raise ValueError(f"Duplicate seed across version buckets: {seed}")
        seen.add(seed)
        if row.get("version") not in VERSIONS:
            raise ValueError(f"{seed}: unsupported version")
        if row.get("verification") not in EVIDENCE:
            raise ValueError(f"{seed}: unsupported verification")
        bounded_text(row, "description", 500)
        bounded_text(row, "sourceName", 180)
        bounded_text(row, "sourceVersion", 180, nullable=True)
        bounded_text(row, "coordinates", 1000, nullable=True)
        bounded_text(row, "evidenceNotes", 1200, nullable=True)
        source_url = row.get("sourceUrl")
        if source_url is not None:
            bounded_text(row, "sourceUrl", 2000)
            parsed = urlsplit(source_url)
            if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
                raise ValueError(f"{seed}: source must be a public HTTPS URL without credentials")
            if any(char.isspace() for char in source_url) or "\\" in source_url:
                raise ValueError(f"{seed}: invalid source URL")
        if row.get("checkedAt") is not None:
            date.fromisoformat(row["checkedAt"])
        if row.get("publisherVerifiedAt") is not None:
            date.fromisoformat(row["publisherVerifiedAt"])
        if row["verification"] != "legacy-collection":
            if not source_url or not row.get("sourceVersion") or not row.get("checkedAt"):
                raise ValueError(f"{seed}: sourced entry needs URL, source version and check date")
    order = {version: index for index, version in enumerate(VERSIONS)}
    return [dict(row, id=index + 1) for index, row in enumerate(
        sorted(rows, key=lambda row: order[row["version"]])
    )]


def markdown_text(value: object) -> str:
    return str(value or "—").replace("&", "&amp;").replace("<", "&lt;").replace(
        ">", "&gt;"
    ).replace("|", "&#124;").replace("[", "&#91;").replace(
        "]", "&#93;"
    ).replace("\n", " ")


def render_markdown(rows: list[dict], checked_at: str) -> str:
    counts = Counter(row["version"] for row in rows)
    lines = [
        f"# Minecraft Java 독특한 바이옴·지형 시드 {len(rows)}선",
        "",
        f"- 자료 갱신일: {checked_at}",
        "- 원본 데이터: [minecraft_java_seeds.json](minecraft_java_seeds.json)",
        "- 기본 월드 유형, 구조물 생성 활성화, 지형 변경 모드·데이터팩 미사용 기준.",
        "- 모든 시드 숫자는 버전 간 중복 없이 한 번만 집계합니다. 여러 버전 호환을 의미하지 않습니다.",
        "",
        "## 버전별 수록 현황",
        "",
        "| 버전 | 개수 |",
        "|---|---:|",
        *[f"| Java {version} | {counts[version]} |" for version in VERSIONS],
        f"| 합계 | {len(rows)} |",
        "",
        "## 확인 방식",
        "",
        "‘출처에서 게임 확인’은 원문 작성자가 해당 버전에서 게임 확인했다고 명시한 자료입니다.",
        "이 사이트가 모든 시드를 직접 생성해 검증했다는 의미는 아닙니다.",
        "‘출처에 버전 명시’는 원문에 Java 호환 버전이 적혀 있는 자료이며 별도 게임 확인 기록을 보장하지 않습니다.",
        "스냅샷 자료는 정식 버전에서 재현되지 않을 수 있으며, 지도 계산 자료는 실제 청크 생성과 다를 수 있습니다.",
        "‘기존 목록 · 개별 재확인 전’은 기존 아카이브에서 유지한 항목입니다. 숫자를 원문에서 다시 찾은 경우에도 Java 에디션·세부 버전 근거가 부족하면 이 표시를 유지합니다.",
        "좌표는 원문에 명시된 경우에만 기록합니다. 출처 확인일은 원문을 읽은 날이며 게임 테스트 날짜가 아닙니다.",
        "",
        "## 공식 업데이트",
        "",
        "- [Java 26.3 정식 출시 노트](https://www.minecraft.net/en-us/article/minecraft-java-edition-26-3): 2026-09-15, Dappled Forest·Abandoned Camp 추가.",
        "- [26.4 Snapshot 1](https://www.minecraft.net/en-us/article/minecraft-26-4-snapshot-1): 2026-09-22 공개. 26.4 시드 호환은 이 목록에서 검증하지 않습니다.",
        "",
        "## 시드와 출처",
        "",
        "| 번호 | 버전 | 특징 | 시드 | 확인 방식 | 원문 버전 | 좌표 | 출처 | 비고 |",
        "|---:|---|---|---:|---|---|---|---|---|",
    ]
    for row in rows:
        if row.get("sourceUrl"):
            url = quote(row["sourceUrl"], safe=":/?=&%#@+,-_.~")
            source = f"[{markdown_text(row['sourceName'])}]({url})"
        else:
            source = "[기존 자료 모음](minecraft_java_unique_biome_terrain_seeds_251.md)"
        lines.append(
            f"| {row['id']} | Java {row['version']} | {markdown_text(row['description'])} | "
            f"`{row['seed']}` | {EVIDENCE[row['verification']]} | "
            f"{markdown_text(row.get('sourceVersion'))} | {markdown_text(row.get('coordinates'))} | "
            f"{source} | {markdown_text(row.get('evidenceNotes'))} |"
        )
    return "\n".join(lines) + "\n"


def render_outputs(document: dict) -> dict[Path, str]:
    rows = validate(document)
    metadata = {
        "checkedAt": document["checkedAt"],
        "total": len(rows),
        "counts": {version: sum(row["version"] == version for row in rows) for version in VERSIONS},
        "evidenceCounts": dict(Counter(row["verification"] for row in rows)),
    }
    # Number cannot hold signed 64-bit seeds exactly; always emit strings.
    javascript = (
        "// Generated from data/minecraft_java_seeds.json; do not edit directly.\n"
        "// Seeds remain strings to preserve Java signed 64-bit integers exactly.\n"
        f"window.MINECRAFT_SEED_METADATA = Object.freeze({json.dumps(metadata, ensure_ascii=False, indent=2)});\n"
        f"window.MINECRAFT_SEEDS = Object.freeze({json.dumps(rows, ensure_ascii=False, indent=2)});\n"
    )
    html = HTML.read_text(encoding="utf-8")
    total = len(rows)
    html = re.sub(r"시드 \d+선", f"시드 {total}선", html)
    html = re.sub(
        r'(<meta name="description" content=")[^"]+(">)',
        lambda match: match[1] + f"Minecraft Java Edition 26.3, 26.2, 26.1, 1.21 계열의 바이옴·지형 시드 {total}개. 출처·좌표·확인 방식을 살펴보고 검색·복사하세요." + match[2],
        html,
    )
    counts = dict(metadata["counts"], all=total)
    for version, count in counts.items():
        html = re.sub(
            rf'(<dd data-stat="{re.escape(version)}">)\d+(</dd>)',
            lambda match: f"{match[1]}{count}{match[2]}", html,
        )
        html = re.sub(
            rf'(<button type="button" data-version="{re.escape(version)}"[^>]*>[^<]*<span>)\d+(</span>)',
            lambda match: f"{match[1]}{count}{match[2]}", html,
        )
    html = re.sub(r'(<p id="result-summary"[^>]*><strong>)\d+(</strong>)',
                  lambda match: f"{match[1]}{total}{match[2]}", html)
    # Static hosting and browser previews can retain previous script responses.
    # Content versions make data/code/style updates load together on the next visit.
    asset_contents = {"js/seeds.js": javascript.encode("utf-8"),
                      "js/app.js": (ROOT / "js" / "app.js").read_bytes(),
                      "css/styles.css": (ROOT / "css" / "styles.css").read_bytes()}
    for asset, content in asset_contents.items():
        digest = hashlib.sha256(content).hexdigest()[:12]
        html = re.sub(rf'({re.escape(asset)})(?:\?v=[a-zA-Z0-9]+)?(?=")',
                      lambda match: f"{match[1]}?v={digest}", html)
    return {OUTPUT: javascript, MARKDOWN: render_markdown(rows, document["checkedAt"]), HTML: html}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Validate and detect stale generated files without writing")
    args = parser.parse_args()
    document = json.loads(SOURCE.read_text(encoding="utf-8"))
    outputs = render_outputs(document)
    for path, content in outputs.items():
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                raise ValueError(f"Stale generated file: {path.relative_to(ROOT)}")
        else:
            path.write_text(content, encoding="utf-8")
    counts = Counter(row["version"] for row in document["seeds"])
    print(f"{'Checked' if args.check else 'Generated'} {len(document['seeds'])} unique seeds: {dict(counts)}")


if __name__ == "__main__":
    main()
