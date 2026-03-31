# skill-writer

A Claude Code skill for writing high-quality, token-efficient LLM skills optimized for modern models (2025–2026).

## What this does

**skill-writer** guides you through creating Claude Code skills that are compact, unambiguous, and effective across current-generation LLMs (Claude 4.x, GPT-5.x, Gemini 3). It focuses on *instruction writing quality* — how to craft rules, examples, and structure that models follow reliably.

## How it relates to Anthropic's skill-creator

Anthropic publishes an official [skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator) that handles the **eval/benchmark loop**: write a skill, run it against test cases, score the outputs, iterate. It's excellent at measuring whether a skill *works*.

**skill-writer** is complementary — it handles the **writing quality** problem that comes before evaluation:

| | Anthropic skill-creator | skill-writer |
|---|---|---|
| **Focus** | Does the skill produce correct outputs? | Are the instructions clear, efficient, and portable? |
| **Method** | Eval framework with assertions and scoring | Interpretation testing — can a fresh agent understand the skill? |
| **Optimizes for** | Output correctness on benchmarks | Instruction clarity, token efficiency, cross-model portability |
| **Knowledge base** | Anthropic best practices | Synthesized from Anthropic, OpenAI, Google, Meta, Cohere, and academic research |
| **Model targeting** | Claude-specific | Cross-model (Claude 4.x, GPT-5.x, Gemini 3) |

You can use both together: skill-writer to *write* the skill well, then skill-creator to *evaluate* it systematically.

## What extra value skill-writer brings

### 1. Cross-provider best practices
The reference documents synthesize guidance from all major LLM providers' 2025–2026 documentation — not just Anthropic. This matters because skills may be adapted for use outside Claude Code (e.g., pasted into ChatGPT or Gemini system prompts), and because different providers have discovered different failure modes.

### 2. Modern model calibration
Prompting advice from 2023 (ALL-CAPS emphasis, chain-of-thought on reasoning models, emotional appeals) actively harms performance on current models. skill-writer includes an anti-patterns reference that flags outdated practices and explains *why* they fail now.

### 3. Token efficiency from research
Built on empirical compression research ([token-compact](https://github.com/theosib/token-compact)) measuring actual token costs of formatting choices. For example: numbered lists add +140% overhead vs bare words, JSON wrapping adds +93%, and abbreviating technical terms like `authentication` saves zero tokens because they're already single BPE tokens.

### 4. Interpretation testing
Instead of only checking "did the skill produce the right output," skill-writer tests "does a fresh agent correctly *understand* the skill." This catches ambiguities, contradictions, and gaps that output-based testing can miss — because a skill might produce correct output despite unclear instructions (the model fills in gaps from training data), then fail unpredictably on edge cases.

### 5. Cross-model portability guidance
Identifies Claude-specific behaviors (XML tag semantics, prefilled responses, thinking tags) that won't transfer to other models, and offers universal alternatives.

## Quick start

### Install
Copy the `.claude/skills/skill-writer/` directory into your project's `.claude/skills/` or `~/.claude/skills/` for global access.

### Use
```
# In Claude Code, just describe what you want:
> Create a skill that reviews Python code for security vulnerabilities

# Or invoke directly:
> /skill-writer "code review skill for Python security"
```

### Validate a skill
```bash
python .claude/skills/skill-writer/scripts/validate_skill.py path/to/SKILL.md --mode full
```

## Project structure

```
.claude/skills/skill-writer/
├── SKILL.md                          # Main skill (6-phase workflow)
├── references/
│   ├── best-practices.md             # Synthesized from all major LLM providers
│   └── anti-patterns.md              # Outdated practices that hurt modern models
└── scripts/
    └── validate_skill.py             # Automated interpretation + stress testing
```

## Part of the semantic-density project

skill-writer is part of a research project on LLM instruction efficiency:
- **[token-compact](https://github.com/theosib/token-compact)** — Compression rules for reducing token usage in system prompts
- **skill-writer** — Applying those insights to skill creation
- **human-compact** *(coming soon)* — A style guide for humans writing LLM-optimized text

## License

MIT
