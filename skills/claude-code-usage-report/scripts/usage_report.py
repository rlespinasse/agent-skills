#!/usr/bin/env python3
"""Claude Code Usage Report Generator.

Scans ~/.claude/projects/ JSONL session files to produce a token usage
and cost estimation report with per-model, per-project, and daily breakdowns.

Pricing is loaded from pricing.json (next to this script). Use
--update-pricing to fetch the latest prices from Anthropic's docs.
"""

import argparse
import json
import os
import sys
from collections import defaultdict
from datetime import datetime
from glob import glob
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PRICING_FILE = SCRIPT_DIR / "pricing.json"
PRICING_URL = "https://docs.anthropic.com/en/docs/about-claude/pricing"

# ---------------------------------------------------------------------------
# Pricing loader
# ---------------------------------------------------------------------------

def load_pricing():
    """Load pricing from pricing.json."""
    try:
        with open(PRICING_FILE) as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        print(f"Error: cannot load {PRICING_FILE}: {e}", file=sys.stderr)
        sys.exit(1)

    pricing = {}
    for key, vals in data.get("models", {}).items():
        family, gen = key.split(":", 1)
        pricing[(family, gen)] = {
            "input": vals["input"],
            "output": vals["output"],
            "cache_read": vals["cache_read"],
            "cache_write": vals["cache_write"],
        }

    plans = [
        (p["name"], p["monthly"])
        for p in data.get("plans", [])
    ]

    fallback = pricing.get(("sonnet", "current"), {
        "input": 3.00, "output": 15.00,
        "cache_read": 0.30, "cache_write": 3.75,
    })

    return pricing, plans, fallback, data.get("updated", "unknown")


PRICING, PLAN_COSTS, FALLBACK_PRICING, PRICING_DATE = load_pricing()


# ---------------------------------------------------------------------------
# Pricing updater
# ---------------------------------------------------------------------------

def show_current_pricing():
    """Display current pricing.json values for review and update the checked date."""
    try:
        with open(PRICING_FILE) as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError):
        data = {"source": PRICING_URL, "models": {}, "plans": []}

    print("Current pricing.json values (per 1M tokens):", file=sys.stderr)
    print("-" * 60, file=sys.stderr)
    for key, vals in data.get("models", {}).items():
        label = vals.get("label", key)
        print(
            f"  {label:<20} input=${vals['input']:<8} output=${vals['output']:<8} "
            f"cache_read=${vals['cache_read']:<8} cache_write=${vals['cache_write']}",
            file=sys.stderr,
        )
    print("", file=sys.stderr)
    print("Subscription plans:", file=sys.stderr)
    for plan in data.get("plans", []):
        print(f"  {plan['name']:<12} ${plan['monthly']}/month", file=sys.stderr)
    print("", file=sys.stderr)
    print(f"Last updated: {data.get('updated', 'unknown')}", file=sys.stderr)
    print(f"Source: {PRICING_URL}", file=sys.stderr)
    print("", file=sys.stderr)
    print(f"To update: compare with the pricing page above, then", file=sys.stderr)
    print(f"edit {PRICING_FILE} with any changed values.", file=sys.stderr)

    # Update the checked timestamp
    data["updated"] = datetime.now().strftime("%Y-%m-%d")
    data["source"] = PRICING_URL

    with open(PRICING_FILE, "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")

    print("", file=sys.stderr)
    print(f"Checked date updated in {PRICING_FILE}", file=sys.stderr)


# ---------------------------------------------------------------------------
# Model classification
# ---------------------------------------------------------------------------

def get_model_family(model_id: str) -> str:
    """Classify model ID into opus/sonnet/haiku."""
    model_lower = model_id.lower()
    if "opus" in model_lower:
        return "opus"
    if "haiku" in model_lower:
        return "haiku"
    if "sonnet" in model_lower:
        return "sonnet"
    return "other"


