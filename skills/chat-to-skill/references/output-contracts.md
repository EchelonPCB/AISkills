# Output Contracts

Use this reference before returning or writing generated artifacts.

## Sanitation

Remove:

- AI citation markers such as `:contentReference` and `oaicite`
- markdown wrapper prose inside saved `skill.md` files
- scaffold wording such as placeholder changelog notes
- template-only language such as unresolved TODO instructions
- stale assumptions from earlier chats
- hidden provenance claims that cannot be verified from available inputs

## Single Artifact Mode

When the user asks for one `skill.md`, return one `skill.md`.

Do not include:

- companion changelog text
- shell commands
- support-file plans
- validation explanations
- extra markdown outside the fenced block

## Repo Transaction Mode

When writing directly in the repo, report:

1. classification
2. files changed
3. validation result
4. blockers or target-runtime handoff, if any

Do not paste the full skill body unless the user asks for it.
