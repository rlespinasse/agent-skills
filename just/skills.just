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
    just validate-skill "{{ skill }}"
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