def get_generation(model_id: str) -> str:
    """Classify model ID into current/previous/legacy generation."""
    if "4-6" in model_id or "4-5" in model_id:
        return "current"
    if "4-1" in model_id or "4-0" in model_id or "4-20" in model_id:
        return "previous"
    if "3-5" in model_id:
        return "legacy"
    if "3" in model_id and "haiku" in model_id.lower():
        return "legacy-3"
    return "current"  # default to current for unknown


def get_pricing(model_id: str) -> dict:
    """Get pricing dict for a model ID."""
    family = get_model_family(model_id)
    generation = get_generation(model_id)
    return PRICING.get((family, generation), FALLBACK_PRICING)


def model_display_name(model_id: str) -> str:
    """Create a readable display name from model ID."""
    family = get_model_family(model_id)
    generation = get_generation(model_id)
    gen_label = {
        "current": "4.5/4.6",
        "previous": "4.0/4.1",
        "legacy": "3.5",
        "legacy-3": "3",
    }.get(generation, generation)
    return f"{family.capitalize()} ({gen_label})"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def clean_project_name(project_dir: str) -> str:
    """Clean project directory name into readable form."""
    name = os.path.basename(project_dir)
    home = os.path.expanduser("~")
    username = os.path.basename(home)
    prefix = f"-Users-{username}-"
    if name.startswith(prefix):
        name = name[len(prefix):]
    # Replace leading path separators encoded as dashes
    parts = name.split("-")
    return "/".join(parts)


def parse_timestamp(ts: str) -> datetime | None:
    """Parse ISO 8601 timestamp string."""
    if not ts:
        return None
    try:
        ts = ts.replace("Z", "+00:00")
        return datetime.fromisoformat(ts)
    except (ValueError, TypeError):
        return None


# ---------------------------------------------------------------------------
# Data collection
# ---------------------------------------------------------------------------

def scan_jsonl_files(base_path: str, project_filter: str | None = None):
    """Find all JSONL session files."""
    if project_filter:
        search_path = os.path.join(base_path, project_filter)
        if not os.path.isdir(search_path):
            matches = [
                d for d in glob(os.path.join(base_path, "*"))
                if os.path.isdir(d) and project_filter in os.path.basename(d)
            ]
            if matches:
                search_path = matches[0]
            else:
                print(f"Error: project '{project_filter}' not found", file=sys.stderr)
                sys.exit(1)
        dirs = [search_path]
    else:
        dirs = [
            d for d in glob(os.path.join(base_path, "*"))
            if os.path.isdir(d)
        ]

    files = []
    for d in dirs:
        for f in glob(os.path.join(d, "*.jsonl")):
            files.append((f, d, "main"))
        for f in glob(os.path.join(d, "*", "subagents", "*.jsonl")):
            files.append((f, d, "subagent"))
    return files


def process_files(files, start_date=None, end_date=None):
    """Process JSONL files and accumulate stats."""
    projects = defaultdict(lambda: {
        "models": defaultdict(lambda: {
            "input": 0, "output": 0, "cache_read": 0, "cache_write": 0,
        }),
        "main_sessions": set(),
        "subagent_sessions": set(),
    })
    daily = defaultdict(lambda: {"tokens": 0, "cost": 0.0})
    global_models = defaultdict(lambda: {
        "input": 0, "output": 0, "cache_read": 0, "cache_write": 0,
    })

    for filepath, project_dir, session_type in files:
        session_id = os.path.basename(filepath)
        has_tokens = False

        try:
            with open(filepath, "r", errors="replace") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        entry = json.loads(line)
                    except json.JSONDecodeError:
                        continue

                    ts_str = entry.get("timestamp", "")
                    ts = parse_timestamp(ts_str)
                    if ts:
                        if start_date and ts.date() < start_date:
                            continue
                        if end_date and ts.date() > end_date:
                            continue

                    msg = entry.get("message", {})
                    if not isinstance(msg, dict):
                        continue
                    usage = msg.get("usage", {})
                    if not usage:
                        continue

                    model_id = msg.get("model", "unknown")
                    inp = usage.get("input_tokens", 0)
                    out = usage.get("output_tokens", 0)
                    cache_r = usage.get("cache_read_input_tokens", 0)
                    cache_w = usage.get("cache_creation_input_tokens", 0)

                    if inp + out + cache_r + cache_w == 0:
                        continue

                    has_tokens = True
                    display = model_display_name(model_id)

                    proj = projects[project_dir]
                    proj["models"][display]["input"] += inp
                    proj["models"][display]["output"] += out
                    proj["models"][display]["cache_read"] += cache_r
                    proj["models"][display]["cache_write"] += cache_w

                    global_models[display]["input"] += inp
                    global_models[display]["output"] += out
                    global_models[display]["cache_read"] += cache_r
                    global_models[display]["cache_write"] += cache_w

                    pricing = get_pricing(model_id)
                    tokens = inp + out + cache_r + cache_w
                    cost = (
                        inp * pricing["input"]
                        + out * pricing["output"]
                        + cache_r * pricing["cache_read"]
                        + cache_w * pricing["cache_write"]
                    ) / 1_000_000

                    if ts:
                        day = ts.date().isoformat()
                        daily[day]["tokens"] += tokens
                        daily[day]["cost"] += cost

        except OSError:
            continue

        if has_tokens:
            proj = projects[project_dir]
            if session_type == "main":
                proj["main_sessions"].add(session_id)
            else:
                proj["subagent_sessions"].add(session_id)

    return projects, daily, global_models


