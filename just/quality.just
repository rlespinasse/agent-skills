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

        # agentskills.io spec: description must be 1-1024 characters, non-empty
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
