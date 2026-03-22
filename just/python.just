# Run Python tests for all skills with scripts
[group('python')]
test-python:
    #!/usr/bin/env bash
    set -euo pipefail
    echo "🐍 Running Python tests..."
    has_tests=false
    for test_file in skills/*/scripts/test_*.py; do
        [ ! -f "$test_file" ] && continue
        has_tests=true
        dir=$(dirname "$test_file")
        name=$(basename "$test_file" .py)
        echo "  Testing $dir/$name..."
        (cd "$dir" && python3 -m unittest "$name" -v)
    done
    if [ "$has_tests" = "false" ]; then
        echo "  No Python tests found"
    fi
    echo "✅ Python tests passed"

# Fetch Anthropic pricing page and check for changes
[group('python')]
check-pricing file="":
    #!/usr/bin/env bash
    set -euo pipefail
    if [ -n "{{ file }}" ]; then
        python3 skills/claude-code-usage-report/scripts/check_pricing.py --file "{{ file }}"
    else
        echo "📡 Fetching pricing page..."
        HTTP_CODE=$(curl -s -L -w "%{http_code}" \
            -H "User-Agent: Mozilla/5.0 (compatible; agent-skills pricing check)" \
            -o /tmp/pricing_page.html \
            "https://docs.anthropic.com/en/docs/about-claude/pricing")
        FILE_SIZE=$(wc -c < /tmp/pricing_page.html | tr -d ' ')
        echo "  HTTP $HTTP_CODE, $FILE_SIZE bytes"
        if [ "$HTTP_CODE" -ne 200 ]; then
            echo "❌ Fetch failed (HTTP $HTTP_CODE)"
            head -20 /tmp/pricing_page.html
            exit 1
        fi
        if [ "$FILE_SIZE" -eq 0 ]; then
            echo "❌ Fetched file is empty"
            exit 1
        fi
        python3 skills/claude-code-usage-report/scripts/check_pricing.py --file /tmp/pricing_page.html
    fi
