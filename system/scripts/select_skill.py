from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


ROOT = Path(".")
DEFAULT_MANIFEST = ROOT / "MANIFEST.md"
WORD_RE = re.compile(r"[a-z0-9_]+")
SEPARATOR_RE = re.compile(r"^-+$")
STOPWORDS = {
    "a",
    "an",
    "and",
    "as",
    "for",
    "from",
    "in",
    "into",
    "of",
    "on",
    "or",
    "the",
    "this",
    "to",
    "with",
}


@dataclass(frozen=True)
class SkillRecord:
    skill_name: str
    skill_id: str
    description: str
    trigger_keywords: str
    current_version: str
    current_path: str


@dataclass(frozen=True)
class SkillMatch:
    score: float
    matched_terms: list[str]
    record: SkillRecord


def split_markdown_row(line: str) -> list[str]:
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]

    cells: list[str] = []
    current: list[str] = []
    escaped = False

    for char in line:
        if escaped:
            current.append(char)
            escaped = False
            continue
        if char == "\\":
            escaped = True
            continue
        if char == "|":
            cells.append("".join(current).strip())
            current = []
            continue
        current.append(char)

    cells.append("".join(current).strip())
    return cells


def parse_manifest(path: Path) -> list[SkillRecord]:
    if not path.exists():
        raise FileNotFoundError(f"Missing manifest: {path}")

    records: list[SkillRecord] = []
    for line in path.read_text().splitlines():
        if not line.startswith("|"):
            continue
        cells = split_markdown_row(line)
        if len(cells) != 6:
            continue
        if cells[0] == "skill_name" or SEPARATOR_RE.fullmatch(cells[0]):
            continue
        records.append(SkillRecord(*cells))
    return records


def tokenize(value: str) -> set[str]:
    normalized = value.lower().replace("-", "_")
    tokens = {token for token in WORD_RE.findall(normalized) if token not in STOPWORDS}
    expanded: set[str] = set()
    for token in tokens:
        expanded.add(token)
        expanded.update(part for part in token.split("_") if part and part not in STOPWORDS)
    return expanded


def compact(value: str) -> str:
    return re.sub(r"\s+", " ", value.lower()).strip()


def score_record(query: str, record: SkillRecord) -> SkillMatch:
    query_tokens = tokenize(query)
    fields = {
        record.skill_name: 4.0,
        record.skill_id: 3.0,
        record.description: 3.0,
        record.trigger_keywords: 5.0,
    }

    score = 0.0
    matched_terms: set[str] = set()

    for text, weight in fields.items():
        field_tokens = tokenize(text)
        overlap = query_tokens & field_tokens
        score += len(overlap) * weight
        matched_terms.update(overlap)

    query_text = compact(query)
    for keyword in [part.strip().lower() for part in record.trigger_keywords.split(",")]:
        if keyword and keyword in query_text:
            score += 8.0
            matched_terms.add(keyword)

    name_phrase = record.skill_name.replace("-", " ")
    if name_phrase in query_text:
        score += 10.0
        matched_terms.add(name_phrase)

    return SkillMatch(score=score, matched_terms=sorted(matched_terms), record=record)


def rank_skills(query: str, records: list[SkillRecord]) -> list[SkillMatch]:
    matches = [score_record(query, record) for record in records]
    return sorted(matches, key=lambda match: (-match.score, match.record.skill_name))


def print_plain(matches: list[SkillMatch], top: int, min_score: float) -> None:
    visible = [match for match in matches if match.score > 0 and match.score >= min_score][:top]
    if not visible:
        print("No confident skill match.")
        return

    for index, match in enumerate(visible, start=1):
        record = match.record
        terms = ", ".join(match.matched_terms) if match.matched_terms else "none"
        print(f"{index}. {record.skill_name} | score: {match.score:.1f}")
        print(f"   id: {record.skill_id}")
        print(f"   description: {record.description}")
        print(f"   keywords: {record.trigger_keywords}")
        print(f"   version: {record.current_version}")
        print(f"   path: {record.current_path}")
        print(f"   matched: {terms}")


def print_json(matches: list[SkillMatch], top: int, min_score: float) -> None:
    visible = [match for match in matches if match.score > 0 and match.score >= min_score][:top]
    payload = [
        {
            "score": match.score,
            "matched_terms": match.matched_terms,
            **asdict(match.record),
        }
        for match in visible
    ]
    print(json.dumps(payload, indent=2))


def show_skill(match: SkillMatch) -> int:
    path = Path(match.record.current_path)
    if not path.exists():
        print(f"ERROR: selected skill path does not exist: {path}", file=sys.stderr)
        return 1

    print("")
    print(f"# Selected Skill: {match.record.skill_name}")
    print(f"# Skill ID: {match.record.skill_id}")
    print(f"# Path: {match.record.current_path}")
    print("")
    print(path.read_text())
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Select AISkills from MANIFEST.md without scanning every skill body."
    )
    parser.add_argument("query", help="User task or search phrase")
    parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST), help="Path to MANIFEST.md")
    parser.add_argument("--top", type=int, default=3, help="Number of matches to print")
    parser.add_argument("--min-score", type=float, default=0.0, help="Minimum score to print")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON")
    parser.add_argument(
        "--show",
        action="store_true",
        help="Print the best matching live skill.md after the match list",
    )
    args = parser.parse_args()

    try:
        records = parse_manifest(Path(args.manifest))
    except OSError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    matches = rank_skills(args.query, records)

    if args.json:
        print_json(matches, args.top, args.min_score)
    else:
        print_plain(matches, args.top, args.min_score)

    if args.show:
        visible = [match for match in matches if match.score > 0 and match.score >= args.min_score]
        if not visible:
            return 2
        return show_skill(visible[0])

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
