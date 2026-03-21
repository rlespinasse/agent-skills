---
name: claude-code-usage-report
description: Generates a token usage and cost estimation report for Claude Code sessions.
  Analyzes local session JSONL files to report per-model token consumption, API-equivalent
  costs, and per-project breakdowns. Use when user mentions token usage, cost report,
  spending, usage report, session stats, or how much Claude Code costs. Supports filtering
  by date range, project, or plan type.
---

# Claude Code Usage Report

Analyze Claude Code token consumption and estimate costs from session JSONL files
stored locally in `~/.claude/projects/`.

## When to Use

- User wants to know how many tokens they have consumed
- User asks for a cost estimate of their Claude Code usage
- Comparing API pricing vs subscription plan value
- Analyzing usage patterns across projects or time periods

## Data Source

Session data is stored as JSONL files in `~/.claude/projects/<project-id>/`:

- **Main session files**: `<project-dir>/*.jsonl`
- **Subagent session files**: `<project-dir>/*/subagents/*.jsonl`

Each line is a JSON object. Token usage is at `message.usage`:

| Field | Description |
| --- | --- |
| `input_tokens` | Direct input tokens |
| `output_tokens` | Model output tokens |
| `cache_read_input_tokens` | Tokens read from prompt cache |
| `cache_creation_input_tokens` | Tokens written to prompt cache |

Model identification is at `message.model` (contains `opus`, `sonnet`, or `haiku`).
Timestamps are at `timestamp` (ISO 8601 format).

## Pricing Reference (per 1M tokens)

Pricing depends on the **model generation**. The `message.model` field in session
data contains the full model ID (e.g., `claude-opus-4-6`, `claude-opus-4-1-20250805`).
Match the model ID to the correct generation pricing.

### Current generation (4.5 / 4.6)

| Model | Input | Output | Cache Read | Cache Write (5m) |
| --- | --- | --- | --- | --- |
| Opus 4.6 / 4.5 | $5.00 | $25.00 | $0.50 | $6.25 |
| Sonnet 4.6 / 4.5 | $3.00 | $15.00 | $0.30 | $3.75 |
| Haiku 4.5 | $1.00 | $5.00 | $0.10 | $1.25 |

### Previous generation (4.0 / 4.1)

| Model | Input | Output | Cache Read | Cache Write (5m) |
| --- | --- | --- | --- | --- |
| Opus 4.1 / 4.0 | $15.00 | $75.00 | $1.50 | $18.75 |
| Sonnet 4.0 | $3.00 | $15.00 | $0.30 | $3.75 |

### Legacy (3.x)

| Model | Input | Output | Cache Read | Cache Write (5m) |
| --- | --- | --- | --- | --- |
| Haiku 3.5 | $0.80 | $4.00 | $0.08 | $1.00 |
| Haiku 3 | $0.25 | $1.25 | $0.03 | $0.30 |

#### Model ID to Generation Mapping

Use the model ID string to determine generation:

```python
def get_generation(model_id):
    if "4-6" in model_id or "4-5" in model_id:
        return "current"
    if "4-1" in model_id or "4-0" in model_id or "4-20" in model_id:
        return "previous"
    return "legacy"
```

**Important:** These prices may change. If the user provides updated pricing,
use their values instead. When in doubt, fetch the latest prices from
<https://docs.anthropic.com/en/docs/about-claude/pricing>.

## Subscription Plan Reference

| Plan | Monthly Cost |
| --- | --- |
| Max 5x | $100/month |
| Max 20x | $200/month |

## Report Process

### Step 1: Determine Scope

Parse the user's request to determine:

- **Date range**: "since Feb 18", "last month", "all time", "this week"
- **Project filter**: specific project, current project, or all projects
- **Plan context**: which plan the user is on (for savings comparison)

If the user does not specify a scope, ask them to clarify.
Default to "all projects" if only a date range is given.

### Step 2: Collect Data

Run a **single Python script** via Bash to scan all relevant JSONL files.
The script must:

1. Scan `~/.claude/projects/` subdirectories (or a specific one)
2. Parse each JSONL file line by line
3. Filter by date range if specified (compare `timestamp` against cutoff)
4. Classify model from `message.model` (opus/sonnet/haiku) **and generation**
   (4.6/4.5 vs 4.1/4.0 vs 3.x) to apply the correct pricing tier
5. Accumulate per-project, per-model token counts
6. Count main sessions and subagent sessions
7. Compute daily token/cost totals
8. Calculate API-equivalent costs using the pricing table

**Critical:** Do this in a single Bash/Python invocation, not multiple tool calls.

#### Dynamic Username Detection

Extract the username from project directory paths dynamically:

```python
import os
home = os.path.expanduser("~")
username = os.path.basename(home)
```

Use this to clean project names by stripping the
`-Users-<username>-git-` prefix and replacing `-` with `/`.

### Step 3: Present the Report

The report must include these sections in order.

#### Global Summary

```text
Active projects:      N
Sessions:             N main + N subagent
Total tokens:         N
API equivalent cost:  $X.XX
[Plan] actual cost:   $X.XX (N months x $X)
Savings vs API:       $X.XX (N%)
```

Include the plan comparison only if the user has specified their plan.

#### Model Breakdown (Global)

Table with columns: Model, Input, Output, Cache Read, Cache Create, Cost.
Show each model that has usage, plus a TOTAL row.

#### Cost Breakdown by Type (Global)

For each model show:
`input=$X | output=$X | cache_read=$X | cache_create=$X`

#### Daily Usage

Table with columns: Date, Tokens, API Cost.
One row per active day, plus a TOTAL row.

#### Per-Project Breakdown

Sorted by cost descending. For each project:

- Project name (cleaned: remove user path prefix, use `/` separators)
- Session count (main+subagent)
- Total tokens and API cost
- Per-model detail: `model in=N out=N cache_r=N cache_w=N $X.XX`

### Step 4: Save the Report

Save the full report to `~/claude-code-usage-report.txt` (overwrite if exists).
Inform the user of the file path.

### Step 5: Highlight Key Insights

After the full report, add a brief summary highlighting:

- Top 5 projects by cost
- Peak usage day
- ROI vs API pricing (if plan context is known)
- Any notable patterns (e.g., one project dominating usage)

## Display Guidelines

- Format large numbers with commas (e.g., `1,234,567`)
- Right-align numeric columns
- Use `$X.XX` format for costs
- Clean project names for readability (strip path prefixes)
- Sort projects by cost descending
- Show percentages for savings and cost distribution

## Edge Cases

- **Missing timestamps**: Skip messages without timestamps for filtered reports
- **Unknown models**: Group under "other" using Sonnet pricing as fallback
- **Empty sessions**: Skip projects with zero tokens in the filtered period
- **Old session cleanup**: Claude Code may prune old session files — mention
  this if the user asks about older periods and data seems incomplete
- **Multiple plans**: If the user switched plans during the period, ask for
  the switch date and compute each period separately

## Anti-patterns to Avoid

| Anti-pattern | Better alternative |
| --- | --- |
| Making per-file tool calls | Single Python script scans everything |
| Hardcoding plan prices | Use pricing table, accept user overrides |
| Ignoring subagent files | Always include `*/subagents/*.jsonl` |
| Showing raw directory names | Clean up to readable project names |
| Omitting cache tokens | Always show all four token types |
| Guessing the date range | Ask the user if ambiguous |
| Hardcoding username in cleanup | Detect dynamically from `$HOME` |
