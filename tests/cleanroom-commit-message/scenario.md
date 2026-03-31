# Cleanroom Test: Commit Message Writer

Source: [FreeCodeCamp — How to Build Your Own Claude Code Skill](https://www.freecodecamp.org/news/how-to-build-your-own-claude-code-skill/)

## Scenario

A skill that generates structured commit messages from staged git changes following the Conventional Commits standard.

### Phase 1 Answers (provided to skill-writer)

1. **What does the skill do?** Generates structured commit messages from staged git changes, following the Conventional Commits standard.
2. **When should it trigger?** When user says "write a commit message", "commit my changes", "summarize my staged diff", "what should my commit say", or any request to describe staged changes for version control.
3. **What inputs does it need?** The output of `git diff --staged`. If nothing is staged, notify the user and suggest `git add`.
4. **What does good output look like?** Format: `type(scope): short description` followed by optional body (what changed and why) and optional footer (BREAKING CHANGE, Closes #N). Types: feat, fix, docs, refactor, test, chore. Short description in imperative mood, under 72 characters, no trailing period.
5. **Any constraints?** Generate the message immediately without asking clarifying questions first. If more than 3 files changed across unrelated concerns, flag that the changes may be better split into separate commits. Short description must be specific — no vague phrases like "various improvements".
6. **Cross-model?** Claude Code only for now.

## Test Input

A staged diff adding rate limiting to an API endpoint:

```diff
diff --git a/src/api/routes/query.ts b/src/api/routes/query.ts
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
+max_requests_per_minute = 100
```

## Assertions

1. Commit type is `feat`
2. Scope references the API or query component
3. Short description is in imperative mood ("add", not "added" or "adds")
4. Short description is under 72 characters
5. Short description is specific (mentions rate limiting)
6. No trailing period on the short description
7. Body explains what changed (rate limiting added) and why (not just how)
8. Does NOT include `Closes #N` (no issue referenced in diff)
9. Does NOT flag for splitting (only 2 files, related concern)
