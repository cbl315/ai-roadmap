# Git Workflow

## Commit Message Format

```
<type>: <description>

<optional body>
```

Types: feat, fix, refactor, docs, test, chore, perf, ci

Note: Attribution disabled globally via ~/.claude/settings.json.

## Pull Request Workflow

When creating PRs:
1. Analyze full commit history (not just latest commit)
2. Use `git diff [base-branch]...HEAD` to see all changes
3. Draft comprehensive PR summary
4. Include test plan with TODOs
5. Push with `-u` flag if new branch

## Branch Strategy (CRITICAL)

**Default: Create PR, do NOT push directly to main/master.**

- ALWAYS create a feature branch for new work
- Push to feature branch and open a PR
- Only merge to main when the feature is complete and reviewed
- ONLY push directly to main if the user explicitly requests it

```bash
# WRONG: direct push to main
git add . && git commit -m "feat: something" && git push origin main

# CORRECT: PR workflow
git checkout -b feat/my-feature
git add . && git commit -m "feat: something"
git push -u origin feat/my-feature
gh pr create --title "feat: something" --body "..."
# ... after review and completion ...
gh pr merge feat/my-feature
```

## Feature Implementation Workflow

1. **Plan First**
   - Use **planner** agent to create implementation plan
   - Identify dependencies and risks
   - Break down into phases

2. **TDD Approach**
   - Use **tdd-guide** agent
   - Write tests first (RED)
   - Implement to pass tests (GREEN)
   - Refactor (IMPROVE)
   - Verify 80%+ coverage

3. **Code Review**
   - Use **code-reviewer** agent immediately after writing code
   - Address CRITICAL and HIGH issues
   - Fix MEDIUM issues when possible

4. **Commit & Push**
   - Detailed commit messages
   - Follow conventional commits format
