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

## Pricing

All pricing data (model token costs and subscription plans) is stored in
[scripts/pricing.json](scripts/pricing.json) — the single source of truth
used by the script. The file includes an `updated` date field so the user
can see when prices were last verified.

If the user asks to update pricing:

1. Run `python3 <skill-path>/scripts/usage_report.py --update-pricing`
   to display the current `pricing.json` values and update the checked date
2. Fetch <https://docs.anthropic.com/en/docs/about-claude/pricing> using
   your web tools to get the latest prices
3. Compare fetched prices with `pricing.json` values
4. Edit `pricing.json` with any changed values

The report displays the pricing data date so the user knows how current
the prices are.

## Report Process

### Step 1: Determine Scope

Parse the user's request to determine:

- **Date range**: "since Feb 18", "last month", "all time", "this week"
- **Project filter**: specific project, current project, or all projects

If the user does not specify a scope, ask them to clarify.
Default to "all projects" if only a date range is given.

### Step 2: Collect Data

Run the bundled script at [scripts/usage_report.py](scripts/usage_report.py)
to scan and aggregate session data. Resolve the script path relative to
the skill installation directory.

```bash
python3 <skill-path>/scripts/usage_report.py \
  [--start-date YYYY-MM-DD] \
  [--end-date YYYY-MM-DD] \
  [--project PROJECT_NAME] \
  [--output PATH] \
  [--update-pricing]
```

| Argument | Description | Default |
| --- | --- | --- |
| `--start-date` | Include only data on or after this date | No filter |
| `--end-date` | Include only data on or before this date | No filter |
| `--project` | Project directory name or substring | All projects |
| `--output` | Report output file path | `~/claude-code-usage-report.txt` |
| `--update-pricing` | Fetch pricing page and guide update of `pricing.json` | — |

The script outputs the formatted report to stdout and saves it to the
output file. It uses only Python stdlib (no dependencies to install).

The report always includes a **Plan ROI Comparison** section showing
savings for all plans (Pro, Max 5x, Max 20x) against API-equivalent cost.

### Step 3: Present the Report

The script produces a formatted report with these sections:

1. **Global Summary** — active projects, session counts, total tokens,
   API equivalent cost
2. **Plan ROI Comparison** — savings for Pro, Max 5x, and Max 20x plans
3. **Model Breakdown** — per-model token counts and costs with a TOTAL row
4. **Cost Breakdown by Type** — input/output/cache cost split per model
5. **Daily Usage** — tokens and cost per active day
6. **Per-Project Breakdown** — sorted by cost descending with per-model detail

Present the script output to the user. The report is also saved
automatically to the `--output` path (default `~/claude-code-usage-report.txt`).
Inform the user of the saved file path.

### Step 4: Highlight Key Insights

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
| Generating a script from scratch | Use the bundled `scripts/usage_report.py` |
| Making per-file tool calls | The bundled script scans everything |
| Hardcoding prices in the skill | Prices live in `scripts/pricing.json` |
| Ignoring subagent files | Script includes `*/subagents/*.jsonl` |
| Showing raw directory names | Script cleans up to readable project names |
| Omitting cache tokens | Script shows all four token types |
| Guessing the date range | Ask the user if ambiguous |
