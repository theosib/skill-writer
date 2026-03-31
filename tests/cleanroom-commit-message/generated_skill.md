---
name: commit-message-writer
description: >-
  Generates structured commit messages from staged git changes following Conventional Commits standard. Summarizes staged diffs, determines commit type (feat, fix, docs, etc.), and produces properly formatted messages with scope and description. Triggered by "write a commit message", "commit my changes", or requests to describe staged changes.
disable-model-invocation: true
---

# Commit Message Writer

## Rules

1. Analyze `git diff --staged` output to determine what changed.
2. Identify the commit type: `feat` (new feature), `fix` (bug fix), `docs` (documentation), `refactor` (code restructuring), `test` (test additions/changes), or `chore` (build, dependencies, tooling).
3. Determine the scope by identifying the primary file, function, or module affected. Keep scope lowercase and hyphenated.
4. Write the short description in imperative mood (e.g., "add", "fix", "update"), under 72 characters, with no trailing period.
5. Short description must be specific. Reject vague phrases like "various improvements", "minor fixes", "update code".
6. If more than 3 files changed across unrelated concerns, flag that the changes may be better split into separate commits before generating the message.
7. If no changes are staged, notify the user and suggest running `git add` first.
8. Include an optional body if the change is non-trivial: explain what changed and why the change was made (not how, which code shows).
9. Include an optional footer if relevant: document breaking changes with `BREAKING CHANGE:` or link to issues with `Closes #N`.

## Process

1. Request `git diff --staged` from the user if not provided.
2. If no staged changes exist, return a message recommending `git add`.
3. Scan the diff to identify affected files and determine the primary change type.
4. Check file count and concern coherence; flag if split recommended.
5. Generate the commit type and scope.
6. Compose the short description (imperative, specific, under 72 chars).
7. Draft a body explaining the what and why if the change is non-trivial.
8. Add a footer if breaking changes or issue references apply.
9. Present the complete formatted message.

## Output Format

```
type(scope): short description

Optional body explaining what changed and why.

Optional footer:
Closes #123
BREAKING CHANGE: description of breaking change
```

Example:

```
feat(auth): add two-factor authentication flow

Implement TOTP-based 2FA for user accounts. Users can enable 2FA
in account settings and will be prompted for a code on next login.

Closes #456
```
