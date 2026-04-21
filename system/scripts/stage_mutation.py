#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MUTATIONS = ROOT / "workspace" / "mutations"

REQUIRED_SECTIONS = (
    "# Index",
    "# Objective",
    "# Trigger",
    "# Do Not Use When",
    "# Required Inputs",
    "# Optional Inputs",
    "# Outputs",
    "# Support Layers",
    "# Procedure",
    "# Decision Logic",
    "# Validation",
    "# Rules",
    "# Failure Modes",
    "# Dependencies",
    "# Assumptions",
    "# Change Log",
)


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "mutation"


def id_token(value: str) -> str:
    return slugify(value).replace("-", "_")


def yaml_quote(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ")
    return f'"{escaped}"'


def acronym(value: str) -> str:
    return "".join(part[0] for part in re.split(r"[^a-z0-9]+", value.lower()) if part)


def load_records():
    os.chdir(ROOT)
    sys.path.insert(0, str(ROOT / "system" / "scripts"))
    from update_index import collect_skills

    records, errors = collect_skills()
    if errors:
        for error in errors:
            print(f"WARNING: {error}", file=sys.stderr)
        print(
            "WARNING: continuing with resolvable live skills only; fix repo hygiene before promotion.",
            file=sys.stderr,
        )
    if not records:
        print("ERROR: no live skills could be collected", file=sys.stderr)
        raise SystemExit(1)
    return records


def resolve_skill(token: str, records):
    normalized = slugify(token)
    token_lower = token.lower()

    exact = []
    for record in records:
        candidates = {
            record.folder.lower(),
            record.name.lower(),
            slugify(record.name),
            record.skill_id.lower(),
            acronym(record.folder),
            acronym(record.name),
        }
        if token_lower in candidates or normalized in candidates:
            exact.append(record)

    if len(exact) == 1:
        return exact[0]
    if len(exact) > 1:
        fail_ambiguous(token, exact)

    fuzzy = [
        record
        for record in records
        if normalized in slugify(record.folder)
        or normalized in slugify(record.name)
        or token_lower in record.skill_id.lower()
    ]
    if len(fuzzy) == 1:
        return fuzzy[0]
    if len(fuzzy) > 1:
        fail_ambiguous(token, fuzzy)

    print(f"ERROR: could not resolve parent skill {token!r}", file=sys.stderr)
    print("Hint: use the skill folder name, frontmatter name, skill_id, or acronym.", file=sys.stderr)
    raise SystemExit(1)


def fail_ambiguous(token: str, matches):
    print(f"ERROR: parent skill {token!r} is ambiguous:", file=sys.stderr)
    for record in matches:
        print(f"  - {record.folder} ({record.skill_id})", file=sys.stderr)
    raise SystemExit(1)


def default_mutation_name(records) -> str:
    names = [record.folder for record in records]
    if len(names) <= 3:
        base = "-".join(names)
    else:
        base = "-".join(names[:2] + [f"plus-{len(names) - 2}"])
    return slugify(f"{base}-mutation")


def section_text(text: str, heading: str) -> str:
    lines = text.splitlines()
    start = None
    for index, line in enumerate(lines):
        if line.strip() == heading:
            start = index + 1
            break
    if start is None:
        return ""

    collected = []
    for line in lines[start:]:
        if line.startswith("# "):
            break
        collected.append(line)
    return "\n".join(collected).strip()


def section_excerpt(text: str, heading: str, max_chars: int = 520) -> str:
    value = section_text(text, heading)
    value = re.sub(r"\s+", " ", value).strip()
    return value[:max_chars] if value else ""


def parent_signal(records, heading: str) -> str:
    rows = []
    for record in records:
        text = record.current_path.read_text()
        excerpt = section_excerpt(text, heading) or "No clear section signal found."
        rows.append(f"- `{record.folder}` `{record.current_version}`: {excerpt}")
    return "\n".join(rows)


def parent_list(records) -> str:
    return ", ".join(f"{record.folder} {record.current_version}" for record in records)


def render_skill(name: str, goal: str, records) -> str:
    today = date.today().isoformat()
    parents = parent_list(records)
    description = f"Staged mutation skill for {goal}, seeded from {parents}."
    trigger_keywords = f"mutate skill, combine skills, {name.replace('-', ' ')}, {goal}"
    parent_dependency_rows = "\n".join(
        f"- `parents/{record.folder}/{record.current_version}/skill.md`"
        for record in records
    )
    index_rows = "\n".join(
        f"| {section.removeprefix('# ')} | {section.removeprefix('# ')} guidance |"
        for section in REQUIRED_SECTIONS
    )

    return f"""---
build_number: "001"
skill_id: "epcb.mutated.{id_token(name)}"
name: "{name}"
description: {yaml_quote(description)}
trigger_keywords: {yaml_quote(trigger_keywords)}
owner: "EPCB"
status: "draft"
created_at: "{today}"
last_updated: "{today}"
---

# Index

| Section | Description |
|--------|-------------|
{index_rows}

---

# Objective

Create a reusable workflow for {goal}.

SYNTHESIS_REQUIRED: This staged candidate is seeded from parent skill signals. A connected AI must rewrite this file so the promoted version describes the mutated runtime behavior directly, not the staging process.

Parent objective signals:

{parent_signal(records, "# Objective")}

---

# Trigger

Use this skill when:

- a user needs a repeatable workflow for {goal}
- the task requires capabilities from more than one parent skill
- the output must be converted into one self-contained AISkills `skill.md`

Parent trigger signals:

{parent_signal(records, "# Trigger")}

---

# Do Not Use When

- one parent skill can handle the task without synthesis
- the desired output is only a note, asset, checklist, or reference file
- parent rules conflict and no human decision has resolved the conflict
- the mutation goal is not reusable beyond one isolated request

Parent exclusion signals:

{parent_signal(records, "# Do Not Use When")}

---

# Required Inputs

1. Source material needed to perform: {goal}
2. Parent snapshots listed in the Dependencies section
3. Mutation brief at `references/mutation-brief.md`
4. Parent mapping at `references/parent-map.md`
5. Merge notes at `references/merge-notes.md`

Parent input signals:

{parent_signal(records, "# Required Inputs")}

---

# Optional Inputs

- Example source chats, contracts, or task records relevant to {goal}
- Naming, domain, owner, or skill ID overrides
- Acceptance criteria supplied by a human reviewer
- Existing support files that should become references, assets, or scripts

---

# Outputs

1. One complete mutated `skill.md` that performs {goal}
2. Updated `references/parent-map.md` explaining which parent components were kept, modified, discarded, or conflicted
3. Updated `references/merge-notes.md` resolving rule, trigger, input, output, dependency, and validation conflicts
4. Updated `references/promotion-checklist.md` with the final recommendation

Parent output signals:

{parent_signal(records, "# Outputs")}

---

# Support Layers

- Parent snapshot layer: immutable parent skills under `parents/<skill>/<V###>/skill.md`
- Mutation brief layer: target behavior and AI work order in `references/mutation-brief.md`
- Parent map layer: explicit component mapping in `references/parent-map.md`
- Merge notes layer: conflict resolution in `references/merge-notes.md`
- Promotion layer: approval gate in `references/promotion-checklist.md`

---

# Procedure

## 1. Read Parent Evidence

1.1 Read `references/mutation-brief.md` first.
1.2 Read each parent snapshot listed in Dependencies.
1.3 Identify the parent behavior that directly supports {goal}.
1.4 Ignore parent content that only serves the parent skill's original artifact type.

## 2. Synthesize The Mutated Skill

2.1 Rewrite this `skill.md` so the Objective states the new runtime behavior directly.
2.2 Convert parent triggers into a single non-overlapping trigger set.
2.3 Merge required inputs into the minimum inputs needed for the mutated workflow.
2.4 Merge outputs into one clear deliverable contract.
2.5 Convert parent procedures into one ordered workflow.
2.6 Resolve parent conflicts in `references/merge-notes.md` before promotion.

## 3. Run Bounded RALPH

3.1 Reaffirm every required AISkills frontmatter field and section.
3.2 Audit alignment with the mutation goal.
3.3 Lock layout, lineage, and versioning.
3.4 Purge scaffold markers, hidden context, copied citation artifacts, and staging-only text.
3.5 Halt after two passes with PASS, CONDITIONAL PASS, REVISE, or REJECT.

---

# Decision Logic

| Condition | Action |
|----------|--------|
| one parent fully covers the task | reject mutation and use that parent skill |
| source material is missing | request the missing material |
| parent instructions conflict | resolve in `references/merge-notes.md` before editing the candidate |
| candidate still contains synthesis-required markers | keep staged and do not promote |
| promotion checklist says revise or reject | keep staged and continue editing |
| promotion checklist says promote and human approval is explicit | run `promote_mutation.py <mutation-name> --approve` |

---

# Validation

A promotion-ready mutated skill must:

1. State {goal} as a self-contained runtime behavior.
2. Preserve only parent instructions that serve the mutation goal.
3. Remove staging-only language, including this synthesis-required notice.
4. Include all required AISkills frontmatter fields and sections.
5. Include at least three useful trigger keywords.
6. Pass `python3 system/scripts/validate_skills.py` after promotion.
7. Have `references/promotion-checklist.md` set to `Recommendation: promote`.

Parent validation signals:

{parent_signal(records, "# Validation")}

---

# Rules

- Do not concatenate parent skill bodies.
- Do not preserve parent content that does not serve {goal}.
- Do not promote while synthesis-required or staging-only language remains.
- Do not bypass human approval.
- Do not create `VP###`, `production/`, or alternate production folders.

Parent rule signals:

{parent_signal(records, "# Rules")}

---

# Failure Modes

| Failure | Recovery |
|--------|----------|
| mutation remains a parent bundle | rewrite into one runtime workflow |
| parent conflict is unresolved | stop and request a human decision |
| candidate fails formatter requirements | revise before promotion |
| RALPH does not converge after two passes | halt and record blockers in the promotion checklist |

---

# Dependencies

Parent skill snapshots:

{parent_dependency_rows}

Mutation references:

- `references/mutation-brief.md`
- `references/parent-map.md`
- `references/merge-notes.md`
- `references/promotion-checklist.md`

---

# Assumptions

- Parent snapshots represent the exact versions selected for mutation.
- The connected AI can read the parent folder and rewrite this staged file before promotion.
- The promoted skill should be self-contained and should not require reading the mutation workspace at runtime.

---

# Change Log

## V001
- Created staged mutation candidate from {parents} for {goal}.
"""


def render_mutation_brief(name: str, goal: str, records) -> str:
    today = date.today().isoformat()
    rows = "\n".join(
        f"- `{record.folder}` `{record.current_version}`: `{record.skill_id}` — {record.description}"
        for record in records
    )
    return f"""# Mutation Brief: {name}

Created: {today}
Current candidate: `CURRENT` -> `V001/skill.md`

## Goal

{goal}

## Parent Skills

{rows}

## AI Work Order

1. Read this brief.
2. Read every file under `parents/<skill>/<V###>/skill.md`.
3. Read `references/parent-map.md` and `references/merge-notes.md`.
4. Rewrite `V001/skill.md` into a self-contained mutated skill that performs the goal directly.
5. Remove `SYNTHESIS_REQUIRED` and staging-only language before promotion.
6. Update `references/promotion-checklist.md`.
7. Set `Recommendation: promote` only when the candidate is ready for human-approved promotion.
"""


def render_parent_map(name: str, goal: str, records) -> str:
    lines = [
        f"# Parent Map: {name}",
        "",
        f"Mutation goal: {goal}",
        "",
        "| Parent | Version | Snapshot | Primary Contribution | Keep / Modify / Discard / Conflict |",
        "|--------|---------|----------|----------------------|------------------------------------|",
    ]
    for record in records:
        snapshot = f"parents/{record.folder}/{record.current_version}/skill.md"
        objective = section_excerpt(record.current_path.read_text(), "# Objective", 180)
        lines.append(
            f"| {record.folder} | {record.current_version} | {snapshot} | {objective} | SYNTHESIS_REQUIRED |"
        )

    lines.extend(["", "## Component Mapping", ""])
    for record in records:
        text = record.current_path.read_text()
        lines.extend(
            [
                f"### {record.folder} {record.current_version}",
                "",
                f"- Objective signal: {section_excerpt(text, '# Objective') or 'No signal found.'}",
                f"- Trigger signal: {section_excerpt(text, '# Trigger') or 'No signal found.'}",
                f"- Required input signal: {section_excerpt(text, '# Required Inputs') or 'No signal found.'}",
                f"- Output signal: {section_excerpt(text, '# Outputs') or 'No signal found.'}",
                f"- Validation signal: {section_excerpt(text, '# Validation') or 'No signal found.'}",
                "- Keep: SYNTHESIS_REQUIRED",
                "- Modify: SYNTHESIS_REQUIRED",
                "- Discard: SYNTHESIS_REQUIRED",
                "- Conflicts: SYNTHESIS_REQUIRED",
                "",
            ]
        )
    return "\n".join(lines)


def render_merge_notes(name: str, records) -> str:
    parents = ", ".join(record.folder for record in records)
    return f"""# Merge Notes: {name}

Parents: {parents}

Use this file to resolve synthesis issues before promotion.

| Surface | Merge Question | Resolution |
|---------|----------------|------------|
| Trigger | Which tasks should activate the mutated skill instead of either parent? | SYNTHESIS_REQUIRED |
| Inputs | Which parent inputs are still required after mutation? | SYNTHESIS_REQUIRED |
| Outputs | What is the one deliverable produced by the mutated skill? | SYNTHESIS_REQUIRED |
| Procedure | What parent steps become the final ordered workflow? | SYNTHESIS_REQUIRED |
| Decision Logic | Which escalation and rejection rules survive? | SYNTHESIS_REQUIRED |
| Validation | Which parent validation gates become mandatory? | SYNTHESIS_REQUIRED |
| Rules | Which parent rules conflict or need narrowing? | SYNTHESIS_REQUIRED |
| Dependencies | Which parent dependencies remain runtime dependencies? | SYNTHESIS_REQUIRED |

## Open Human Decisions

- SYNTHESIS_REQUIRED
"""


def render_promotion_checklist(name: str) -> str:
    return f"""# Promotion Checklist: {name}

Recommendation: revise

## Required Before Promotion

- `CURRENT` points to the candidate version.
- `CURRENT` -> `V###/skill.md` is the only candidate skill file.
- Candidate has no `SYNTHESIS_REQUIRED`, `DRAFT`, or `TODO` markers.
- Candidate describes the mutated runtime behavior directly.
- Candidate does not tell the runtime AI to read the mutation workspace.
- `references/parent-map.md` has no unresolved parent mapping rows.
- `references/merge-notes.md` has no unresolved conflict rows.
- RALPH completed in no more than two passes.
- Human approval is ready.

## RALPH Result

- R: SYNTHESIS_REQUIRED
- A: SYNTHESIS_REQUIRED
- L: SYNTHESIS_REQUIRED
- P: SYNTHESIS_REQUIRED
- H: SYNTHESIS_REQUIRED

## Promotion Notes

Set `Recommendation: promote` only after the checklist is true and the candidate is ready for `promote_mutation.py <mutation-name> --approve`.
"""


def render_parent_metadata(record) -> str:
    return f"""# Parent Snapshot Metadata

Skill: `{record.folder}`
Version: `{record.current_version}`
Skill ID: `{record.skill_id}`
Source path: `{record.current_path.as_posix()}`
Description: {record.description}
Trigger keywords: {record.trigger_keywords}
"""


def render_changelog(name: str, goal: str, records) -> str:
    today = date.today().isoformat()
    parents = parent_list(records)
    return f"""# CHANGELOG

## V001
- Created on {today}
- Staged mutation `{name}` from {parents}.
- Goal: {goal}
"""


def write_file(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n")


def touch_keep(path: Path):
    path.mkdir(parents=True, exist_ok=True)
    (path / ".gitkeep").write_text("")


def stage_mutation(args):
    records = load_records()
    parents = [resolve_skill(token, records) for token in args.parents]
    unique = []
    seen = set()
    for record in parents:
        if record.folder in seen:
            continue
        seen.add(record.folder)
        unique.append(record)

    if len(unique) < 2:
        print("ERROR: mutation staging requires two or more distinct parent skills", file=sys.stderr)
        return 1

    name = slugify(args.name) if args.name else default_mutation_name(unique)
    goal = args.goal or f"combine {', '.join(record.folder for record in unique)} into one validated skill"
    mutation_dir = MUTATIONS / name

    print(f"Mutation: {name}")
    print("Parents:")
    for record in unique:
        print(f"  - {record.folder} ({record.current_version})")
    print(f"Goal: {goal}")
    print(f"Staging path: {mutation_dir.relative_to(ROOT)}")

    if args.dry_run:
        return 0

    if mutation_dir.exists():
        print(
            f"ERROR: {mutation_dir.relative_to(ROOT)} already exists. "
            "Use --name for a new mutation folder.",
            file=sys.stderr,
        )
        return 1

    write_file(mutation_dir / "CURRENT", "V001")
    touch_keep(mutation_dir / "archived")
    touch_keep(mutation_dir / "assets")
    touch_keep(mutation_dir / "scripts")
    (mutation_dir / "references").mkdir(parents=True, exist_ok=True)

    for record in unique:
        parent_dir = mutation_dir / "parents" / record.folder / record.current_version
        write_file(parent_dir / "skill.md", record.current_path.read_text())
        write_file(parent_dir / "metadata.md", render_parent_metadata(record))

    write_file(mutation_dir / "V001" / "skill.md", render_skill(name, goal, unique))
    write_file(mutation_dir / "references" / "mutation-brief.md", render_mutation_brief(name, goal, unique))
    write_file(mutation_dir / "references" / "parent-map.md", render_parent_map(name, goal, unique))
    write_file(mutation_dir / "references" / "merge-notes.md", render_merge_notes(name, unique))
    write_file(mutation_dir / "references" / "promotion-checklist.md", render_promotion_checklist(name))
    write_file(mutation_dir / "CHANGELOG.md", render_changelog(name, goal, unique))

    print("")
    print("Created mutation staging workspace.")
    print("Next:")
    print(f"  1. Read workspace/mutations/{name}/references/mutation-brief.md")
    print(f"  2. Rewrite workspace/mutations/{name}/V001/skill.md into the actual mutated skill")
    print(f"  3. Resolve SYNTHESIS_REQUIRED markers in references/parent-map.md and references/merge-notes.md")
    print(f"  4. Set references/promotion-checklist.md to `Recommendation: promote` when ready")
    print(f"  5. Promote with: python3 system/scripts/promote_mutation.py {name} --approve")
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="Stage a higher-risk mutated skill from two or more live parent skills."
    )
    parser.add_argument("parents", nargs="+", help="parent skill folder/name/skill_id/acronym")
    parser.add_argument("--name", help="mutation folder and candidate skill name")
    parser.add_argument("--goal", help="one-sentence mutation goal")
    parser.add_argument("--dry-run", action="store_true", help="show resolved parents without writing files")
    args = parser.parse_args()
    return stage_mutation(args)


if __name__ == "__main__":
    raise SystemExit(main())
