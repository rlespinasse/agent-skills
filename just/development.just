# Set up local development environment (git hooks)
[group('development')]
setup:
    echo "🔧 Setting up development environment..."
    git config core.hooksPath .githooks
    echo "✅ Git hooks configured (using .githooks/)"

# Check everything before commit
[group('development')]
pre-commit: sync fix check
    echo "✅ Ready to commit"

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
