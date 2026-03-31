#!/usr/bin/env python3
"""
Cleanroom Test: Commit Message Writer

Tests the skill-writer by:
1. Generating a skill from a scenario description (Phase A)
2. Applying the generated skill to a test input (Phase B)
3. Checking assertions against the output (Phase C)

Usage:
    python run_test.py [--model haiku] [--skip-generation]

    --skip-generation: Use the saved generated_skill.md instead of regenerating
"""

import argparse
import json
import os
import re
import subprocess
import sys


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_WRITER_DIR = os.path.join(SCRIPT_DIR, '..', '..', '.claude', 'skills', 'skill-writer')

TEST_DIFF = r'''diff --git a/src/api/routes/query.ts b/src/api/routes/query.ts
index abc1234..def5678 100644
--- a/src/api/routes/query.ts
+++ b/src/api/routes/query.ts
@@ -1,5 +1,7 @@
 import { Router } from 'express';
+import { rateLimit } from 'express-rate-limit';

+const limiter = rateLimit({ windowMs: 60 * 1000, max: 100, standardHeaders: true });
 const router = Router();

-router.get('/query', async (req, res) => {
+router.get('/query', limiter, async (req, res) => {
diff --git a/wrangler.toml b/wrangler.toml
index 111aaaa..222bbbb 100644
--- a/wrangler.toml
+++ b/wrangler.toml
@@ -10,3 +10,6 @@ compatibility_date = "2024-01-01"
 [vars]
 ENVIRONMENT = "production"
+
+[rate_limiting]
+max_requests_per_minute = 100'''


def claude_cli(prompt, model="sonnet"):
    """Run a prompt through the claude CLI."""
    env = os.environ.copy()
    env.pop('CLAUDECODE', None)
    result = subprocess.run(
        ["claude", "-p", "--model", model,
         "--no-session-persistence",
         "--output-format", "text"],
        input=prompt,
        capture_output=True,
        text=True,
        timeout=300,
        env=env,
    )
    if result.returncode != 0:
        raise RuntimeError(f"claude CLI failed: {result.stderr}")
    return result.stdout.strip()


def load_scenario():
    """Load the scenario description for Phase 1 answers."""
    with open(os.path.join(SCRIPT_DIR, 'scenario.md')) as f:
        return f.read()


def load_skill_writer_guide():
    """Load the skill-writer SKILL.md."""
    with open(os.path.join(SKILL_WRITER_DIR, 'SKILL.md')) as f:
        return f.read()


def phase_a_generate(model):
    """Generate a skill from the scenario using skill-writer guidance."""
    guide = load_skill_writer_guide()
    scenario = load_scenario()

    # Extract just the Phase 1 answers from the scenario
    phase1_match = re.search(
        r'### Phase 1 Answers.*?\n\n(.*?)(?=\n## )',
        scenario, re.DOTALL
    )
    phase1 = phase1_match.group(1) if phase1_match else ""

    prompt = f"""You are testing a skill-writing system. Follow the guide below to produce a complete SKILL.md file.

IMPORTANT: Skip Phase 1 (interview) — answers provided. Skip Phases 3-6 (validation). Focus on Phase 2 (writing).

## SKILL-WRITING GUIDE

{guide}

## SCENARIO (Phase 1 answers)

{phase1}

Produce ONLY the complete SKILL.md file content (frontmatter + body). No commentary."""

    return claude_cli(prompt, model)


def phase_b_apply(skill_content, model):
    """Apply the generated skill to the test diff."""
    prompt = f"""You are testing a skill. Follow the instructions exactly.

<skill>
{skill_content}
</skill>

Apply this skill to the following staged diff:

```diff
{TEST_DIFF}
```

Produce ONLY the commit message output. No commentary."""

    return claude_cli(prompt, model)