# ---------------------------------------------------------------------------
# Cost computation
# ---------------------------------------------------------------------------

def compute_model_cost(model_display: str, stats: dict) -> float:
    """Compute cost for a model's token stats using display name to infer pricing."""
    pricing_key = _resolve_pricing_key(model_display)
    pricing = PRICING.get(pricing_key, FALLBACK_PRICING)
    return (
        stats["input"] * pricing["input"]
        + stats["output"] * pricing["output"]
        + stats["cache_read"] * pricing["cache_read"]
        + stats["cache_write"] * pricing["cache_write"]
    ) / 1_000_000


def _resolve_pricing_key(display_name: str):
    """Resolve display name to pricing dict key."""
    dl = display_name.lower()
    if "opus" in dl:
        family = "opus"
    elif "haiku" in dl:
        family = "haiku"
    else:
        family = "sonnet"

    if "4.5/4.6" in display_name:
        gen = "current"
    elif "4.0/4.1" in display_name:
        gen = "previous"
    elif "3.5" in display_name:
        gen = "legacy"
    elif "(3)" in display_name:
        gen = "legacy-3"
    else:
        gen = "current"
    return (family, gen)


# ---------------------------------------------------------------------------
# Formatting
# ---------------------------------------------------------------------------

def fmt_num(n: int) -> str:
    """Format number with commas."""
    return f"{n:,}"


def fmt_cost(c: float) -> str:
    """Format cost as $X.XX."""
    return f"${c:,.2f}"


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

