---
name: skill-writer
description: Write high-quality, token-efficient Claude Code skills optimized for modern LLMs (2025-2026). Use when creating a new skill, improving an existing skill's instruction quality, or optimizing a skill for cross-model portability and token efficiency. Also use when asked to write a SKILL.md, create a slash command, or build an agent skill.
argument-hint: "[description of desired skill or path to existing SKILL.md]"
---

# Skill Writer

Write Claude Code skills that are compact, unambiguous, and effective across modern LLM families (Claude 4.x, GPT-5.x, Gemini 3). This skill focuses on **instruction quality** — how to write rules, examples, and structure that models follow reliably — complementing eval/benchmark frameworks like Anthropic's skill-creator.

Read `references/best-practices.md` and `references/anti-patterns.md` in this skill's directory before writing. These contain synthesized guidance from all major LLM providers.

## Workflow

### Phase 1: Capture Intent

Establish what the skill does by answering these 6 questions:
1. **What does the skill do?** — one sentence, verb-first ("Generates...", "Transforms...", "Reviews...")
2. **When should it trigger?** — what user phrases or file patterns activate it
3. **What inputs does it need?** — arguments, file contents, context
4. **What does good output look like?** — format, length, structure, examples
5. **Any constraints?** — model tier, tool restrictions, side effects, security
6. **Cross-model?** — will this skill be used outside Claude Code (e.g., pasted into ChatGPT, Gemini)?

**Adaptive interviewing:** If the user provides comprehensive answers upfront (in their initial message or a prepared brief), skip to confirmation rather than asking each question sequentially. Only ask about gaps. If all 6 are covered, confirm your understanding in one message and move on.

### Phase 1.5: Research (when the skill encodes domain expertise)

Skip this phase for simple workflow skills (commit messages, code formatting). Use it when the skill needs to make Claude an expert in a specialized domain — hardware APIs, niche protocols, specific frameworks, etc.

**Decide whether research is needed:** If the user could write the skill from their own knowledge in one sitting, skip to Phase 2. If the skill needs to encode knowledge from forums, documentation, examples, and community wisdom, do research first.

**Auto-generate research tracks:** Based on Phase 1 answers, propose 3–6 research tracks covering the skill's knowledge areas. Common track patterns:
- Core patterns/examples for the domain
- Integration with adjacent systems (DMA, databases, build tools, etc.)
- Advanced techniques and community-discovered tricks
- Common pitfalls and debugging approaches
- Version/platform differences (if applicable)

Present the proposed tracks to the user for approval or modification before launching.

**Parallelize research and code exploration:** If the user provides example code paths or a project directory, launch code exploration agents in parallel with web research agents. Don't wait for research to finish before examining existing code.

**Research execution:**
1. Launch parallel subagents (one per track) to search the web, GitHub repos, forums, and documentation. Each subagent should:
   - Search for examples, patterns, and common solutions
   - Identify pitfalls, edge cases, and non-obvious behaviors
   - Collect community-discovered tricks and best practices
   - Note version/platform differences if applicable
2. Save research findings to files (e.g., `research/track-name.md`) before proceeding. These files become raw material for the skill's reference documents.
3. Ask the user to review findings and contribute their own examples or corrections.

**When web tools are unavailable:** If WebSearch/WebFetch are denied, the agent can still produce useful research from training data. Mark confidence levels clearly: "well-documented" vs "from training data, verify against current docs." The user should know which findings may be stale.

**Research quality criteria:**
- Each track should have at least 3 concrete examples with code/config
- Pitfalls should explain WHY they fail, not just WHAT fails
- Community tricks should be verified against official documentation where possible
- Note which findings are well-established vs experimental/untested

The research files are intermediate artifacts — they'll be distilled into the skill's `references/` directory during Phase 2.

### Phase 2: Write the Skill

Apply these principles (details in `references/best-practices.md`):

**Frontmatter:**
- `name`: lowercase-hyphenated, descriptive, ≤64 chars
- `description`: ≤250 chars visible in listing. Third person, front-load the use case, include trigger synonyms
- Add `disable-model-invocation: true` for skills with side effects (deploy, publish, send)
- Add `paths` globs if the skill is file-type-specific

**Body structure:**
```
# Skill Name (one line explaining core purpose)

## Rules
(Numbered if sequential, bulleted if independent)

## Process
(Numbered steps for the workflow)

## Output Format
(What the result looks like)
```

