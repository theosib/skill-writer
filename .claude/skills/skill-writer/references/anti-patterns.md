# Skill Anti-Patterns — What to Avoid in 2025–2026

Common mistakes in skill/prompt writing, organized by why they fail on modern LLMs.

## Outdated Prompting Habits

### Aggressive emphasis (ALL-CAPS, "CRITICAL", "YOU MUST")
**Why it's harmful now:** Claude 4.x and GPT-5.x are more responsive to system prompts than older models. Aggressive language causes over-compliance — the model focuses disproportionate attention on emphasized rules at the expense of others. Use calm, declarative sentences.
**Exception:** A single emphasized word per skill is acceptable for genuinely safety-critical constraints.

### Chain-of-thought prompts on reasoning models
**Why it's harmful now:** Models with built-in reasoning (o-series, Claude extended thinking) handle CoT internally. Adding "think step by step" can degrade performance by interfering with the model's own reasoning process. Only use explicit CoT on non-reasoning model tiers.

### Emotional appeals and bribes
"I'll tip $200 for a good answer" / "My career depends on this" — these never reliably worked and modern models are explicitly trained to ignore them. They waste tokens and look unprofessional.

### Prefilled assistant responses
Deprecated in Claude 4.6. Never existed on other platforms. Don't design skills that depend on starting the assistant's response.

## Structural Anti-Patterns

### Kitchen-sink skills (>500 lines)
Skills that try to cover every edge case in one file. Models lose track of rules buried in long documents. Split into a focused SKILL.md + reference files loaded on demand.

### Contradictory instructions
"Be concise" + "Explain your reasoning thoroughly" — GPT-5.x specifically wastes reasoning tokens trying to reconcile contradictions. Claude picks one arbitrarily. Resolve conflicts explicitly: "Be concise in the output; use internal thinking for thorough reasoning."

### Deep nesting (>3 levels)
```
## Section
### Subsection
#### Sub-subsection
##### Sub-sub-subsection
```
Models parse flat structures better. Flatten to 2 levels (H2 + H3) with bullets underneath.

### Numbered lists for unordered rules
If the order doesn't matter, use bullets. Numbered lists imply sequence, which models may follow literally even when the steps are independent.

### JSON for document/reference embedding
OpenAI's research shows JSON performs poorly for long-context document retrieval. Use markdown or XML for reference material.

## Content Anti-Patterns

### Negative-only instructions
"Don't use markdown. Don't add comments. Don't include type annotations." — This tells the model what to avoid but not what to produce. The model focuses attention on the forbidden behaviors. Instead: "Write plain prose. Code should be self-documenting. Use type inference."

### Explaining what the model already knows
"PostgreSQL is a relational database management system that..." — Modern models know this. You're spending tokens on content the model will discard. Only explain project-specific facts.
**Caveat for cross-model skills:** If a domain fact is critical to correct skill behavior, state it even if most models know it — some may not.

### Redundant examples
Providing 5 examples that all demonstrate the same pattern. Use 3–5 diverse examples covering different scenarios, including edge cases. If examples all look the same, you probably only need 1–2.

### Over-specifying implementation details
"Use a for loop to iterate over the array, then use an if statement to check each element..." — This is solving the problem for the model. State the goal and constraints; let the model choose implementation.

### Hypothetical future requirements
"In case we later need to support X, add a configuration flag for..." — Design for what the skill actually needs now. Speculative abstractions add complexity and tokens for scenarios that may never occur.

## Testing Anti-Patterns

### Testing only the happy path
If a skill handles code review, test it on good code, bad code, ambiguous code, and code in languages it hasn't seen. Edge cases reveal whether the skill's instructions are specific enough.

### Testing only with the model that wrote the skill
A skill written by Claude and tested only on Claude may rely on Claude-specific behaviors. Test on at least one other model tier to catch portability issues.

### Not testing on the original document
Before testing a skill on compressed/modified input, verify it produces correct results on the original unmodified input. If baseline fails, the skill has a fundamental problem.

### Grading by vibes
"That looks about right" is not a test. Define specific, verifiable assertions: "Output must contain X", "Output must NOT contain Y", "Output format must match Z."
