# RALPH Gate

Run at most two passes.

## Pass

- Reaffirm requirements: identity, source scope, required fields, runtime target, output mode.
- Audit alignment: generated skill matches source behavior and AISkills structure.
- Lock layout and lineage: repo-backed changes use `V###`, `CURRENT`, `MANIFEST.md`, and support files correctly.
- Purge provenance problems: remove stale chat assumptions, citation artifacts, placeholders, and invalid scaffold text.
- Halt or hand off: PASS, CONDITIONAL PASS, or concrete blockers.

## Exit States

- PASS: structure and validation requirements are satisfied.
- CONDITIONAL PASS: offline copy-paste output is structurally valid but repo duplicate checks cannot run.
- HAND OFF: unresolved blockers remain after two passes, especially target-runtime hardware checks.
