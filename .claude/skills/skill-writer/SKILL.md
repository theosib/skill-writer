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

Interview the user to establish:
1. **What does the skill do?** — one sentence, verb-first ("Generates...", "Transforms...", "Reviews...")
2. **When should it trigger?** — what user phrases or file patterns activate it
3. **What inputs does it need?** — arguments, file contents, context
4. **What does good output look like?** — format, length, structure, examples
5. **Any constraints?** — model tier, tool restrictions, side effects, security
6. **Cross-model?** — will this skill be used outside Claude Code (e.g., pasted into ChatGPT, Gemini)?

Keep the interview to ≤6 questions. Don't ask about things you can infer from the answers.

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

**Cross-model portability (if applicable):**
- Use markdown headers as primary structure (universal)
- Don't rely on XML tag semantics for instruction parsing (Claude-specific)
- State domain facts explicitly rather than assuming model knowledge
- Don't use prefilled responses (deprecated in Claude 4.6, never existed elsewhere)
- Don't add CoT instructions if targeting reasoning models (they handle this internally)

### Phase 3: Validate — Interpretation Test

After writing the skill, run an automated interpretation test. Spawn a subagent with a fresh context that receives ONLY the SKILL.md content and a test prompt. The subagent should:

1. Read the SKILL.md
2. Summarize in its own words: what this skill does, when it triggers, what rules it follows
3. Process a sample input using the skill's instructions
4. Report any instructions it found ambiguous or contradictory

**Evaluate the subagent's response:**
- Did it correctly identify the skill's purpose?
- Did it follow all rules without prompting?
- Did it miss any rules? (indicates the rule is unclear or buried)
- Did it invent behaviors not in the skill? (indicates gaps the model filled with assumptions)
- Did it flag any contradictions? (fix these — contradictions waste model reasoning)

Use the script `scripts/validate_skill.py` to automate this. It generates test prompts, spawns a subagent, and reports a structured assessment.

### Phase 4: Validate — Stress Tests

Generate edge-case inputs that test the skill's boundaries:

1. **Minimal input** — shortest valid input; does the skill handle it without crashing or producing empty output?
2. **Adversarial input** — input that could trigger anti-pattern behaviors the skill should prevent
3. **Ambiguous input** — input where the correct action isn't obvious; does the skill's decision logic resolve it?
4. **Large input** — input near the practical size limit; does the skill degrade gracefully?

For each test case, define an assertion: a specific, verifiable property of the expected output (not "looks good" — concrete: "output contains X", "output is ≤Y tokens", "output format matches Z").

### Phase 5: Iterate

Based on validation results:
- Fix ambiguities by making instructions more specific
- Remove rules the subagent ignored (they may be redundant or unclear)
- Add rules for behaviors the subagent invented (gaps in the instructions)
- Re-run interpretation test after changes to verify the fix

Stop when: the interpretation test subagent correctly identifies all rules and produces correct output on all test cases, OR the user is satisfied with the quality.

### Phase 6: Compress (Optional)

If the skill exceeds 300 lines or the user wants maximum token efficiency, apply compression:
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
- [ ] Interpretation test passed
- [ ] At least 2 stress-test assertions verified

## Output

Deliver the complete skill directory:
```
skill-name/
  SKILL.md              # Main skill file
  references/           # Optional: detailed docs loaded on demand
  scripts/              # Optional: executable tools
```

Report: skill name, description, line count, estimated token cost (SKILL.md body only), and validation results summary.
