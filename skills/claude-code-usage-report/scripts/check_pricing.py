#!/usr/bin/env python3
"""Check Anthropic pricing page for changes and update pricing.json.

Two-layer detection:
  1. Hash-based: detect if the pricing page content changed at all
  2. Price extraction: attempt to parse specific prices and show diffs

If extraction fails, the workflow still opens a PR with the hash change
so a human can review manually.

Exit codes:
  0 — changes detected (pricing.json updated)
  1 — no changes detected
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
# After a match, the next 4 dollar amounts are: input, output, cache_read, cache_write.
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
    - found_prices: dict of {model_key: {input, output, cache_read, cache_write}}
    - errors: list of error messages for models that could not be extracted
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

            if len(prices) < 4:
                errors.append(
                    f"  {key}: found model name (pattern: {pattern}) at position "
                    f"{match.start()}, but only {len(prices)} price(s) after it "
                    f"(need 4). Nearby text: ...{after_text[:100]}..."
                )
                continue

            found[key] = {
                "input": float(prices[0]),
                "output": float(prices[1]),
                "cache_read": float(prices[2]),
                "cache_write": float(prices[3]),
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
        for field in ("input", "output", "cache_read", "cache_write"):
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
        for field in ("input", "output", "cache_read", "cache_write"):
            data["models"][key][field] = new_prices[field]

    data["updated"] = datetime.now().strftime("%Y-%m-%d")

    with open(PRICING_FILE, "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")

    print(f"Updated {PRICING_FILE}")


def main():
    parser = argparse.ArgumentParser(
        description="Check Anthropic pricing page for changes"
    )
    parser.add_argument(
        "--file",
        help="HTML file to parse (default: read from stdin)",
    )
    args = parser.parse_args()

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
        sys.exit(1)

    print(f"Page content changed (stored: {stored_hash[:16] or 'none'}...)")
    print()

    # --- Layer 2: Price extraction ---
    fetched, extraction_errors = extract_prices_from_html(html)

    print(f"Extracted prices for {len(fetched)}/{len(EXPECTED_MODELS)} model(s)")
    for key, prices in fetched.items():
        print(f"  {key}: input=${prices['input']} output=${prices['output']} "
              f"cache_read=${prices['cache_read']} cache_write=${prices['cache_write']}")

    if extraction_errors:
        print()
        print(f"Extraction errors ({len(extraction_errors)}):")
        for err in extraction_errors:
            print(err)

    print()

    # --- Decide what to do ---
    if fetched:
        changes, has_price_changes = compare_prices(fetched)
        if has_price_changes:
            print("Price changes detected:")
            for change in changes:
                print(change)
            update_pricing_json(fetched)
        else:
            print("Extracted prices match pricing.json (page changed but prices didn't).")

    # Always update the hash so we don't re-alert on the same page content
    with open(PRICING_FILE) as f:
        data = json.load(f)
    data["page_hash"] = page_hash
    data["updated"] = datetime.now().strftime("%Y-%m-%d")
    with open(PRICING_FILE, "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")

    # If the page changed, always signal it — even if extraction failed.
    # The PR will show the hash update + any price changes + extraction errors in logs.
    if fetched and not has_price_changes and not extraction_errors:
        # Page layout changed but prices are the same and extraction was clean
        print("Only non-pricing content changed. Updating hash only.")
        sys.exit(0)

    # Page changed: either prices changed, or extraction had issues worth reviewing
    sys.exit(0)


if __name__ == "__main__":
    main()
