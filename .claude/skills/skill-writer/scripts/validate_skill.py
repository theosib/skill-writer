#!/usr/bin/env python3
"""
Skill Validation Script

Tests whether an LLM can correctly interpret and apply a SKILL.md file
by spawning a fresh agent with only the skill content and a test prompt.

Usage:
    python validate_skill.py <path-to-SKILL.md> [--test-prompt "prompt"] [--model haiku]
    python validate_skill.py <path-to-SKILL.md> --mode stress [--test-input "input"]
    python validate_skill.py <path-to-SKILL.md> --mode full

Modes:
    interpret (default): Tests whether the agent correctly understands the skill
    stress: Tests edge cases with specific inputs
    full: Runs interpretation test + generates and runs stress tests
"""

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile


def read_skill(path):
    """Read a SKILL.md file and return its content."""
    with open(path) as f:
        return f.read()


def extract_frontmatter(content):
    """Extract YAML frontmatter from skill content."""
    match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if match:
        fm = {}
        for line in match.group(1).split('\n'):
            if ':' in line:
                key, val = line.split(':', 1)
                fm[key.strip()] = val.strip()
        return fm
    return {}


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


def run_interpretation_test(skill_content, test_prompt, model="sonnet"):
    """Spawn a fresh agent to interpret and apply the skill."""
    prompt = f"""You are testing a skill file. You have received ONLY the skill instructions below.
Do NOT use any prior knowledge about this skill — interpret it purely from what is written.

<skill>
{skill_content}
</skill>

Complete these tasks in order:

TASK 1 — COMPREHENSION
Summarize in your own words:
a) What does this skill do? (one sentence)
b) When should it trigger? (list trigger conditions)
c) What are its key rules? (list each rule as a short phrase)

TASK 2 — APPLICATION
Apply this skill to the following input. Follow the skill's instructions exactly.

Input: {test_prompt}

TASK 3 — AMBIGUITY REPORT
List any instructions you found:
a) Ambiguous (could be interpreted multiple ways)
b) Contradictory (conflicts with another instruction)
c) Missing (you had to make assumptions to complete the task)
d) Redundant (says the same thing as another instruction)

If none, say "None found" for each category.

Format your response with clear headers for each task."""

    return claude_cli(prompt, model)


def run_stress_test(skill_content, test_input, description, model="sonnet"):
    """Run a specific stress test against the skill."""
    prompt = f"""You have received a skill file. Apply it to the input below.
Follow the skill's instructions exactly — do not improvise or add behaviors not specified.

<skill>
{skill_content}
</skill>

Input: {test_input}

Produce ONLY the output the skill specifies. No commentary."""

    output = claude_cli(prompt, model)
    return {
        "description": description,
        "input": test_input[:200] + ("..." if len(test_input) > 200 else ""),
        "output": output[:500] + ("..." if len(output) > 500 else ""),
        "output_length": len(output),
    }


def generate_stress_tests(skill_content, model="sonnet"):
    """Ask the model to generate edge-case test inputs for the skill."""
    prompt = f"""Analyze this skill file and generate 4 test inputs that stress-test its boundaries.

<skill>
{skill_content}
</skill>

Generate exactly 4 test cases as a JSON array. Each test case should have:
- "description": what this tests (e.g., "minimal input", "adversarial input")
- "input": the actual test input text
- "assertion": a concrete, verifiable property of the expected output

The 4 tests should be:
1. Minimal input — shortest valid input
2. Adversarial input — input that could trigger anti-pattern behaviors
3. Ambiguous input — input where correct action isn't obvious
4. Large/complex input — input near the practical limit

Output ONLY the JSON array, no other text."""

    result = claude_cli(prompt, model)
    # Try to extract JSON from the response
    try:
        # Handle markdown code blocks
        json_match = re.search(r'```(?:json)?\s*\n?(.*?)\n?```', result, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(1))
        return json.loads(result)
    except json.JSONDecodeError:
        print(f"  Warning: Could not parse stress test JSON. Raw output:")
        print(f"  {result[:500]}")
        return []


