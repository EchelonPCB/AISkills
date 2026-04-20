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
