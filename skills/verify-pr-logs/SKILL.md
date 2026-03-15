---
name: verify-pr-logs
description: Checks GitHub Actions CI logs on a pull request, diagnoses failures,
  and guides the agent to implement fixes. Use when user mentions CI failing, check
  PR logs, fix pipeline, GitHub Actions errors, workflow failures, build broken, tests
  failing on PR, or debug CI. Focuses on PR-scoped CI analysis only.
---

# Verify PR Logs

You are helping the user diagnose and fix CI failures on a pull request by fetching
GitHub Actions logs, triaging the failure type, and implementing the appropriate fix.

Always use the `gh` CLI to interact with GitHub. Never ask the user to copy-paste logs.

## Step 1: Identify the Pull Request

Determine the PR to analyze:

1. **If the user provides a PR number**, use it directly
2. **Otherwise**, detect from the current branch:

   ```bash
   gh pr view --json number,title,url,headRefName
   ```

3. If no PR is found for the current branch, inform the user and ask for a PR number

Confirm the PR with the user before proceeding:

```text
PR #42: "Add new feature" (branch: feature/new-feature)
```

## Step 2: List Check Runs

Fetch the status of all checks on the PR:

```bash
gh pr checks <pr-number>
```

Present a summary table:

```text
| Check Name          | Status | Conclusion |
| ------------------- | ------ | ---------- |
| build               | pass   | success    |
| test                | fail   | failure    |
| lint                | fail   | failure    |
```

If all checks pass, inform the user and stop. Only proceed with failed checks.

## Step 3: Fetch Failed Logs

For each failed check, get the run ID and fetch **only the failed logs**:

```bash
gh run view <run-id> --log-failed
```

**Critical:** Always use `--log-failed` first. Never fetch full logs (`--log`) unless
`--log-failed` returns no output or the failure cannot be identified from the filtered
output. Full logs can be extremely large and flood the context window.

If `--log-failed` produces no useful output, fall back to:

```bash
gh run view <run-id> --log 2>&1 | tail -100
```

## Step 4: Triage the Failure Type

Categorize each failure to guide the diagnosis:

| Failure Type | Log Signals | Typical Fix Location |
| ------------------- | ----------------------------------------- | ------------------------------- |
| Lint / format | `eslint`, `prettier`, `flake8`, `rubocop` | Source files flagged in output |
| Test failure | `FAIL`, `AssertionError`, `expected/got` | Test file or implementation |
| Build / compile | `error TS`, `cannot find module`, `syntax` | Source files referenced |
| Type error | `type mismatch`, `incompatible types` | Source files referenced |
| Timeout | `exceeded`, `timed out`, `cancelled` | CI config or slow test |
| Permission / auth | `403`, `401`, `permission denied` | Workflow config or secrets |
| Dependency | `not found`, `resolve failed`, `404` | Lock file or package manifest |
| Flaky test | Passes locally, fails intermittently | Test isolation or timing issue |
| Workflow config | `Invalid workflow`, `syntax error` | `.github/workflows/*.yml` |

## Step 5: Diagnose the Root Cause

Parse the logs to find the actual error:

1. **Skip boilerplate** — ignore setup steps, dependency installation, and framework
   banners. Focus on lines after the actual command execution
2. **Find the first error** — the root cause is usually the first failure, not cascading
   errors that follow
3. **Trace to source** — identify the exact file and line number from the error output
4. **Check if it reproduces locally** — suggest running the failing command locally
   (e.g., `npm test`, `make lint`) to confirm the fix before pushing

### Distinguishing Code vs CI Issues

Not all failures should be fixed in the source code:

| Symptom | Likely a CI issue | Likely a code issue |
| -------------------------------- | ------------------------------------------ | ---------------------------------- |
| Works locally, fails in CI | Environment, secrets, or path differences | Rare — check for OS-specific code |
| Failed on unrelated step | Workflow config or infrastructure | Not a code issue |
| Same test fails intermittently | Flaky test or resource contention | Test isolation problem |
| New failure after workflow change | Workflow syntax or step configuration | Not a code issue |
| Failure matches code changes | Unlikely a CI issue | Check the diff for the root cause |

## Step 6: Implement the Fix

1. **Explain the diagnosis** to the user before making changes — describe what failed,
   why, and where the fix should go
2. **Fix in the correct location**:
   - Code errors → fix in source files
   - CI configuration errors → fix in `.github/workflows/` files
   - Dependency errors → update lock files or package manifests
   - Flaky tests → fix test isolation, do not simply retry
3. **Make minimal changes** — fix only what is broken, do not refactor surrounding code

**Important:** Even if the user says "just fix it", always explain the diagnosis first.
The user needs to understand what broke and why to approve the fix.

## Step 7: Re-verify

After implementing the fix:

1. **Run locally** if possible — execute the same command that failed in CI:

   ```bash
   # Example: if lint failed
   npm run lint

   # Example: if tests failed
   npm test
   ```

2. **Push the fix** and watch the CI run:

   ```bash
   gh run watch
   ```

3. **Report the result** — confirm whether the fix resolved the failure or if further
   investigation is needed

## Anti-patterns to Avoid

| Anti-pattern | Why it is wrong | Correct approach |
| ------------------------------------ | ----------------------------------------------- | ------------------------------------------- |
| Fetching full logs first | Floods context with thousands of lines | Always use `--log-failed` first |
| Blindly re-running failed jobs | Masks real issues, wastes CI minutes | Diagnose the root cause before re-running |
| Fixing CI issues in source code | Wrong location, does not address the real issue | Distinguish code vs CI issues |
| Skipping local reproduction | Fix may not work, wastes CI round-trips | Run the failing command locally first |
| Fixing without explaining | User cannot review or learn from the issue | Always explain diagnosis before fixing |
| Retrying flaky tests without fixing | Flakiness will recur and erode trust in CI | Fix the underlying isolation or timing issue |

## Important Guidelines

- **Use `--log-failed` first** — never fetch full logs unless the filtered output is insufficient
- **Diagnose before fixing** — always explain what failed and why before implementing changes
- **Fix in the right place** — distinguish between code issues and CI configuration issues
- **Reproduce locally** — run the failing command locally before pushing a fix
- **One failure at a time** — when multiple checks fail, address them independently and in order
- **Never blindly retry** — `gh run rerun` without understanding the failure wastes CI time and hides issues
