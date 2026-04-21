# Promotion Checklist: chat-to-contracts

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