def analyze_interpretation(skill_content, agent_response, model="sonnet"):
    """Analyze the interpretation test results for quality issues."""
    prompt = f"""You are a skill quality auditor. Compare the original skill file against how a fresh agent interpreted and applied it.

<original_skill>
{skill_content}
</original_skill>

<agent_response>
{agent_response}
</agent_response>

Produce a structured assessment:

## Comprehension Score
Rate 1-5 how accurately the agent understood the skill.
List any rules it missed or misunderstood.

## Application Score
Rate 1-5 how correctly the agent applied the skill to the test input.
List any rules it violated or behaviors it invented.

## Ambiguity Issues
List instructions that caused interpretation problems, with suggested fixes.

## Contradiction Issues
List any contradictions found, with suggested resolutions.

## Gap Issues
List any assumptions the agent had to make, suggesting instructions to add.

## Overall Assessment
One paragraph: is this skill ready for use, or does it need revision?
List the top 3 improvements in priority order.

Output ONLY this assessment, no other text."""

    return claude_cli(prompt, model)


def main():
    parser = argparse.ArgumentParser(description="Validate a SKILL.md file")
    parser.add_argument("skill_path", help="Path to SKILL.md")
    parser.add_argument("--test-prompt", default=None,
                        help="Test prompt for interpretation test")
    parser.add_argument("--test-input", default=None,
                        help="Specific input for stress test")
    parser.add_argument("--model", default="sonnet",
                        help="Model to use (haiku, sonnet, opus)")
    parser.add_argument("--mode", choices=["interpret", "stress", "full"],
                        default="interpret",
                        help="Validation mode")
    parser.add_argument("--output", default=None,
                        help="Save results to JSON file")
    args = parser.parse_args()

    skill_content = read_skill(args.skill_path)
    fm = extract_frontmatter(skill_content)
    skill_name = fm.get("name", os.path.basename(os.path.dirname(args.skill_path)))

    print(f"{'=' * 70}")
    print(f"  Skill Validation: {skill_name}")
    print(f"  Model: {args.model}")
    print(f"  Mode: {args.mode}")
    print(f"{'=' * 70}")

    results = {"skill": skill_name, "model": args.model, "mode": args.mode}

    # Default test prompt if none provided
    test_prompt = args.test_prompt
    if not test_prompt and args.mode in ("interpret", "full"):
        test_prompt = f"Create a simple example that exercises the '{skill_name}' skill."

    # Phase 1: Interpretation test
    if args.mode in ("interpret", "full"):
        print(f"\n--- Interpretation Test ---")
        print(f"  Test prompt: {test_prompt[:80]}...")
        response = run_interpretation_test(skill_content, test_prompt, args.model)
        print(f"\n  Agent response ({len(response)} chars):")
        print(f"  {'─' * 60}")
        for line in response.split('\n'):
            print(f"  {line}")
        print(f"  {'─' * 60}")

        # Analyze the interpretation
        print(f"\n--- Quality Analysis ---")
        analysis = analyze_interpretation(skill_content, response, args.model)
        print(f"  {'─' * 60}")
        for line in analysis.split('\n'):
            print(f"  {line}")
        print(f"  {'─' * 60}")

        results["interpretation"] = {
            "test_prompt": test_prompt,
            "response": response,
            "analysis": analysis,
        }

    # Phase 2: Stress tests
    if args.mode in ("stress", "full"):
        print(f"\n--- Stress Tests ---")

        if args.test_input:
            # Single manual stress test
            tests = [{"description": "manual", "input": args.test_input, "assertion": "N/A"}]
        else:
            # Generate stress tests
            print(f"  Generating stress test cases...")
            tests = generate_stress_tests(skill_content, args.model)
            print(f"  Generated {len(tests)} test cases")

        stress_results = []
        for i, test in enumerate(tests):
            print(f"\n  Test {i+1}: {test.get('description', 'unknown')}")
            print(f"    Input: {str(test.get('input', ''))[:80]}...")
            print(f"    Assertion: {test.get('assertion', 'N/A')}")

            result = run_stress_test(
                skill_content,
                test.get("input", ""),
                test.get("description", f"test_{i+1}"),
                args.model,
            )
            result["assertion"] = test.get("assertion", "N/A")
            stress_results.append(result)

            print(f"    Output ({result['output_length']} chars): {result['output'][:100]}...")

        results["stress_tests"] = stress_results

    # Save results
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"\nResults saved to {args.output}")

    print(f"\n{'=' * 70}")
    print(f"  Validation complete")
    print(f"{'=' * 70}")


if __name__ == "__main__":
    main()
