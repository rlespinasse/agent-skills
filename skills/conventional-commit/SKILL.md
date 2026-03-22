---
name: conventional-commit
description: Guides committing staged (indexed) git files using the Conventional Commits specification
  and commit message best practices. Use when user mentions commit, git commit, conventional commit,
  commit message, staged files, or indexed files. Helps craft well-structured, meaningful commit messages.
---

# Commit Staged Files with Conventional Commits

You are helping the user commit their currently staged (indexed) git files using the
[Conventional Commits](https://www.conventionalcommits.org/) specification and commit message best practices.

## Pre-flight Checks

Before crafting a commit message, always:

1. **Run `git status`** to see what files are staged
2. **Run `git diff --cached`** to review the actual staged changes
3. **If nothing is staged**, inform the user and stop — do not create an empty commit

## Conventional Commit Format

```text
<type>[optional scope]: <subject>

[optional body]

[optional footer(s)]
```

### Types

| Type | When to use |
| ------------ | ----------------------------------------------------------- |
| `feat` | A new feature or capability |
| `fix` | A bug fix |
| `docs` | Documentation-only changes |
| `style` | Formatting, whitespace, semicolons — no logic change |
| `refactor` | Code restructuring without behavior change |
| `perf` | Performance improvement |
| `test` | Adding or updating tests |
| `build` | Build system or external dependency changes |
| `ci` | CI/CD configuration changes |
| `chore` | Maintenance tasks (deps update, tooling, config) |
| `revert` | Reverting a previous commit |

**Note**: Comment-only changes (adding, updating, or removing code comments) should use `style` or
`chore` — never `feat` or `fix`. Keep commit messages concise; do not describe individual comments.

### Scope

- Optional, but recommended when the change targets a specific module, component, or area
- Use lowercase, kebab-case: `feat(auth):`, `fix(api-client):`
- Keep consistent with the project's existing scope conventions
- **Check recent git log** (`git log --oneline -50` or more) for scope patterns already used in the project
- Also note whether the project actually uses conventional commits — if not, adapt to the project's style

### Subject Line Rules

- **Imperative mood**: "add feature" not "added feature" or "adds feature"
- **Lowercase first letter**: "add feature" not "Add feature"
- **No period at the end**
- **50 characters or less** — hard limit at 72
- **Complete the sentence**: "If applied, this commit will _\<subject\>_"

### Body Rules

- Separate from subject with a blank line
- Wrap at 72 characters
- Explain **what** and **why**, not **how** (the diff shows how)
- Use when the subject alone is not sufficient to understand the change
- Use bullet points for multiple related changes

### Footer Rules

- `BREAKING CHANGE: <description>` for breaking changes (triggers major version bump)
- `Refs: #123` or `Closes #456` for issue references
- `Co-authored-by: Name <email>` for co-authors
- `Signed-off-by: Name <email>` when the project requires a Developer Certificate of Origin (DCO)

## Decision Process

Follow this process to determine the commit message:

### Step 1: Analyze the Staged Changes

Read the diff carefully and identify:

- What files changed and their purpose
- Whether this is a single logical change or multiple unrelated changes
- The primary intent: new feature, bug fix, refactor, etc.

### Step 2: Check for Multiple Logical Changes

If the staged changes contain **multiple unrelated changes**:

- Inform the user: "The staged changes contain multiple unrelated changes.
  Consider splitting them into separate commits for a cleaner history."
- Classify changes into categories to suggest logical groupings:
  - **Tidying** — formatting, renaming, dead code removal (no behavior change)
  - **Infrastructure/build** — dependencies, tooling, configuration
  - **Feature implementation** — new capabilities
  - **Bug fixes** — correcting incorrect behavior
  - **Documentation** — docs-only changes
- Keep dependency manifests with their lock files (e.g., `package.json` + `package-lock.json`,
  `go.mod` + `go.sum`, `Cargo.toml` + `Cargo.lock`, `pyproject.toml` + lock files)
- Suggest a commit order that tells a clear story:
  1. Tidying/structural changes first (separate from behavior changes)
  2. Documentation before related code changes
  3. Infrastructure/build before features that depend on them
  4. Feature or fix commits last
- Let the user decide whether to proceed with a single commit or split

### Step 3: Determine the Type

- Ask yourself: "What is the **primary intent** of this change?"
- If a feature includes tests, the type is `feat` (not `test`)
- If a bug fix includes a refactor, the type is `fix` (not `refactor`)
- The type reflects the reason for the change, not every file touched
- **Exception — scope-inherent types**: When all changed files belong to a single domain that has
  its own type, use that type directly without a scope. For example, if a commit only touches CI/CD
  files (e.g., `.github/workflows/`), use `ci:` — not `fix(ci):` or `feat(ci):`. The same applies
  to `docs:` (only documentation files), `test:` (only test files), and `build:` (only build config).
  These types already convey the scope, so adding it as a parenthetical is redundant.

### Step 4: Determine the Scope

- Look at what area of the codebase is affected
- Check `git log --oneline -50` for existing scope conventions
- If the change touches multiple areas, either omit the scope or use the primary area

### Step 5: Write the Subject

- Describe the change concisely in imperative mood
- Focus on the user-facing or developer-facing impact
- Bad: `fix(api): fixed the bug in the login endpoint`
- Good: `fix(api): return 401 on expired token instead of 500`

### Step 6: Write the Body (if needed)

Add a body when:

- The subject does not fully explain the change
- There is important context (why this approach, what was considered)
- The change has side effects or non-obvious consequences
- There is a breaking change to document

### Step 7: Present and Confirm

- Present the complete commit message to the user
- Wait for approval before executing the commit
- If the user wants changes, adjust accordingly

## Commit Execution

When executing the commit:

- Use `git commit -m` with a HEREDOC for multi-line messages
- **Never** use `--no-verify` — respect pre-commit hooks
- **Never** use `--amend` unless the user explicitly requests it
- If a pre-commit hook fails, investigate and fix the issue, then create a new commit
- After committing, run `git status` to confirm success

### Single-line Commit

```bash
git commit -m "feat(auth): add JWT token refresh endpoint"
```

### Multi-line Commit

```bash
git commit -m "$(cat <<'EOF'
feat(auth): add JWT token refresh endpoint

Implement automatic token refresh when the access token expires.
The refresh endpoint validates the refresh token and issues a new
access token with a 15-minute expiry.

Closes #234
EOF
)"
```

## Examples

### Simple Feature

```text
feat: add dark mode toggle to settings page
```

### Bug Fix with Context

```text
fix(parser): handle empty input without panic

The YAML parser panicked on empty strings because it attempted
to access the first character without a length check. Now returns
an empty document instead.

Closes #89
```

### Breaking Change

```text
feat(api)!: require authentication for all endpoints

All API endpoints now require a valid Bearer token. Previously,
read-only endpoints were publicly accessible.

BREAKING CHANGE: unauthenticated requests to /api/* now return 401.
Clients must include an Authorization header with a valid token.

Refs: #156
```

### Documentation Update

```text
docs: add API rate limiting guide
```

### Refactor

```text
refactor(db): extract connection pooling into dedicated module

Move connection pool logic from the monolithic database module into
its own module to improve testability and separation of concerns.
No behavior change.
```

## Anti-patterns to Avoid

| Anti-pattern | Why it is wrong | Better alternative |
| ------------------------------------- | ------------------------------ | ---------------------------------------- |
| `fix: fix bug` | Says nothing useful | `fix(cart): prevent negative quantities` |
| `update code` | Not a conventional commit | `refactor(utils): simplify date parsing` |
| `feat: Added new feature and fixes` | Past tense, vague, mixed scope | Split into separate commits |
| `WIP` | Not meaningful in history | Use a descriptive message or `--fixup` |
| `misc changes` | Uninformative | Describe what actually changed |
| `fix: fix` | Redundant and meaningless | Describe the actual fix |
| Subject longer than 72 characters | Breaks tooling and readability | Keep it concise, use body for details |

## Important Guidelines

- **Always review the diff** before writing the commit message — do not guess
- **Never commit secrets** (.env, API keys, credentials) — warn the user if staged
- **Respect the project's conventions** — check recent history for patterns
- **One logical change per commit** — suggest splitting when appropriate
- **Ask before committing** — always present the message for approval first