**Writing rules for each instruction:**
- One behavior per instruction — testable in isolation
- Positive framing: say what TO DO, not what to avoid
- Add WHY when the reason isn't obvious (helps models generalize to edge cases)
- Use calm, declarative sentences — no ALL-CAPS, "CRITICAL", or "YOU MUST"
- Be concrete enough that a human colleague could verify compliance

**Token efficiency:**
- Don't explain well-known technologies (models know PostgreSQL, REST, TypeScript)
- Keep novel/project-specific content at full detail
- Use telegraphic style in instructional text: drop articles, copulas where clarity is preserved
- Use cross-references ("see §Config") instead of restating content
- Target ≤300 lines for SKILL.md; move reference material to separate files

**Reference file naming:** Use descriptive, lowercase-hyphenated names matching the content domain: `pio-patterns.md`, `dma-guide.md`, `common-pitfalls.md`. Prefer specificity (`dma-guide.md`) over vagueness (`techniques.md`).

**Cross-model portability (if applicable):**
- Use markdown headers as primary structure (universal)
- Don't rely on XML tag semantics for instruction parsing (Claude-specific)
- State domain facts explicitly rather than assuming model knowledge
- Don't use prefilled responses (deprecated in Claude 4.6, never existed elsewhere)
- Don't add CoT instructions if targeting reasoning models (they handle this internally)

### Phase 3: Validate — Autonomous Test Loop

Run validation autonomously. Only involve the user if contradictions can't be resolved automatically.

**Interpretation test:** Spawn a subagent with a fresh context that receives ONLY the SKILL.md content and a test prompt. The subagent should:
1. Summarize in its own words: what this skill does, when it triggers, what rules it follows
2. Process a sample input using the skill's instructions
3. Report any instructions it found ambiguous or contradictory

**Evaluate and fix automatically:**
- Rules the subagent missed → make them more prominent or specific
- Behaviors the subagent invented → add instructions to fill the gap
- Contradictions flagged → resolve them (contradictions waste model reasoning)
- Re-run the interpretation test after fixes to verify

Use the script `scripts/validate_skill.py` to automate this.

**Stress tests:** Generate edge-case inputs:
1. **Minimal input** — shortest valid input
2. **Adversarial input** — input that could trigger anti-pattern behaviors
3. **Ambiguous input** — input where correct action isn't obvious
4. **Large input** — input near the practical size limit

For each test case, define a concrete assertion ("output contains X", "output is ≤Y tokens", "output format matches Z").

Run the full test → fix → re-test cycle autonomously. Report results to the user when done, including what was fixed.

### Phase 4: Compress (if needed)

Skip if SKILL.md is already ≤300 lines (common for well-structured skills with reference files).

If compression is needed:
- Move reference material to `references/` files
- Apply telegraphic English to instructional text
- Merge rules that cover related behaviors
- Remove examples that don't add information beyond the rules
- Target: ≤200 lines for the SKILL.md body while preserving all behavioral rules

If the `token-compact` skill is available, use it on the final SKILL.md and report token savings.

## Quality Checklist

Before delivering the skill, verify:
- [ ] Description front-loads the use case in ≤250 chars
- [ ] Every instruction is positive-framed (DO, not DON'T)
- [ ] Every instruction maps to one testable behavior
- [ ] No ALL-CAPS emphasis or aggressive language
- [ ] No explanations of well-known technologies
- [ ] Novel/project-specific content preserved at full detail
- [ ] WHY provided for non-obvious rules
- [ ] Cross-references used instead of repetition
- [ ] SKILL.md body ≤300 lines (or justified if longer)
- [ ] If research was done: findings distilled into `references/`, raw research saved separately
- [ ] Interpretation test passed (autonomous fix cycle completed)
- [ ] At least 2 stress-test assertions verified

## Output

Write the skill to the **project directory** (e.g., `.claude/skills/skill-name/` within the current working directory or a path the user specifies). Do NOT install directly to `~/.claude/skills/` unless the user explicitly asks.

```
skill-name/
  SKILL.md              # Main skill file
  references/           # Optional: detailed docs loaded on demand
  scripts/              # Optional: executable tools
```

After writing, report: skill name, description, line count, estimated token cost (SKILL.md body only), and validation results summary.

Then ask the user what they'd like to do next:
- Review and edit the files before installing
- Install to `~/.claude/skills/` for global access
- Install to a specific project's `.claude/skills/`
- Commit to a git repository
