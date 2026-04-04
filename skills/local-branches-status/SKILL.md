---
name: local-branches-status
description: Reports the status of all local git branches with remote sync state, main branch diff,
  worktree path, last activity date, and content description. Use when user mentions branch status,
  branch overview, local branches, branch report, or branch summary. Helps understand the state of
  all branches at a glance.
---

# Local Branches Status Report

You are helping the user get a comprehensive overview of all local git branches in their repository.
The report shows each branch's sync state, divergence from main, worktree usage, last activity,
and a brief description of what the branch contains.

## When to Use

- Before deciding which branches to clean up or delete
- When resuming work after time away from a project
- Before pushing or rebasing to understand the current state
- When onboarding to a repository with multiple active branches
- When reviewing worktree usage across branches

## Report Process

### Step 1: Gather Branch Data

Collect all branch information in a **single shell invocation** using the batch loop in Step 3.
Do not make N separate tool calls per branch — one loop gathers every column for every branch.

Data collected per branch:

- Remote sync state (ahead/behind upstream)
- Divergence from the main branch (ahead/behind)
- Worktree association (with path)
- Last activity date
- Unique commits (commits not on main)
- Whether this is the current branch (HEAD)

### Step 2: Determine the Main Branch

Identify the main branch automatically:

```bash
git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@'
```

If that fails, fall back to checking for `main` or `master`.

### Step 3: Batch Data Collection

Gather all per-branch data in a single shell loop rather than making separate tool calls
for each branch and column. This is critical for efficiency — one invocation collects everything:

```bash
main_branch=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@' || echo "main")
current_branch=$(git symbolic-ref --short HEAD 2>/dev/null || echo "")
worktree_list=$(git worktree list)

for branch in $(git for-each-ref --format='%(refname:short)' refs/heads/); do
  # Remote sync state
  upstream=$(git for-each-ref --format='%(upstream:short)' "refs/heads/$branch")
  if [ -n "$upstream" ] && git rev-parse --verify "refs/remotes/$upstream" &>/dev/null; then
    counts=$(git rev-list --left-right --count "$upstream...$branch" 2>/dev/null || echo "0 0")
  else
    upstream=""
    counts="no_upstream"
  fi

  # Main branch diff
  if [ "$branch" = "$main_branch" ]; then
    main_diff="—"
  else
    main_diff=$(git rev-list --left-right --count "$main_branch...$branch" 2>/dev/null || echo "0 0")
  fi

  # Last activity
  last_activity=$(git log -1 --format='%cr' "$branch" 2>/dev/null || echo "unknown")

  # Worktree path
  wt_path=$(echo "$worktree_list" | grep "\[$branch\]" | awk '{print $1}')

  # Unique commits summary
  unique=$(git log "$main_branch..$branch" --oneline 2>/dev/null)

  echo "BRANCH:$branch|UPSTREAM:$upstream|COUNTS:$counts|MAIN_DIFF:$main_diff|LAST:$last_activity|WT:$wt_path|CURRENT:$([ "$branch" = "$current_branch" ] && echo yes || echo no)"
  echo "COMMITS:$unique"
  echo "---"
done
```

### Step 4: Compute Display Values

Use the raw data from Step 3 to format each column:

#### Remote Sync State

| Condition | Display |
| --- | --- |
| No upstream configured | `no upstream` |
| 0 ahead, 0 behind | `synced` |
| N ahead, 0 behind | `+N ahead` |
| 0 ahead, N behind | `-N behind` |
| N ahead, M behind | `+N ahead, -M behind` |

If an upstream is configured, include the upstream name (e.g., `synced with origin/feature-x`).

#### Main Branch Diff

| Condition | Display |
| --- | --- |
| Current branch is main | `—` |
| 0 ahead, N behind | `0 ahead, -N behind` (fully merged, stale) |
| N ahead, 0 behind | `+N ahead` |
| N ahead, M behind | `+N ahead, -M behind` |

#### Worktree State

| Condition | Display |
| --- | --- |
| Branch checked out in main repo | `main repo` |
| Branch checked out in a worktree | worktree path (last 2 segments, e.g., `…/proj-feat-x`) |
| Branch not checked out anywhere | `no worktree` |

When a branch has a dedicated worktree, show the truncated path (last 2 path segments)
so users can navigate directly. For example, `/home/user/projects/proj-feat-x` becomes
`…/projects/proj-feat-x`.

#### Last Activity

Show the relative date of the most recent commit on the branch (e.g., `2 days ago`,
`3 weeks ago`). This helps users prioritize branches by recency, not just divergence counts.

#### Current Branch Marker

