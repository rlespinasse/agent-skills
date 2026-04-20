#!/usr/bin/env python3
"""Check Anthropic pricing page for changes and update pricing.json.

Two-layer detection:
  1. Hash-based: detect if the pricing page content changed at all
  2. Price extraction: attempt to parse specific prices and show diffs

pricing.json is written only when there's a meaningful change — a real
price delta, a table-structure alert, or an extraction error. Page-hash
drift alone (common when unrelated page content shifts) is ignored so
the workflow doesn't open PRs that only bump `updated` + `page_hash`.

Exit codes:
  0 — script ran successfully (pricing.json may or may not have been updated)
  2 — error (no HTML, fetch failure, etc.)

Usage:
    python check_pricing.py --file pricing_page.html
    curl -s URL | python check_pricing.py
"""

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PRICING_FILE = SCRIPT_DIR / "pricing.json"

# Expected number of current-gen models to extract
EXPECTED_MODELS = ["opus:current", "sonnet:current", "haiku:current"]

# Patterns to locate model pricing rows in stripped HTML text.
# Each entry tries multiple regex patterns in order; first match wins.
# After a match, the next 5 dollar amounts are (in page column order):
#   input, cache_write_5m, cache_write_1h, cache_read, output.
MODEL_PATTERNS = {
    "opus:current": [
        r"Opus\s+4[.\s]*[56]",
        r"claude-opus-4-[56]",
    ],
    "sonnet:current": [
        r"Sonnet\s+4[.\s]*[56]",
        r"claude-sonnet-4-[56]",
    ],
    "haiku:current": [
        r"Haiku\s+4[.\s]*5",
        r"claude-haiku-4-5",
    ],
}


ALERTS_FILE = Path("/tmp/pricing_alerts.json")
PRICING_SOURCE = "https://docs.anthropic.com/en/docs/about-claude/pricing"


def extract_table_columns(html: str) -> list[str]:
    """Extract column headers from the first pricing table.

    Looks for a table row (<th> cells) that contains "Input" or "Output"
    to identify the model pricing table header.
    """
    # Find all <th> sequences that look like a pricing table header
    header_re = re.compile(
        r"<th[^>]*>(.*?)</th>", re.IGNORECASE | re.DOTALL
    )
    # Find table rows
    row_re = re.compile(
        r"<tr[^>]*>(.*?)</tr>", re.IGNORECASE | re.DOTALL
    )

    for row_match in row_re.finditer(html):
        row_html = row_match.group(1)
        headers = header_re.findall(row_html)
        if not headers:
            continue

        # Clean HTML tags and whitespace from header text
        cleaned = []
        for h in headers:
            text = re.sub(r"<[^>]+>", "", h).strip()
            text = re.sub(r"\s+", " ", text)
            if text:
                cleaned.append(text)

        # Identify the pricing table by checking for pricing-related headers
        lower_joined = " ".join(c.lower() for c in cleaned)
        if "input" in lower_joined and "output" in lower_joined:
            # Skip the "Model" column itself
            return [c for c in cleaned if c.lower() != "model"]

    return []


def check_table_structure(html: str, expected_columns: list[str]) -> list[str]:
    """Compare actual table columns against expected ones.

    Returns a list of alert messages (empty if structure matches).
    """
    actual = extract_table_columns(html)
    if not actual:
        return ["Could not extract table column headers from the pricing page."]

    alerts = []

    if actual != expected_columns:
        alerts.append(
            f"Table column structure changed.\n"
            f"  Expected: {expected_columns}\n"
            f"  Actual:   {actual}"
        )

        # Detect specific changes
        expected_set = set(expected_columns)
        actual_set = set(actual)

        new_cols = actual_set - expected_set
        removed_cols = expected_set - actual_set

        if new_cols:
            alerts.append(f"New columns added: {sorted(new_cols)}")
        if removed_cols:
            alerts.append(f"Columns removed: {sorted(removed_cols)}")
        if not new_cols and not removed_cols:
            alerts.append("Column order changed (same columns, different order).")

    return alerts


def compute_page_hash(html: str) -> str:
    """Compute a stable hash of the pricing-relevant content.

    Strips whitespace and HTML tags to reduce noise from layout changes.
    """
    text = re.sub(r"<[^>]+>", " ", html)
    text = re.sub(r"\s+", " ", text).strip()
    return hashlib.sha256(text.encode()).hexdigest()


