---
build_number: "001"
skill_id: "epcb.meta.prompt_optimizer"
name: "master-prompt-optimizer"
description: "Transform raw user input into a structured prompt with clear purpose, inputs, outputs, and constraints."
trigger_keywords: "prompt, optimize prompt, structure request, clarify output, rewrite instructions"
owner: "EPCB"
status: "template"
created_at: "YYYY-MM-DD"
last_updated: "YYYY-MM-DD"
---

# Objective

Transform rough or ambiguous user input into an AI-ready prompt that states the purpose, required context, desired output, constraints, and validation criteria.

# Trigger

Use this template when:

- A user has a rough prompt but wants a clearer AI instruction.
- A request needs structure before being handed to another model.
- The output format, constraints, or success criteria are ambiguous.

# Required Inputs

1. Raw user request or rough prompt
2. Intended recipient model or tool, when known
3. Desired output format, when known

# Outputs

1. Optimized prompt
2. Clarifying questions when required information is missing
3. Assumptions used during optimization

# Procedure

1. **Capture Input**
   1.1 Preserve the raw request.
   1.2 Identify unclear or missing information.

2. **Extract Intent**
   2.1 Identify the user's goal.
   2.2 Identify required inputs and context.
   2.3 Identify desired outputs.
   2.4 Identify constraints and non-goals.

3. **Structure Prompt**
   3.1 Add a purpose section.
   3.2 Add input/context requirements.
   3.3 Add output format requirements.
   3.4 Add rules, constraints, and validation criteria.

4. **Optimize**
   4.1 Remove ambiguity.
   4.2 Replace vague terms with concrete instructions.
   4.3 Add examples only when they reduce ambiguity.

5. **Output**
   5.1 Return the optimized prompt.
   5.2 Return assumptions and open questions separately.

# Failure Modes

- Missing goal: ask what the prompt should accomplish.
- Missing output format: ask for the expected format or propose one.
- Conflicting constraints: name the conflict and request resolution.

# Dependencies

- Raw user request
- Optional style, policy, or formatting requirements

# Assumptions

- The user wants a prompt, not direct task execution.
- The optimized prompt should preserve the user's intent while improving clarity.

# Change Log

Template refreshed to match current AISkills metadata and section conventions.
