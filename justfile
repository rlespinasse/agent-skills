# Agent Skills Development Justfile
# https://github.com/casey/just

set quiet := true

# List available recipes
default:
    just --list

# ============================================================================
# Setup
# ============================================================================

# Install development dependencies
[group('setup')]
install:
    #!/usr/bin/env bash
    set -euo pipefail
    echo "📦 Installing development dependencies..."
    npm install -g markdownlint-cli

# ============================================================================
# Quality
# ============================================================================

# Lint all markdown files
[group('quality')]
lint:
    echo "🔍 Linting markdown files..."
    markdownlint "**/*.md" --config .markdownlint.json

# Fix markdown linting issues automatically
[group('quality')]
lint-fix:
    echo "🔧 Fixing markdown issues..."
    markdownlint "**/*.md" --config .markdownlint.json --fix

# Validate skill structure for all skills
[group('quality')]
validate:
    #!/usr/bin/env bash
    set -euo pipefail
    echo "✅ Validating skill structure..."
    for skill_dir in */; do
        if [ -f "${skill_dir}SKILL.md" ]; then
            echo "Checking ${skill_dir}SKILL.md..."
            if ! grep -q "^---" "${skill_dir}SKILL.md"; then
                echo "❌ Missing frontmatter in ${skill_dir}SKILL.md"
                exit 1
            fi
            if ! grep -q "^name:" "${skill_dir}SKILL.md"; then
                echo "❌ Missing 'name' in frontmatter of ${skill_dir}SKILL.md"
                exit 1
            fi
            if ! grep -q "^description:" "${skill_dir}SKILL.md"; then
                echo "❌ Missing 'description' in frontmatter of ${skill_dir}SKILL.md"
                exit 1
            fi
            echo "✅ ${skill_dir}SKILL.md is valid"
        fi
    done
    echo "✅ All skills validated successfully"

# Run all checks (lint + validate)
[group('quality')]
check: lint validate
    echo "✅ All checks passed"

# Fix all auto-fixable issues
[group('quality')]
fix: lint-fix
    echo "✅ All fixes applied"

# Format the justfile
[group('quality')]
format:
    echo "🎨 Formatting justfile..."
    just --fmt --unstable

# ============================================================================
# Skills
# ============================================================================

# Create a new skill with boilerplate
[group('skills')]
new-skill name:
    #!/usr/bin/env bash
    set -euo pipefail
    echo "📝 Creating new skill: {{ name }}..."
    if [ -d "{{ name }}" ]; then
        echo "❌ Skill directory '{{ name }}' already exists"
        exit 1
    fi
    mkdir -p "{{ name }}"
    echo "---" > "{{ name }}/SKILL.md"
    echo "name: {{ name }}" >> "{{ name }}/SKILL.md"
    echo "description: TODO - Add description for {{ name }} skill" >> "{{ name }}/SKILL.md"
    echo "---" >> "{{ name }}/SKILL.md"
    echo "" >> "{{ name }}/SKILL.md"
    echo "# {{ name }}" >> "{{ name }}/SKILL.md"
    echo "" >> "{{ name }}/SKILL.md"
    echo "TODO - Add skill documentation" >> "{{ name }}/SKILL.md"
    echo "✅ Created new skill: {{ name }}"
    echo "📝 Edit {{ name }}/SKILL.md to add your skill documentation"

# List all skills in the repository
[group('skills')]
list-skills:
    #!/usr/bin/env bash
    set -euo pipefail
    echo "📋 Available skills:"
    for skill_dir in */; do
        if [ -f "${skill_dir}SKILL.md" ]; then
            skill_name=$(basename "$skill_dir")
            description=$(sed -n '/^description:/,/^---/p' "${skill_dir}SKILL.md" | sed -n '1p' | sed 's/^description: //')
            echo "  • $skill_name"
            echo "    ${description:-No description}"
        fi
    done

# Test skill locally by validating and previewing
[group('skills')]
test-skill skill="":
    #!/usr/bin/env bash
    set -euo pipefail
    if [ -z "{{ skill }}" ]; then
        echo "❌ Please specify a skill name: just test-skill <skill-name>"
        exit 1
    fi
    if [ ! -d "{{ skill }}" ]; then
        echo "❌ Skill directory '{{ skill }}' does not exist"
        exit 1
    fi
    if [ ! -f "{{ skill }}/SKILL.md" ]; then
        echo "❌ SKILL.md not found in {{ skill }}/"
        exit 1
    fi
    echo "🧪 Testing {{ skill }} skill..."
    echo ""
    echo "📋 Validating skill structure..."
    just validate
    echo ""
    echo "📝 Skill content preview:"
    echo "===================="
    head -20 "{{ skill }}/SKILL.md"
    echo "===================="
    echo ""
    echo "✅ Skill {{ skill }} is valid and ready"
    echo ""
    echo "To install locally for testing:"
    echo "  npx skills add $PWD/{{ skill }}"

# Show installation command for remote testing
[group('skills')]
test-install skill="":
    #!/usr/bin/env bash
    set -euo pipefail
    if [ -z "{{ skill }}" ]; then
        echo "🧪 Testing full repository installation..."
        echo "npx skills add rlespinasse/agent-skills"
    else
        echo "🧪 Testing {{ skill }} installation..."
        echo "npx skills add rlespinasse/agent-skills/{{ skill }}"
    fi
    echo "Note: Run the command above manually to test installation"

# Show skill specification compliance
[group('skills')]
spec:
    echo "📋 Agent Skills Specification (https://agentskills.io/specification)"
    echo ""
    echo "Required structure:"
    echo "  • Each skill must have a SKILL.md file"
    echo "  • SKILL.md must have YAML frontmatter with 'name' and 'description'"
    echo "  • Skill names should be kebab-case"
    echo ""
    echo "Current compliance:"
    just validate

# ============================================================================
# Release
# ============================================================================

# Run semantic-release locally (dry-run)
[group('release')]
release-dry-run:
    #!/usr/bin/env bash
    set -euo pipefail
    echo "🔍 Running semantic-release in dry-run mode..."
    npx semantic-release --dry-run

# Validate commit message format
[group('release')]
validate-commit message:
    #!/usr/bin/env bash
    set -euo pipefail
    echo "✅ Validating commit message..."
    echo "{{ message }}" | npx commitlint

# ============================================================================
# Documentation
# ============================================================================

# Update README with current skills list
[group('documentation')]
update-readme:
    #!/usr/bin/env bash
    set -euo pipefail
    echo "📝 Updating README.md..."

    # Build skills section
    for skill_dir in */; do
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
        } >> /tmp/skills.md
    done

    # Replace skills section in README
    sed -n '1,/^## Available Skills$/p' README.md > /tmp/readme-new.md
    echo "" >> /tmp/readme-new.md
    cat /tmp/skills.md >> /tmp/readme-new.md
    sed -n '/^## Installation$/,$p' README.md >> /tmp/readme-new.md

    mv /tmp/readme-new.md README.md
    rm /tmp/skills.md

    echo "✅ README.md updated"

# ============================================================================
# Development
# ============================================================================

# Check everything before commit
[group('development')]
pre-commit: update-readme fix check
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
    rm -rf node_modules
    rm -rf .DS_Store
    echo "✅ Cleanup complete"