def extract_prices_from_html(html: str) -> tuple[dict, list[str]]:
    """Extract pricing data from HTML content.

    Returns (found_prices, errors) where:
    - found_prices: dict of {model_key: {input, output, cache_read,
      cache_write_5m, cache_write_1h}}
    - errors: list of error messages for models that could not be extracted

    The pricing page column order is:
      Base Input | 5m Cache Writes | 1h Cache Writes | Cache Hits | Output
    """
    text = re.sub(r"<[^>]+>", " ", html)
    text = re.sub(r"\s+", " ", text)

    price_re = re.compile(r"\$(\d+(?:\.\d+)?)")
    found = {}
    errors = []

    for key, patterns in MODEL_PATTERNS.items():
        matched = False
        for pattern in patterns:
            model_re = re.compile(pattern, re.IGNORECASE)
            match = model_re.search(text)
            if not match:
                continue

            after_text = text[match.end():match.end() + 500]
            prices = price_re.findall(after_text)

            if len(prices) < 5:
                errors.append(
                    f"  {key}: found model name (pattern: {pattern}) at position "
                    f"{match.start()}, but only {len(prices)} price(s) after it "
                    f"(need 5). Nearby text: ...{after_text[:100]}..."
                )
                continue

            found[key] = {
                "input": float(prices[0]),
                "cache_write_5m": float(prices[1]),
                "cache_write_1h": float(prices[2]),
                "cache_read": float(prices[3]),
                "output": float(prices[4]),
            }
            matched = True
            break

        if not matched and key not in found:
            errors.append(
                f"  {key}: no matching model name found on the page. "
                f"Tried patterns: {patterns}"
            )

    return found, errors


def compare_prices(fetched: dict) -> tuple[list[str], bool]:
    """Compare fetched prices with pricing.json.

    Returns (change_lines, has_changes).
    Does NOT modify pricing.json — caller decides whether to write.
    """
    with open(PRICING_FILE) as f:
        data = json.load(f)

    changes = []
    for key, new_prices in fetched.items():
        if key not in data["models"]:
            changes.append(f"  {key}: NEW model (not in pricing.json)")
            continue
        current = data["models"][key]
        for field in ("input", "output", "cache_read", "cache_write_5m", "cache_write_1h"):
            old_val = current.get(field)
            new_val = new_prices.get(field)
            if old_val != new_val:
                changes.append(f"  {key}.{field}: ${old_val} -> ${new_val}")

    return changes, len(changes) > 0


def update_pricing_json(fetched: dict):
    """Write extracted prices into pricing.json."""
    with open(PRICING_FILE) as f:
        data = json.load(f)

    for key, new_prices in fetched.items():
        if key not in data["models"]:
            continue
        for field in ("input", "output", "cache_read", "cache_write_5m", "cache_write_1h"):
            data["models"][key][field] = new_prices[field]

    data["updated"] = datetime.now().strftime("%Y-%m-%d")

    with open(PRICING_FILE, "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")

    print(f"Updated {PRICING_FILE}")


