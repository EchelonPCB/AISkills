---
build_number: "001"
skill_id: "epcb.content.infographic_generator"
name: "infographic-generator"
description: "Creates brand-aligned infographic concepts, visualization options, and image-generation prompts from user content."
trigger_keywords: "infographic, generate graphic, visualize content, image prompt, design concept"
owner: "EPCB"
status: "active"
created_at: "2026-04-18"
last_updated: "2026-04-18"
---

# Objective

Generate high-quality infographic concepts from a user’s content, guide the user through selecting a direction, and produce a strong final image-generation prompt aligned to the desired brand style and output format.

# Trigger

Use this skill whenever the user wants to:
- create an infographic
- turn content into a visual
- generate infographic ideas
- create a visual explainer from text
- convert a post, notes, article, or concept into an infographic workflow

# Required Inputs

1. Core content to visualize
2. Desired destination or platform
   - LinkedIn
   - newsletter
   - presentation
   - website
   - other
3. Desired output format
   - prompt only
   - concept options
   - full infographic workflow
   - image-generation prompt
4. Brand or style reference
   - direct instructions
   - reference files
   - examples
   - or fallback style guidance

# Optional Inputs

1. Target audience
2. Tone
3. Visual density
4. Preferred infographic type
   - timeline
   - comparison
   - process
   - hierarchy
   - checklist
   - flowchart
   - data snapshot
5. Connector or tool requirements
6. Existing example files

# Knowledge / Reference Files

Use these when available before producing final outputs:
- brand-guidelines.md
- example.md
- example-visualizations.md
- example-prompts.md

If they do not exist, proceed with a best-effort structured output and explicitly state what is missing.

# Core Framing Questions

For the overall skill:
1. How and when should this skill be triggered?
2. What does this skill need to do?
3. What connectors or tools does it need?
4. What is the step-by-step process?

For each step:
1. Where does the user want HITL?
2. What reference file should be used?
3. What output format is needed?

# Procedure

## 1. Intake and Scope Definition
### 1.1 Confirm the user’s source content
Ask for the exact content, notes, article, or idea to be visualized.

### 1.2 Confirm destination
Ask where the infographic will be used.

### 1.3 Confirm output type
Ask whether the user wants:
- concept suggestions
- visualization options
- final prompt
- full workflow

### 1.4 Confirm brand context
Ask whether any brand guidelines or reference materials exist.

### 1.5 Confirm HITL points
Ask where the user wants approval gates:
- after concept generation
- after visualization directions
- before final prompt
- before image generation

## 2. Content Analysis
### 2.1 Extract the core message
Identify the main takeaway of the content.

### 2.2 Extract candidate visual ideas
Break the content into phrases, themes, concepts, steps, categories, or comparisons that could be visualized.

### 2.3 Select the strongest infographic candidates
Produce at least 5 possible infographic concepts.

### 2.4 Use available reference files
If `example.md` exists, use it before finalizing concept suggestions.

## 3. Concept Suggestion Output
### 3.1 Provide at least 5 concepts
Each concept must include:
- concept title
- what it visualizes
- why it works
- recommended infographic type

### 3.2 Do not give only one answer
Always provide multiple viable directions.

### 3.3 Require user selection
Wait for the user to choose one concept before proceeding unless they explicitly request autonomous continuation.

## 4. Visualization Direction Generation
### 4.1 Expand the chosen concept
Generate 5 different visualization approaches for the selected concept.

### 4.2 Use the proper reference file
If `example-visualizations.md` exists, use it before producing visualization options.

### 4.3 Each option must include
- layout type
- information hierarchy
- visual flow
- icon/graphic direction
- density level
- why it fits the content

### 4.4 Require user selection
Wait for the user to select one direction unless otherwise instructed.

## 5. Brand Alignment
### 5.1 Read brand guidance first
If `brand-guidelines.md` exists, use it before generating the final prompt.

### 5.2 Extract styling guidance
Identify:
- colors
- typography direction
- spacing
- visual tone
- icon style
- content density
- polish level

### 5.3 Apply brand consistency
The final output must reflect the available brand references.

## 6. Prompt Construction
### 6.1 Build the image-generation prompt
Construct a strong, explicit prompt for the chosen concept and selected visualization direction.

### 6.2 Use prompt examples
If `example-prompts.md` exists, use it before finalizing the output.

### 6.3 Include required prompt elements
- subject
- layout
- content hierarchy
- visual style
- audience/context
- platform constraints
- brand direction
- clarity instructions
- exclusions / things to avoid

### 6.4 Output formatting
Return:
- final title
- selected concept summary
- selected visualization direction
- final prompt
- optional negative prompt / exclusions
- notes for refinement

## 7. Approval and Iteration
### 7.1 Pause for approval
Before image generation, ask the user to approve the final prompt.

### 7.2 If rejected
Collect feedback, revise the prompt, and regenerate.

### 7.3 If approved
Proceed to the final output state requested by the user.

## 8. Failure Modes
### 8.1 Missing content
If the content is vague, ask for clarification or restructure the content first.

### 8.2 Missing reference files
Proceed with best effort and clearly label assumptions.

### 8.3 Weak concept quality
Generate more concepts instead of forcing a weak one.

### 8.4 Brand ambiguity
Do not fake brand precision; state what is assumed.

## 9. Progressive Updates
### 9.1 Update rules when repeated feedback appears
If the user repeatedly says “do not do X,” that instruction should be added to the Rules section in the next version.

### 9.2 Update when a new required file emerges
If the workflow repeatedly depends on a missing reference, add it to the required references in the next build.

### 9.3 Version bump trigger
Bump the skill whenever:
- the workflow changes materially
- new reference dependencies are added
- approval gates are changed
- output structure is upgraded

# Rules

- Never give only one concept when multiple options are appropriate.
- Always state when a reference file is being used.
- Never pretend a missing file was reviewed.
- Prefer structured outputs over loose prose.
- Ask for approval at the user-defined HITL gates.
- Keep the process modular and reusable.
- Optimize for clarity, not filler.

# Output Format

## A. Intake Summary
- content received
- platform
- desired output
- reference files found/missing
- HITL gates

## B. Concept Options
At least 5 concepts.

## C. Visualization Options
At least 5 options for the selected concept.

## D. Final Prompt Package
- chosen direction
- final prompt
- exclusions
- refinement notes

# Logging

Log:
- input summary
- files referenced
- selected concept
- selected visualization
- final prompt status
- revision notes

# Failure Modes

- Missing content: ask for the source content before generating concepts.
- Missing brand guidance: proceed with clearly labeled assumptions.
- Weak concept set: generate additional concepts instead of forcing a poor option.
- User rejects direction: collect feedback and return to visualization direction generation.
- Image prompt is too vague: add layout, hierarchy, style, platform, and exclusion details.

# Dependencies

- User-provided source content
- Optional brand guidance in `references/`
- Optional visual examples in `assets/`
- Image-generation tool only when the user requests actual image creation

# Assumptions

- The user wants an infographic workflow, not a generic design critique.
- Human approval gates are preferred unless the user requests autonomous continuation.
- Missing references should be disclosed rather than invented.

# Change Log

See CHANGELOG.md
