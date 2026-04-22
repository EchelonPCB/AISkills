# Offline Copy-Paste Mode

Use this mode only when the assistant cannot access AISkills files, indexes, or MCP tools.

## Output Contract

- Return exactly one fenced markdown block containing the complete `skill.md`.
- The first character inside the fenced block must be `-` from the opening YAML delimiter `---`.
- Do not include shell commands, validation notes, changelog companion text, support plans, or commentary inside the fenced block.
- If duplicate checking cannot be performed, include this sentence only inside the generated skill's `# Assumptions` section: `Manifest unavailable; duplicate check not performed.`

## Safety

- Preserve user-supplied identity if provided.
- If folder path and frontmatter `name` conflict, ask which identity is authoritative before generating.
- If source material is too vague to produce a reusable procedure, classify as `insufficient` and ask one concise question.
- Do not pretend repo validation ran.
