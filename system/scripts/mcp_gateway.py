#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT_DIR = ROOT / "system" / "scripts"
MUTATIONS = ROOT / "workspace" / "mutations"
sys.dont_write_bytecode = True


def setup_imports():
    os.chdir(ROOT)
    sys.path.insert(0, str(SCRIPT_DIR))


def emit(payload: dict, status: int = 0) -> int:
    print(json.dumps(payload, indent=2, sort_keys=True))
    return status


def command_result(command: list[str]) -> dict:
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    return {
        "command": command,
        "returncode": result.returncode,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
        "ok": result.returncode == 0,
    }


def record_to_payload(record) -> dict:
    return {
        "skill_name": record.name,
        "folder": record.folder,
        "skill_id": record.skill_id,
        "description": record.description,
        "trigger_keywords": [
            keyword.strip()
            for keyword in record.trigger_keywords.split(",")
            if keyword.strip()
        ],
        "trigger_keywords_raw": record.trigger_keywords,
        "current_version": record.current_version,
        "current_path": record.current_path.as_posix(),
    }


def list_skills(args) -> int:
    setup_imports()
    from update_index import collect_skills

    records, errors = collect_skills()
    payload = {
        "ok": not errors,
        "count": len(records),
        "skills": [record_to_payload(record) for record in records],
        "errors": errors,
    }
    return emit(payload, 0 if not errors else 1)


def resolve_skill(identifier: str):
    setup_imports()
    from update_index import collect_skills

    records, errors = collect_skills()
    if errors:
        return None, errors

    needle = identifier.lower()
    matches = []
    for record in records:
        candidates = {
            record.folder.lower(),
            record.name.lower(),
            record.skill_id.lower(),
            record.current_path.as_posix().lower(),
        }
        if needle in candidates:
            matches.append(record)

    if len(matches) == 1:
        return matches[0], []
    if len(matches) > 1:
        return None, [f"ambiguous skill identifier {identifier!r}"]

    fuzzy = [
        record
        for record in records
        if needle in record.folder.lower()
        or needle in record.name.lower()
        or needle in record.skill_id.lower()
    ]
    if len(fuzzy) == 1:
        return fuzzy[0], []
    if len(fuzzy) > 1:
        return None, [f"ambiguous skill identifier {identifier!r}"]
    return None, [f"unknown skill identifier {identifier!r}"]


def read_skill(args) -> int:
    record, errors = resolve_skill(args.skill)
    if errors:
        return emit({"ok": False, "errors": errors}, 1)

    path = ROOT / record.current_path
    if not path.exists():
        return emit({"ok": False, "errors": [f"missing current_path {record.current_path}"]}, 1)

    payload = record_to_payload(record)
    payload.update({"ok": True, "text": path.read_text()})
    return emit(payload)


def select_skill(args) -> int:
    setup_imports()
    import select_skill as selector

    records = selector.parse_manifest(ROOT / "MANIFEST.md")
    matches = selector.rank_skills(args.query, records)
    visible = selector.visible_matches(matches, args.top, args.min_score)
    payload = []
    for index, match in enumerate(visible):
        runner_up = visible[index + 1] if index + 1 < len(visible) else None
        assessment = selector.assess_match(match, runner_up)
        payload.append(
            {
                "score": match.score,
                "confidence": assessment.confidence,
                "ambiguous": assessment.ambiguous,
                "score_gap": assessment.score_gap,
                "routing_reason": assessment.reason,
                "matched_terms": match.matched_terms,
                **asdict(match.record),
            }
        )
    return emit({"ok": True, "matches": payload})


def validate_repo(args) -> int:
    update = command_result(["python3", "system/scripts/update_index.py", "--check"])
    validate = command_result(["python3", "system/scripts/validate_skills.py"])
    payload = {
        "ok": update["ok"] and validate["ok"],
        "index_check": update,
        "skill_validation": validate,
    }
    return emit(payload, 0 if payload["ok"] else 1)


def list_mutations(args) -> int:
    mutations = []
    if MUTATIONS.exists():
        for stage_dir in sorted(path for path in MUTATIONS.iterdir() if path.is_dir()):
            current_file = stage_dir / "CURRENT"
            current = current_file.read_text().strip() if current_file.exists() else None
            current_skill = stage_dir / current / "skill.md" if current else None
            checklist = stage_dir / "references" / "promotion-checklist.md"
            recommendation = None
            if checklist.exists():
                for line in checklist.read_text().splitlines():
                    if line.lower().startswith("recommendation:"):
                        recommendation = line.split(":", 1)[1].strip()
                        break
            mutations.append(
                {
                    "name": stage_dir.name,
                    "path": stage_dir.relative_to(ROOT).as_posix(),
                    "current_version": current,
                    "current_skill_path": current_skill.relative_to(ROOT).as_posix()
                    if current_skill and current_skill.exists()
                    else None,
                    "promotion_recommendation": recommendation,
                }
            )
    return emit({"ok": True, "count": len(mutations), "mutations": mutations})


def validate_mutation(args) -> int:
    setup_imports()
    import validate_mutation as validator

    payload = validator.validate_mutation(
        validator.resolve_stage_dir(args.mutation),
        args.promotable,
    )
    return emit(payload, 0 if payload["ok"] else 1)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="JSON gateway for MCP-safe AISkills operations."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("list-skills", help="List live skills from the governed index").set_defaults(func=list_skills)

    read = sub.add_parser("read-skill", help="Read one live skill by folder, name, skill_id, or current_path")
    read.add_argument("skill")
    read.set_defaults(func=read_skill)

    select = sub.add_parser("select-skill", help="Route a task to candidate skills")
    select.add_argument("query")
    select.add_argument("--top", type=int, default=3)
    select.add_argument("--min-score", type=float, default=6.0)
    select.set_defaults(func=select_skill)

    sub.add_parser("validate-repo", help="Check generated indexes and validate live skills").set_defaults(func=validate_repo)
    sub.add_parser("list-mutations", help="List staged mutation workspaces").set_defaults(func=list_mutations)

    mutation = sub.add_parser("validate-mutation", help="Validate a staged mutation workspace")
    mutation.add_argument("mutation")
    mutation.add_argument("--promotable", action="store_true")
    mutation.set_defaults(func=validate_mutation)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
