# CHANGELOG

## V001
- Created on 2026-04-19
- Initial skill scaffold

## V002
- Bumped from V001 on 2026-04-19
- [Add change summary here]

## V003
- Bumped from V002 on 2026-04-19
- [Add change summary here]

## V004
- Bumped from V003 on 2026-04-19
- Added old-chat intake workflow and repo action classification
- Aligned generated skill structure to AISkills manifest-only doctrine
- Added progressive disclosure rules for skill-local references, assets, and scripts
- Updated skill ID guidance to underscore-based epcb IDs

## V005
- Bumped from V004 on 2026-04-19
- Preserved mode-selection guardrails in a clean bumped version after live V004 edits
- Formalized apply-mode-first behavior for old chat extraction requests
- Kept V004 archived as the historical version before this correction boundary
## V006
- Bumped from V005 on 2026-04-19
- Testing Command

## V007
- Bumped from V006 on 2026-04-19
- Force extraction output to be a single copy-pastable governed skill and reject non-epcb generated IDs

## V008
- Bumped from V007 on 2026-04-19
- Improve generated skill quality checks for source-specific examples, support layers, baseline modes, and changelog sync

## V009
- Bumped from V008 on 2026-04-19
- Force immediate classification mode when this skill is supplied as operating instructions
- Added first-response classification block for apply mode
- Added routing lock to prevent advisory-mode drift before classification
- Added current-visible-chat fallback when no separate transcript is supplied
- Added non-qualifying output rules for reject, insufficient, reference, asset, and script classifications
## V010
- Bumped from V009 on 2026-04-20
- Added Hard Constraints

## V011
- Bumped from V010 on 2026-04-20
- Added Required Skill Formatter for generated `skill.md` files
- Added exact frontmatter and level-one header requirements
- Added hard validation constraint requiring revision before output when a generated skill would fail repo validation
## V012
- Bumped from V011 on 2026-04-20
- Added Source Artifact Sanitation as a blocking pre-output gate
- Rejected AI citation markers such as `:contentReference` and `oaicite` in generated skills
- Rejected scaffold changelog leftovers in generated companion changelog guidance
## V013
- Bumped from V012 on 2026-04-20
- Added bounded RALPH validation loop with a two-pass maximum and explicit exit states
- Added Offline Copy-Paste Mode for assistants without repository or manifest access
- Required manifest-unavailable disclosure in validation notes
- Rejected `VP###` and separate production folders in favor of `V###`, `CURRENT`, and `MANIFEST.md`
## V014
- Bumped from V013 on 2026-04-20
- Harden copy-paste output with identity lock, exact header scan, single-artifact mode, and changelog sanitation
- Added exact single-artifact output contract for generated `skill.md` responses.
- Added user-supplied identity lock and canonical folder-name derivation rules.
- Added literal required-header preflight for level-one heading conformance.
- Added CHANGELOG sanitation rules banning scaffold, template, placeholder, and TODO language.
- Removed external repo command, support plan, and validation note requirements from copy-paste skill output.
## V015
- Bumped from V014 on 2026-04-22
- Separate repo-backed skill writes from offline copy-paste mode and require runtime-target validation for hardware workflows
- Added Repo-Backed Mode with manifest selection, `new_skill.sh`, `bump_skill.sh`, validation, and no offline manifest assumptions in live skills.
- Added runtime target gating for physical hardware and remote-runtime workflows.
- Required generated skills to include `# RALPH Loop` for stronger structure alignment.
## V016
- Bumped from V015 on 2026-04-22
- Compress live CTS body into progressive references and add optional clarification gates for token savings
- Moved detailed repo-backed, offline copy-paste, format, runtime-target, output, and RALPH rules into skill-local references.
- Added `assets/governed-skill-template.md` as the reusable generated-skill skeleton.
- Clarified that CTS does not impose a fixed word or character limit; AISkills validation and token economy are the governing limits.
- Added one-question clarification guidance for identity, runtime target, destructive scope, and validation authority.
