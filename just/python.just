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
