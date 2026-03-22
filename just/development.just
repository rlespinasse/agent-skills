# Watch markdown files for changes (requires entr)
[group('development')]
watch:
    #!/usr/bin/env bash
    set -euo pipefail
    echo "👀 Watching markdown files for changes..."
    echo "Install 'entr' if not available: brew install entr"
    find . -name '*.md' -not -path './.git/*' | entr just lint

# Clean generated files and caches
[group('development')]
clean:
    #!/usr/bin/env bash
    set -euo pipefail
    echo "🧹 Cleaning up..."
    find . -name '.DS_Store' -not -path './.git/*' -delete
    rm -f *.tmp
    echo "✅ Cleanup complete"