def generate_report(projects, daily, global_models):
    """Generate the formatted report string."""
    lines = []

    # --- Global Summary ---
    total_projects = len(projects)
    total_main = sum(len(p["main_sessions"]) for p in projects.values())
    total_sub = sum(len(p["subagent_sessions"]) for p in projects.values())
    total_tokens = sum(
        s["input"] + s["output"] + s["cache_read"] + s["cache_write"]
        for m in global_models.values()
        for s in [m]
    )
    total_cost = sum(
        compute_model_cost(name, stats)
        for name, stats in global_models.items()
    )

    if daily:
        dates = sorted(daily.keys())
        first = datetime.fromisoformat(dates[0]).date()
        last = datetime.fromisoformat(dates[-1]).date()
        months = max(1, ((last.year - first.year) * 12 + last.month - first.month) + 1)
    else:
        months = 1

    lines.append("=" * 70)
    lines.append("CLAUDE CODE USAGE REPORT")
    lines.append("=" * 70)
    lines.append("")
    lines.append(f"Active projects:      {total_projects}")
    lines.append(f"Sessions:             {fmt_num(total_main)} main + {fmt_num(total_sub)} subagent")
    lines.append(f"Total tokens:         {fmt_num(total_tokens)}")
    lines.append(f"API equivalent cost:  {fmt_cost(total_cost)}")
    lines.append(f"Pricing data:         {PRICING_DATE}")
    lines.append("")

    # --- Plan ROI Comparison ---
    lines.append("-" * 70)
    lines.append("PLAN ROI COMPARISON")
    lines.append("-" * 70)
    lines.append("")
    plan_header = f"{'Plan':<12} {'Monthly':>10} {'Period Cost':>14} {'Savings':>14} {'ROI':>8}"
    lines.append(plan_header)
    lines.append("-" * len(plan_header))
    for plan_name, monthly in PLAN_COSTS:
        plan_cost = months * monthly
        savings = total_cost - plan_cost
        pct = (savings / total_cost * 100) if total_cost > 0 else 0
        roi_str = f"{pct:.0f}%" if savings > 0 else "n/a"
        lines.append(
            f"{plan_name:<12} {fmt_cost(monthly):>10} {fmt_cost(plan_cost):>14} "
            f"{fmt_cost(savings):>14} {roi_str:>8}"
        )
    lines.append("")
    lines.append(f"  Period: {months} month(s) | API equivalent: {fmt_cost(total_cost)}")
    lines.append("")

    # --- Model Breakdown ---
    lines.append("-" * 70)
    lines.append("MODEL BREAKDOWN")
    lines.append("-" * 70)
    lines.append("")
    header = f"{'Model':<22} {'Input':>14} {'Output':>14} {'Cache Read':>14} {'Cache Create':>14} {'Cost':>12}"
    lines.append(header)
    lines.append("-" * len(header))

    for name in sorted(global_models.keys()):
        stats = global_models[name]
        cost = compute_model_cost(name, stats)
        lines.append(
            f"{name:<22} {fmt_num(stats['input']):>14} {fmt_num(stats['output']):>14} "
            f"{fmt_num(stats['cache_read']):>14} {fmt_num(stats['cache_write']):>14} {fmt_cost(cost):>12}"
        )

    lines.append("-" * len(header))
    total_stats = {
        k: sum(m[k] for m in global_models.values())
        for k in ("input", "output", "cache_read", "cache_write")
    }
    lines.append(
        f"{'TOTAL':<22} {fmt_num(total_stats['input']):>14} {fmt_num(total_stats['output']):>14} "
        f"{fmt_num(total_stats['cache_read']):>14} {fmt_num(total_stats['cache_write']):>14} {fmt_cost(total_cost):>12}"
    )
    lines.append("")

    # --- Cost Breakdown by Type ---
    lines.append("-" * 70)
    lines.append("COST BREAKDOWN BY TYPE")
    lines.append("-" * 70)
    lines.append("")
    for name in sorted(global_models.keys()):
        stats = global_models[name]
        pricing_key = _resolve_pricing_key(name)
        pricing = PRICING.get(pricing_key, FALLBACK_PRICING)
        ic = stats["input"] * pricing["input"] / 1_000_000
        oc = stats["output"] * pricing["output"] / 1_000_000
        rc = stats["cache_read"] * pricing["cache_read"] / 1_000_000
        wc = stats["cache_write"] * pricing["cache_write"] / 1_000_000
        lines.append(
            f"{name}: input={fmt_cost(ic)} | output={fmt_cost(oc)} | "
            f"cache_read={fmt_cost(rc)} | cache_create={fmt_cost(wc)}"
        )
    lines.append("")

    # --- Daily Usage ---
    lines.append("-" * 70)
    lines.append("DAILY USAGE")
    lines.append("-" * 70)
    lines.append("")
    day_header = f"{'Date':<14} {'Tokens':>16} {'API Cost':>12}"
    lines.append(day_header)
    lines.append("-" * len(day_header))
    day_total_tokens = 0
    day_total_cost = 0.0
    for day in sorted(daily.keys()):
        d = daily[day]
        day_total_tokens += d["tokens"]
        day_total_cost += d["cost"]
        lines.append(f"{day:<14} {fmt_num(d['tokens']):>16} {fmt_cost(d['cost']):>12}")
    lines.append("-" * len(day_header))
    lines.append(f"{'TOTAL':<14} {fmt_num(day_total_tokens):>16} {fmt_cost(day_total_cost):>12}")
    lines.append("")

    # --- Per-Project Breakdown ---
    lines.append("-" * 70)
    lines.append("PER-PROJECT BREAKDOWN")
    lines.append("-" * 70)
    lines.append("")

    project_costs = []
    for proj_dir, proj_data in projects.items():
        proj_cost = sum(
            compute_model_cost(name, stats)
            for name, stats in proj_data["models"].items()
        )
        proj_tokens = sum(
            s["input"] + s["output"] + s["cache_read"] + s["cache_write"]
            for s in proj_data["models"].values()
        )
        project_costs.append((proj_dir, proj_data, proj_cost, proj_tokens))

    project_costs.sort(key=lambda x: x[2], reverse=True)

    for proj_dir, proj_data, proj_cost, proj_tokens in project_costs:
        name = clean_project_name(proj_dir)
        main_count = len(proj_data["main_sessions"])
        sub_count = len(proj_data["subagent_sessions"])
        lines.append(f"  {name}")
        lines.append(f"    Sessions: {main_count} main + {sub_count} subagent")
        lines.append(f"    Tokens: {fmt_num(proj_tokens)}  Cost: {fmt_cost(proj_cost)}")
        for model_name in sorted(proj_data["models"].keys()):
            ms = proj_data["models"][model_name]
            mc = compute_model_cost(model_name, ms)
            lines.append(
                f"      {model_name} in={fmt_num(ms['input'])} out={fmt_num(ms['output'])} "
                f"cache_r={fmt_num(ms['cache_read'])} cache_w={fmt_num(ms['cache_write'])} {fmt_cost(mc)}"
            )
        lines.append("")

    lines.append("=" * 70)
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Generate Claude Code token usage and cost report"
    )
    parser.add_argument(
        "--start-date",
        help="Start date filter (YYYY-MM-DD)",
    )
    parser.add_argument(
        "--end-date",
        help="End date filter (YYYY-MM-DD)",
    )
    parser.add_argument(
        "--project",
        help="Project directory name or substring to filter",
    )
    parser.add_argument(
        "--output",
        default=os.path.expanduser("~/claude-code-usage-report.txt"),
        help="Output file path (default: ~/claude-code-usage-report.txt)",
    )
    parser.add_argument(
        "--update-pricing",
        action="store_true",
        help="Fetch latest pricing from Anthropic docs and update pricing.json",
    )
    args = parser.parse_args()

    if args.update_pricing:
        show_current_pricing()
        sys.exit(0)

    # Parse dates
    start_date = None
    end_date = None
    if args.start_date:
        try:
            start_date = datetime.strptime(args.start_date, "%Y-%m-%d").date()
        except ValueError:
            print(f"Error: invalid start date '{args.start_date}', use YYYY-MM-DD", file=sys.stderr)
            sys.exit(1)
    if args.end_date:
        try:
            end_date = datetime.strptime(args.end_date, "%Y-%m-%d").date()
        except ValueError:
            print(f"Error: invalid end date '{args.end_date}', use YYYY-MM-DD", file=sys.stderr)
            sys.exit(1)

    base_path = os.path.expanduser("~/.claude/projects")
    if not os.path.isdir(base_path):
        print("Error: ~/.claude/projects/ directory not found", file=sys.stderr)
        sys.exit(1)

    files = scan_jsonl_files(base_path, args.project)
    if not files:
        print("No session files found.", file=sys.stderr)
        sys.exit(1)

    projects, daily, global_models = process_files(files, start_date, end_date)

    if not projects:
        print("No token usage data found for the specified filters.", file=sys.stderr)
        sys.exit(1)

    report = generate_report(projects, daily, global_models)

    print(report)

    try:
        with open(args.output, "w") as f:
            f.write(report)
            f.write("\n")
        print(f"\nReport saved to {args.output}", file=sys.stderr)
    except OSError as e:
        print(f"Warning: could not save report to {args.output}: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