def format_pr_body(alerts_file: Path, logs_url: str = "") -> str:
    """Format a PR body from the alerts file.

    Reads structure_alerts and extraction_errors from the alerts JSON
    and returns a markdown PR body string.
    """
    lines = [
        "## Summary\n",
        f"- Automated pricing update detected from [Anthropic pricing page]({PRICING_SOURCE})",
        "- Updated `skills/claude-code-usage-report/scripts/pricing.json`\n",
    ]

    if alerts_file.exists():
        with open(alerts_file) as f:
            data = json.load(f)

        alerts = data.get("structure_alerts", [])
        errors = data.get("extraction_errors", [])

        if alerts or errors:
            lines.append("## ⚠️ Maintainer action required\n")
            lines.append(
                "The pricing page structure has changed. "
                "The extraction script may need updating.\n"
            )

            if alerts:
                lines.append("**Structure alerts:**\n")
                for a in alerts:
                    for line in a.split("\n"):
                        lines.append(f"- {line}")
                lines.append("")

            if errors:
                lines.append("**Extraction errors:**\n")
                for e in errors:
                    lines.append(f"- {e.strip()}")
                lines.append("")

            lines.append("**Action items:**\n")
            lines.append(
                f"- [ ] Review column changes on the [pricing page]({PRICING_SOURCE})"
            )
            lines.append(
                "- [ ] Update `check_pricing.py` extraction logic if column order/count changed"
            )
            lines.append(
                "- [ ] Update `expected_columns` in `pricing.json` to match the new structure"
            )
            lines.append(
                "- [ ] Update `SKILL.md` if new pricing dimensions affect cost estimation"
            )
            lines.append("")

    lines.append("Please review the changes to ensure they are correct.")
    if logs_url:
        lines.append(
            f"Check the [workflow logs]({logs_url}) for extraction details and any errors."
        )
    lines.append("")
    lines.append("🤖 Generated by the update-pricing workflow")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Check Anthropic pricing page for changes"
    )
    parser.add_argument(
        "--file",
        help="HTML file to parse (default: read from stdin)",
    )
    parser.add_argument(
        "--format-pr-body",
        action="store_true",
        help="Format a PR body from the alerts file and print to stdout",
    )
    parser.add_argument(
        "--logs-url",
        default="",
        help="URL to workflow logs (used with --format-pr-body)",
    )
    args = parser.parse_args()

    if args.format_pr_body:
        print(format_pr_body(ALERTS_FILE, args.logs_url))
        return

    if args.file:
        with open(args.file) as f:
            html = f.read()
    else:
        html = sys.stdin.read()

    if not html.strip():
        print("Error: no HTML content provided", file=sys.stderr)
        sys.exit(2)

    print(f"HTML content: {len(html)} bytes")

    # --- Layer 1: Hash-based change detection ---
    page_hash = compute_page_hash(html)
    print(f"Page hash: {page_hash[:16]}...")

    with open(PRICING_FILE) as f:
        data = json.load(f)

    stored_hash = data.get("page_hash", "")
    hash_changed = page_hash != stored_hash

    if not hash_changed:
        print("Page content unchanged (hash match). No update needed.")
        sys.exit(0)

    print(f"Page content changed (stored: {stored_hash[:16] or 'none'}...)")
    print()

    # --- Layer 2: Table structure check ---
    expected_columns = data.get("expected_columns", [])
    structure_alerts = check_table_structure(html, expected_columns) if expected_columns else []

    if structure_alerts:
        print("⚠️  Table structure alerts:")
        for alert in structure_alerts:
            for line in alert.split("\n"):
                print(f"  {line}")
        print()

    # --- Layer 3: Price extraction ---
    fetched, extraction_errors = extract_prices_from_html(html)

    print(f"Extracted prices for {len(fetched)}/{len(EXPECTED_MODELS)} model(s)")
    for key, prices in fetched.items():
        print(f"  {key}: input=${prices['input']} output=${prices['output']} "
              f"cache_read=${prices['cache_read']} "
              f"cache_write_5m=${prices['cache_write_5m']} "
              f"cache_write_1h=${prices['cache_write_1h']}")

    if extraction_errors:
        print()
        print(f"Extraction errors ({len(extraction_errors)}):")
        for err in extraction_errors:
            print(err)

    print()

    # --- Decide what to do ---
    has_price_changes = False
    if fetched:
        changes, has_price_changes = compare_prices(fetched)
        if has_price_changes:
            print("Price changes detected:")
            for change in changes:
                print(change)
        else:
            print("Extracted prices match pricing.json (page changed but prices didn't).")

    meaningful_change = has_price_changes or bool(structure_alerts) or bool(extraction_errors)

    # Write alerts file for the workflow to consume
    alerts_data = {
        "structure_alerts": structure_alerts,
        "extraction_errors": extraction_errors,
    }
    with open(ALERTS_FILE, "w") as f:
        json.dump(alerts_data, f, indent=2)
        f.write("\n")

    if not meaningful_change:
        # Page content drifted (hash changed) but nothing actionable found.
        # Skip updating pricing.json so the workflow's `git diff` stays clean
        # and no spurious PR is opened. The hash will be recomputed next run.
        print("No pricing, structure, or extraction changes. Skipping pricing.json update.")
        return

    if fetched and has_price_changes:
        update_pricing_json(fetched)

    # Update the hash so a merged PR prevents re-alerting on the same content.
    with open(PRICING_FILE) as f:
        data = json.load(f)
    data["page_hash"] = page_hash
    data["updated"] = datetime.now().strftime("%Y-%m-%d")
    with open(PRICING_FILE, "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")

    if has_price_changes:
        print("Pricing data updated.")
    elif extraction_errors:
        print("Extraction had issues worth reviewing.")
    elif structure_alerts:
        print("Table structure changed — review required.")


if __name__ == "__main__":
    main()