Mark the branch where HEAD currently points with `*` prefix or `(current)` suffix in the
Branch column, so the user knows which branch is checked out.

#### Content Description

Derive from the unique commits on the branch (commits not on main):

- Summarize the branch purpose in one short phrase based on commit messages
- Focus on the **intent** (what the branch achieves), not individual commits
- If no unique commits exist, note the branch as "fully merged" or "identical to main"

### Step 5: Present the Report

Present results in a **summary table**:

```markdown
| Branch | Remote | Main diff | Worktree | Last activity | Description |
| --- | --- | --- | --- | --- | --- |
```

### Step 6: Add Actionable Notes

After the table, add a **Notes** section highlighting:

- **Deletable branches**: branches with 0 unique commits (fully merged)
- **Stale branches**: 10+ commits behind main **and** no unique commits in the last 30 days
- **Unpushed branches**: branches with no upstream (remind to push or confirm local-only)
- **Diverged branches**: branches both ahead and behind their upstream (potential conflicts)

Only include notes that are relevant — skip empty categories.

## Example Output

```markdown
| Branch | Remote | Main diff | Worktree | Last activity | Description |
| --- | --- | --- | --- | --- | --- |
| **main** * | synced | — | main repo | 1 day ago | Current working branch |
| **feature/auth-oauth2** | synced with `origin/feature/auth-oauth2` | +3 ahead, -1 behind | …/wt/auth-oauth2 | 2 days ago | Add OAuth2 authentication flow with token refresh |
| **feature/api-pagination** | no upstream | +2 ahead, -5 behind | …/wt/api-pagination | 5 days ago | Implement cursor-based pagination on REST endpoints |
| **fix/memory-leak** | +1 ahead `origin/fix/memory-leak` | +1 ahead, -3 behind | no worktree | 1 week ago | Fix connection pool memory leak on idle timeout |
| **refactor/db-layer** | no upstream | +6 ahead, -12 behind | …/wt/db-layer | 3 weeks ago | Extract repository pattern from service layer |
| **docs/api-reference** | no upstream | +1 ahead, -2 behind | no worktree | 4 days ago | Update OpenAPI spec with new pagination parameters |
| **spike/grpc-migration** | no upstream | +8 ahead, -20 behind | …/wt/grpc-migration | 2 months ago | Prototype gRPC transport layer, very stale |
| **old/legacy-import** | no upstream | 0 ahead, -15 behind | no worktree | 3 months ago | Fully merged into main, can be deleted |

**Notes:**

- **old/legacy-import** has no unique commits — safe to delete
- **spike/grpc-migration** is stale (20 commits behind main, last activity 2 months ago) — likely obsolete
- **refactor/db-layer** is stale (12 commits behind main, last activity 3 weeks ago) — consider rebase or deletion
- **feature/api-pagination**, **refactor/db-layer**, **docs/api-reference** have no upstream — unpushed
```

## Edge Cases

- **Detached HEAD**: If a worktree is in detached HEAD state, note it but do not include it
  as a branch in the table
- **Orphan branches**: Branches with no common ancestor with main — note this in the description
  and skip the main diff column (it would be misleading)
- **Many branches**: If there are more than 20 branches, suggest filtering by activity
  (e.g., branches with commits in the last 30 days)
- **No remote**: If the repository has no remote configured, skip the Remote column entirely
- **Pruned upstream**: A branch may have an upstream configured in `.git/config` that no longer
  exists on the remote (e.g., after `git fetch --prune`). Always verify the upstream ref exists
  before using it — treat branches with stale upstream refs as having no upstream

## Anti-patterns to Avoid

| Anti-pattern | Why it is wrong | Better alternative |
| --- | --- | --- |
| Listing commits instead of summarizing | Too verbose, defeats the purpose of a summary | Summarize branch intent in one phrase |
| Showing only branch names | Not actionable without context | Include all six columns |
| Skipping stale branch warnings | User may not notice cleanup opportunities | Always flag deletable and stale branches |
| Running `git fetch` without asking | Modifies state, may be unwanted | Only suggest fetching if data seems stale |
| Guessing branch purpose from name | Branch names can be misleading | Always read the actual commits |
| Making N separate tool calls per branch | Slow and wasteful | Use the batch script to collect all data in one pass |

## Important Guidelines

- **Do not run `git fetch`** without user approval — report on local state only
- **Do not delete branches** — only suggest deletions in the notes
- **Summarize, do not list** — the description column should be a short phrase, not a commit log
- **Sort meaningfully** — put main first, then active branches, then stale/deletable ones last
- **Be concise** — the report should fit on one screen for typical repositories
- **Batch data collection** — always use a single shell loop, never make per-branch tool calls
