# Update README with current skills list
[group('documentation')]
update-readme:
    #!/usr/bin/env bash
    set -euo pipefail
    echo "📝 Updating README.md..."

    # Clean up temp files on exit
    trap 'rm -f skills.md.tmp readme-new.md.tmp' EXIT

    # Build skills section
    > skills.md.tmp
    for skill_dir in skills/*/; do
        [ ! -f "${skill_dir}SKILL.md" ] && continue

        skill_name=$(basename "$skill_dir")
        echo "Processing ${skill_name}..." >&2

        # Extract description: line after "description:" until next "---"
        desc=$(sed -n '/^description:/,/^---$/p' "${skill_dir}SKILL.md" | sed '1s/^description: *//;$d' | tr -d '\n')

        # Write skill entry with word wrapping
        {
            echo "### ${skill_name}"
            echo ""
            echo "$desc" | fold -s -w 120 | sed 's/[[:space:]]*$//'
            echo ""
        } >> skills.md.tmp
    done

    # Replace skills section in README
    sed -n '1,/^## Available Skills$/p' README.md > readme-new.md.tmp
    echo "" >> readme-new.md.tmp
    cat skills.md.tmp >> readme-new.md.tmp
    sed -n '/^## Installation$/,$p' README.md >> readme-new.md.tmp

    mv readme-new.md.tmp README.md

    echo "✅ README.md updated"

# Update .claude-plugin/marketplace.json from skill directories
[group('documentation')]
update-marketplace:
    #!/usr/bin/env bash
    set -euo pipefail
    echo "📝 Updating .claude-plugin/marketplace.json..."
    mkdir -p .claude-plugin
    node scripts/update-marketplace.js
    echo "✅ marketplace.json updated"

# Sync all generated files (README + marketplace)
[group('documentation')]
sync: update-readme update-marketplace
    echo "✅ All generated files synced"
