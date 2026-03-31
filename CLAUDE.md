# skill-writer

A Claude Code skill for writing high-quality, token-efficient skills optimized for modern LLMs (2025-2026).

## Project structure

- `.claude/skills/skill-writer/SKILL.md` — Main skill file
- `.claude/skills/skill-writer/references/best-practices.md` — Synthesized best practices from all major LLM providers
- `.claude/skills/skill-writer/references/anti-patterns.md` — Common mistakes and outdated practices
- `.claude/skills/skill-writer/scripts/validate_skill.py` — Automated interpretation and stress testing

## Development

The validation script uses the `claude` CLI to spawn fresh agents for testing. Run it with:

```
python .claude/skills/skill-writer/scripts/validate_skill.py <path-to-SKILL.md> --mode full
```

## Relationship to other projects

- **token-compact**: Compression rules applied during Phase 6 (optional compression)
- **Anthropic skill-creator**: Complementary — that handles eval/benchmark loops; this handles writing quality