def phase_c_check(output):
    """Check assertions against the output."""
    # Strip markdown code fences if present
    clean = output.strip()
    if clean.startswith('```'):
        lines = clean.split('\n')
        # Remove first line (```...) and last line (```)
        lines = [l for l in lines if not l.strip().startswith('```')]
        clean = '\n'.join(lines).strip()

    first_line = clean.split('\n')[0]
    output = clean  # Use cleaned output for all checks

    assertions = [
        {
            "name": "Commit type is feat",
            "check": first_line.startswith("feat"),
        },
        {
            "name": "Scope references API or query",
            "check": bool(re.search(r'\((api|query|route|rate)', first_line, re.IGNORECASE)),
        },
        {
            "name": "Imperative mood (add, not added/adds)",
            "check": bool(re.search(r':\s*(add|implement|introduce|apply|enable)', first_line, re.IGNORECASE)),
        },
        {
            "name": "Short description under 72 chars",
            "check": len(first_line) <= 72,
        },
        {
            "name": "Mentions rate limit in description",
            "check": "rate limit" in first_line.lower() or "rate-limit" in first_line.lower(),
        },
        {
            "name": "No trailing period on short description",
            "check": not first_line.rstrip().endswith('.'),
        },
        {
            "name": "Has body content",
            "check": len(output.strip().split('\n')) > 2,
        },
        {
            "name": "Does NOT include Closes #N (no issue in diff)",
            "check": "closes #" not in output.lower(),
        },
        {
            "name": "Does NOT flag for splitting (2 related files)",
            "check": "split" not in output.lower(),
        },
    ]

    return assertions


def main():
    parser = argparse.ArgumentParser(description="Cleanroom test: commit-message-writer")
    parser.add_argument("--model", default="haiku", help="Model to use")
    parser.add_argument("--skip-generation", action="store_true",
                        help="Use saved generated_skill.md")
    parser.add_argument("--output", default=None, help="Save results to JSON")
    args = parser.parse_args()

    print(f"{'=' * 60}")
    print(f"  Cleanroom Test: Commit Message Writer")
    print(f"  Model: {args.model}")
    print(f"{'=' * 60}")

    # Phase A: Generate skill
    if args.skip_generation:
        print(f"\n--- Phase A: Loading saved skill ---")
        with open(os.path.join(SCRIPT_DIR, 'generated_skill.md')) as f:
            skill_content = f.read()
        print(f"  Loaded generated_skill.md ({len(skill_content)} chars)")
    else:
        print(f"\n--- Phase A: Generating skill from scenario ---")
        skill_content = phase_a_generate(args.model)
        print(f"  Generated skill ({len(skill_content)} chars)")
        # Save for future --skip-generation runs
        with open(os.path.join(SCRIPT_DIR, 'generated_skill.md'), 'w') as f:
            f.write(skill_content)
        print(f"  Saved to generated_skill.md")

    # Phase B: Apply skill
    print(f"\n--- Phase B: Applying skill to test diff ---")
    output = phase_b_apply(skill_content, args.model)
    print(f"  Output:")
    print(f"  {'─' * 50}")
    for line in output.split('\n'):
        print(f"  {line}")
    print(f"  {'─' * 50}")

    # Phase C: Check assertions
    print(f"\n--- Phase C: Checking assertions ---")
    assertions = phase_c_check(output)
    passed = 0
    failed = 0
    for a in assertions:
        status = "PASS" if a["check"] else "FAIL"
        if a["check"]:
            passed += 1
        else:
            failed += 1
        print(f"  [{status}] {a['name']}")

    print(f"\n  Result: {passed}/{len(assertions)} assertions passed")

    # Save results
    results = {
        "model": args.model,
        "skill_length": len(skill_content),
        "output": output,
        "assertions": [{"name": a["name"], "passed": a["check"]} for a in assertions],
        "passed": passed,
        "total": len(assertions),
    }

    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"  Results saved to {args.output}")

    print(f"\n{'=' * 60}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
