# Agent Skills Development Justfile
# https://github.com/casey/just

set quiet := true

# List available recipes
default:
    just --list

# ============================================================================
# Quality
# ============================================================================

# Lint all markdown files
[group('quality')]
lint:
    echo "🔍 Linting markdown files..."
    npx -y markdownlint-cli "**/*.md" --config .markdownlint.json

# Fix markdown linting issues automatically
[group('quality')]
lint-fix:
    echo "🔧 Fixing markdown issues..."
    npx -y markdownlint-cli "**/*.md" --config .markdownlint.json --fix

# Validate skill structure for all skills (errors block, warnings inform)
[group('quality')]
validate:
    #!/usr/bin/env bash
    set -euo pipefail
    SPEC="https://agentskills.io/specification"
    echo "✅ Validating skill structure..."
    has_errors=false
    for skill_dir in skills/*/; do
        [ ! -f "${skill_dir}SKILL.md" ] && continue
        skill_name=$(basename "$skill_dir")
        echo "Checking ${skill_dir}SKILL.md..."

        # --- ERRORS (blocking) ---

        # Spec: SKILL.md must contain YAML frontmatter ($SPEC)
        if ! grep -q "^---" "${skill_dir}SKILL.md"; then
            echo "  ❌ ERROR: Missing frontmatter in ${skill_dir}SKILL.md"
            has_errors=true
            continue
        fi

        # Spec: 'name' is a required frontmatter field ($SPEC)
        if ! grep -q "^name:" "${skill_dir}SKILL.md"; then
            echo "  ❌ ERROR: Missing 'name' in frontmatter of ${skill_dir}SKILL.md"
            has_errors=true
            continue
        fi

        # Spec: 'description' is a required frontmatter field ($SPEC)
        if ! grep -q "^description:" "${skill_dir}SKILL.md"; then
            echo "  ❌ ERROR: Missing 'description' in frontmatter of ${skill_dir}SKILL.md"
            has_errors=true
            continue
        fi

        # Extract name from frontmatter
        fm_name=$(sed -n 's/^name: *//p' "${skill_dir}SKILL.md" | head -1)

        # Spec: name must match the parent directory name ($SPEC)
        if [ "$fm_name" != "$skill_name" ]; then
            echo "  ❌ ERROR: Frontmatter name '$fm_name' does not match directory name '$skill_name'"
            has_errors=true
        fi

        # Spec: name must be lowercase alphanumeric + hyphens, no leading/trailing/consecutive hyphens ($SPEC)
        if ! echo "$fm_name" | grep -qE '^[a-z0-9]+(-[a-z0-9]+)*$'; then
            echo "  ❌ ERROR: Name '$fm_name' is not valid kebab-case (must be lowercase alphanumeric + hyphens, no leading/trailing/consecutive hyphens)"
            has_errors=true
        fi

        # Spec: name must be 1-64 characters ($SPEC)
        name_len=${#fm_name}
        if [ "$name_len" -lt 1 ] || [ "$name_len" -gt 64 ]; then
            echo "  ❌ ERROR: Name '$fm_name' length ($name_len) must be between 1 and 64 characters"
            has_errors=true
        fi

        # Extract description from frontmatter
        desc=$(sed -n '/^description:/,/^---$/p' "${skill_dir}SKILL.md" | sed '1s/^description: *//;$d' | tr '\n' ' ' | sed 's/ *$//')
        desc_len=${#desc}

        # Spec: description must be 1-1024 characters, non-empty ($SPEC)
        if [ "$desc_len" -lt 1 ] || [ "$desc_len" -gt 1024 ]; then
            echo "  ❌ ERROR: Description length ($desc_len) must be between 1 and 1024 characters"
            has_errors=true
        fi

        # Spec: optional 'compatibility' field must be 1-500 characters if present ($SPEC)
        compat=$(sed -n 's/^compatibility: *//p' "${skill_dir}SKILL.md" | head -1)
        if [ -n "$compat" ]; then
            compat_len=${#compat}
            if [ "$compat_len" -lt 1 ] || [ "$compat_len" -gt 500 ]; then
                echo "  ❌ ERROR: Compatibility length ($compat_len) must be between 1 and 500 characters"
                has_errors=true
            fi
        fi

        # --- WARNINGS (informational) ---

        # Best practice: descriptions should include trigger phrases (docs/reference-skill-spec.md#description-field)
        has_trigger=false
        for phrase in "use when" "when user" "mention" "activate" "trigger"; do
            if echo "$desc" | grep -qi "$phrase"; then
                has_trigger=true
                break
            fi
        done
        if [ "$has_trigger" = "false" ]; then
            echo "  ⚠️  WARNING: Description lacks trigger phrases (e.g., 'Use when...', 'When user mentions...')"
        fi

        # Spec: body recommended under 500 lines, split longer content into references/ ($SPEC)
        line_count=$(wc -l < "${skill_dir}SKILL.md")
        if [ "$line_count" -gt 500 ]; then
            echo "  ⚠️  WARNING: SKILL.md has $line_count lines (recommended: <500). Consider moving details to references/"
        fi

        # Convention: standard subdirectories are references/, scripts/, assets/, evals/, examples/
        # (docs/reference-skill-spec.md#skill-directory-structure)
        for subdir in "${skill_dir}"*/; do
            [ ! -d "$subdir" ] && continue
            subdir_name=$(basename "$subdir")
            case "$subdir_name" in
                references|scripts|assets|evals|examples) ;;
                *)
                    echo "  ⚠️  WARNING: Non-standard subdirectory '$subdir_name' (expected: references/, scripts/, assets/, evals/, examples/)"
                    ;;
            esac
        done

        # Best practice: evals are recommended for every skill (docs/reference-skill-spec.md#evals-schema)
        if [ ! -f "${skill_dir}evals/evals.json" ]; then
            echo "  ⚠️  WARNING: No evals found. Consider adding ${skill_dir}evals/evals.json"
        fi

        echo "  ✅ ${skill_dir}SKILL.md is valid"
    done
    if [ "$has_errors" = "true" ]; then
        echo "❌ Validation failed with errors"
        exit 1
    fi
    echo "✅ All skills validated successfully"

# Validate evals JSON syntax and required fields
[group('quality')]
check-evals:
    #!/usr/bin/env bash
    set -euo pipefail
    echo "🧪 Validating evals..."
    has_errors=false
    found_evals=false
    for skill_dir in skills/*/; do
        [ ! -f "${skill_dir}evals/evals.json" ] && continue
        found_evals=true
        echo "Checking ${skill_dir}evals/evals.json..."

        # Check valid JSON and required fields
        node scripts/check-evals.js "${skill_dir}evals/evals.json" || has_errors=true
    done
    if [ "$found_evals" = "false" ]; then
        echo "⚠️  No evals found in any skill"
    fi
    if [ "$has_errors" = "true" ]; then
        echo "❌ Evals validation failed"
        exit 1
    fi
    echo "✅ All evals validated successfully"

# Run all checks (lint + validate + evals)
[group('quality')]
check: lint validate check-evals
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
    if [ -d "skills/{{ name }}" ]; then
        echo "❌ Skill directory 'skills/{{ name }}' already exists"
        exit 1
    fi
    # Spec: name must be lowercase alphanumeric + hyphens, no leading/trailing/consecutive hyphens
    # (https://agentskills.io/specification)
    if ! echo "{{ name }}" | grep -qE '^[a-z0-9]+(-[a-z0-9]+)*$'; then
        echo "❌ Skill name must be kebab-case (lowercase alphanumeric + hyphens, no leading/trailing/consecutive hyphens)"
        exit 1
    fi
    mkdir -p "skills/{{ name }}"
    printf '%s\n' \
        '---' \
        'name: {{ name }}' \
        'description: TODO - Add description for {{ name }} skill. Use when user mentions...' \
        'globs: []' \
        '---' \
        '' \
        '# {{ name }}' \
        '' \
        'TODO - Add skill documentation' \
        '' \
        '<!-- Optional directories: references/, scripts/, assets/, evals/ -->' \
        > "skills/{{ name }}/SKILL.md"

    # Create evals boilerplate
    mkdir -p "skills/{{ name }}/evals"
    node scripts/create-evals-boilerplate.js "skills/{{ name }}"

    echo "✅ Created new skill: skills/{{ name }}"
    echo "📝 Edit skills/{{ name }}/SKILL.md to add your skill documentation"
    echo "🧪 Edit skills/{{ name }}/evals/evals.json to add test scenarios"

# List all skills in the repository
[group('skills')]
list-skills:
    #!/usr/bin/env bash
    set -euo pipefail
    echo "📋 Available skills:"
    for skill_dir in skills/*/; do
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
    if [ ! -d "skills/{{ skill }}" ]; then
        echo "❌ Skill directory 'skills/{{ skill }}' does not exist"
        exit 1
    fi
    if [ ! -f "skills/{{ skill }}/SKILL.md" ]; then
        echo "❌ SKILL.md not found in skills/{{ skill }}/"
        exit 1
    fi
    echo "🧪 Testing {{ skill }} skill..."
    echo ""
    echo "📋 Validating skill structure..."
    just validate
    echo ""
    echo "📝 Skill content preview:"
    echo "===================="
    head -20 "skills/{{ skill }}/SKILL.md"
    echo "===================="
    echo ""
    echo "✅ Skill {{ skill }} is valid and ready"
    echo ""
    echo "To install locally for testing:"
    echo "  npx skills add $PWD/skills/{{ skill }}"

# ============================================================================
# Release
# ============================================================================

# Validate commit message format
[group('release')]
validate-commit message:
    #!/usr/bin/env bash
    set -euo pipefail
    echo "✅ Validating commit message..."
    echo "{{ message }}" | npx -y -p @commitlint/cli -p @commitlint/config-conventional commitlint

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
    rm skills.md.tmp

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

# ============================================================================
# Development
# ============================================================================

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
