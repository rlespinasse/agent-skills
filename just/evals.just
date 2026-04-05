# Run evals for a specific skill using promptfoo + Claude Code CLI
[group('evals')]
eval-skill skill:
    #!/usr/bin/env bash
    set -euo pipefail
    if [ -z "{{ skill }}" ]; then
        echo "❌ Please specify a skill name: just eval-skill <skill-name>"
        exit 1
    fi
    if [ ! -f "skills/{{ skill }}/evals/evals.json" ]; then
        echo "❌ No evals found for skill: {{ skill }}"
        exit 1
    fi
    echo "🧪 Generating eval config for {{ skill }}..."
    node scripts/generate-eval-config.js "{{ skill }}"
    echo "🚀 Running evals (this uses Claude Code CLI — each eval ≈ 2 calls)..."
    npx -y promptfoo@latest eval
    echo "✅ Done. Run 'just eval-view' to browse results."

# Run evals for all skills using promptfoo + Claude Code CLI
[group('evals')]
eval-all:
    #!/usr/bin/env bash
    set -euo pipefail
    echo "🧪 Generating eval config for all skills..."
    node scripts/generate-eval-config.js
    echo "🚀 Running evals (this uses Claude Code CLI — each eval ≈ 2 calls)..."
    npx -y promptfoo@latest eval
    echo "✅ Done. Run 'just eval-view' to browse results."

# Open promptfoo results viewer in browser
[group('evals')]
eval-view:
    npx -y promptfoo@latest view
