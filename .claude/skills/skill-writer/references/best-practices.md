# Skill Writing Best Practices — Modern LLMs (2025–2026)

Synthesized from Anthropic, OpenAI, Google, Meta, and Cohere documentation plus academic research. Targets Claude 4.x, GPT-5.x, Gemini 3 — NOT older models.

## 1. Instruction Architecture

### Progressive disclosure
Skills load in three levels: (1) name+description at startup, (2) full SKILL.md on trigger, (3) referenced files on demand. Budget accordingly:
- Description: ≤250 chars, front-load the use case
- SKILL.md body: ≤500 lines (target ≤300 for most skills)
- Reference files: unlimited, loaded only when needed

### Structure for scannability
Use markdown headers (H2/H3) to create named sections the model can reference internally. Models navigate by landmarks, not line numbers. Flat bullet lists under clear headers outperform deep nesting or numbered step hierarchies.

### Placement matters
- **Claude**: put reference data/context first, instructions/queries last (up to 30% improvement)
- **GPT-5.x**: place critical rules at both start AND end of instruction block (models prioritize edges)
- **Gemini 3**: context first, then task instructions, then constraints/formatting last
- **Universal**: critical rules should never be buried in the middle of a long document

## 2. Writing Instructions for Modern Models

### Calibrate intensity
2025–2026 models (Claude 4.x, GPT-5.x, Gemini 3) follow instructions more literally and are more responsive to system prompts than predecessors. This means:
- Drop ALL-CAPS emphasis, "CRITICAL", "YOU MUST" — a clear declarative sentence is sufficient
- Remove "bribes" ("I'll tip you $200"), threats, or emotional appeals — these were never reliable and modern models don't need them
- Don't add chain-of-thought instructions to reasoning models (o-series, Claude with extended thinking) — they handle this internally; adding CoT can hurt performance

### Positive framing
State what TO DO, not what NOT to do. Negative instructions ("don't use markdown") paradoxically focus attention on the forbidden behavior. Instead: "Write in plain prose paragraphs."

### Explain WHY
Adding motivation helps models generalize to edge cases. Instead of "always use UTC timestamps", write "Use UTC timestamps — this system serves users across 12 time zones, and local times cause scheduling bugs." The WHY costs tokens but prevents entire classes of misapplication.

### Be concrete and verifiable
Bad: "Format code properly"
Good: "Use 2-space indentation, 80-char line limit, trailing commas in multiline collections"

A human colleague should be able to verify compliance from the instruction alone.

### One instruction, one behavior
Don't overload a single bullet with multiple requirements. Each instruction should map to one observable behavior that can be independently tested.

## 3. Token Efficiency

### What costs more tokens than you think
- Numbered lists: +140% overhead vs bare words
- Bulleted lists: +87% overhead vs bare words
- JSON wrapping: +93% overhead
- Markdown tables: high overhead for simple data
- Repeated explanations across sections

### What costs fewer tokens than you think
- Technical terms (`authentication`, `parameter`, `context`) — already single tokens; abbreviating saves nothing
- Section headers — cheap navigation landmarks
- Short cross-references ("see §Config above") vs restating content

### Compression principles (from semantic density research)
- Drop articles, pronouns, copulas in instructional text (telegraphic style)
- Use arrows (→) for flows, compact notation for lists
- Don't explain well-known technologies — models already know PostgreSQL, REST, TypeScript
- Keep novel/project-specific content at full detail — this can't be reconstructed from training data
- For skills >300 lines, triage sections by information density before compressing

## 4. Cross-Model Portability

### Universal practices (work across all current models)
- Markdown structure with H2/H3 headers
- Explicit output format specification with examples
- Few-shot examples (3–5) when output format matters
- Positive instruction framing
- Role assignment in the opening line

### Model-specific divergences to avoid relying on
- XML tags: Claude was trained on them and handles them natively; other models may not weight them as strongly. Use markdown headers as primary structure, XML for wrapping data payloads only.
- Prefilled responses: deprecated in Claude 4.6, never existed elsewhere. Don't design around them.
- `<thinking>` tags: Claude-specific. For cross-model, instruct explicit reasoning without model-specific tag syntax.
- Domain knowledge assumptions: different models have different training data. If a fact matters for the skill to work correctly, state it explicitly rather than assuming the model "knows" it.

### Testing portability
A skill designed for Claude should also produce reasonable results on GPT-5.x and Gemini 3. If it relies on Claude-specific behaviors (XML tag nesting, specific tool names), document those dependencies explicitly.

## 5. Description Writing

The description is the most token-constrained and highest-leverage text in the skill. It determines whether the skill triggers.

- Write in third person: "Generates unit tests..." not "I help you..." or "Use this to..."
- Front-load the primary use case in the first 50 characters
- Include natural trigger phrases users would say (synonyms, alternate phrasings)
- Cover both what it does AND when to use it
- Undertriggering is more common than overtriggering — be "pushy" with keyword coverage
- Max 250 chars are shown in the skill listing; full description up to 1024 chars

## 6. Examples in Skills

### When examples are essential
- Output format matters (structured data, specific layouts)
- The task has non-obvious edge cases
- The instruction is ambiguous without demonstration

### When examples waste tokens
- The task is straightforward (summarize, translate, explain)
- The model's default behavior already matches the desired behavior
- You're just restating the instructions in concrete form

### Example quality
- Diverse: cover the range of expected inputs, including edge cases
- Realistic: mirror actual use-case inputs, not toy examples
- Minimal: shortest example that demonstrates the point
- Wrap in `<example>` tags or fenced blocks to separate from instructions

## 7. Process Sections

For skills that define a multi-step workflow:
- Use numbered steps for sequential operations
- Use bullets for unordered collections of rules
- Keep steps at a consistent level of abstraction (don't mix "1. Read the file" with "2. Implement the entire feature")
- Include decision points: "If X, do Y; otherwise Z"
- End with output format specification

## Sources

- Anthropic: Prompting best practices, Context engineering for agents, Agent skills blog, Claude Code docs
- OpenAI: GPT-4.1/5.x/5.4 prompting guides, Custom GPT guidelines, Prompt caching/optimization
- Google: Gemini 3 prompting guide, Prompt design strategies
- Meta: Llama prompting guide
- Cohere: Crafting effective prompts
- Academic: "The Prompt Report" (Schulhoff et al., arXiv:2406.06608), "Systematic Survey of Prompt Engineering" (Sahoo et al., arXiv:2402.07927)
