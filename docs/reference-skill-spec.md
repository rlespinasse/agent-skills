# Skill Specification Reference

This page documents the structural requirements and conventions for agent skills in this repository.

## SKILL.md Frontmatter

Each skill must have a `SKILL.md` file with YAML frontmatter:

```yaml
---
name: skill-name
description: Brief description of what the skill does and when to use it
---
```

| Field | Required | Constraints |
| ------------- | -------- | ------------------------------------------- |
| `name` | Yes | Kebab-case, 1-64 characters, must match directory name |
| `description` | Yes | 1-1024 characters |

## SKILL.md Content Structure

1. **Main heading** — clear title for the skill
2. **Introduction** — brief overview and context
3. **Decision trees** — help agents choose between options
4. **Quick reference** — common patterns and examples
5. **Detailed documentation** — comprehensive information
6. **Examples** — real-world usage scenarios

Keep SKILL.md under 500 lines. Move detailed content to `references/`.

## Description Field

The `description` determines when agents activate the skill. Include:

1. **What the skill does** — one sentence summary
2. **Trigger phrases** — keywords that should activate the skill
3. **Scope boundaries** — mention related skills if applicable

**Pattern:**

```text
<What it does>. Use when user mentions '<keyword1>', '<keyword2>', or '<keyword3>'.
For <related topic>, see <other-skill>.
```

**Good example:**

```yaml
description: Decision guide for the third-party Draw.io export ecosystem by @rlespinasse.
  Covers docker-drawio-desktop-headless, drawio-exporter, drawio-export, and drawio-export-action.
  Use when user mentions diagram export, CI/CD automation, batch processing, or Draw.io files.
  Helps select the right tool based on context.
```

**Anti-patterns:**

- `"A skill for drawio"` — too vague, no trigger phrases
- `"Helps with exports"` — no context, no keywords
- Missing scope boundaries when related skills exist

## Skill Directory Structure

```text
my-skill/
├── SKILL.md              # Required: Main skill documentation
├── evals/
│   └── evals.json        # Recommended: Test scenarios
├── references/           # Optional: Detailed docs
├── scripts/              # Optional: Helper scripts
├── assets/               # Optional: Images, diagrams
└── examples/             # Optional: Example files
```

| Directory | Purpose | When to use |
| ------------- | ---------------------------------- | -------------------------------------------------- |
| `evals/` | Test scenarios (`evals.json`) | Always recommended — defines expected behavior |
| `references/` | Detailed reference documentation | When SKILL.md exceeds 500 lines |
| `scripts/` | Helper scripts for the skill | When skill involves automation |
| `assets/` | Images, diagrams, static files | When skill needs visual aids |
| `examples/` | Example files and configurations | When showing complete working examples |

## Evals Schema

Each skill should have `evals/evals.json` with test scenarios:

```json
[
  {
    "id": "unique-eval-id",
    "prompt": "What the user asks the agent",
    "expected_output": "Brief description of expected agent behavior",
    "assertions": [
      "specific assertion about the response",
      "another assertion to verify"
    ],
    "files": [
      "skill-name/SKILL.md"
    ]
  }
]
```

| Field | Type | Required | Description |
| ----------------- | -------- | -------- | ------------------------------------------------- |
| `id` | string | Yes | Unique identifier (must be unique across the file) |
| `prompt` | string | Yes | The user input that triggers the skill |
| `expected_output` | string | Yes | Brief description of expected agent behavior |
| `assertions` | string[] | Yes | Specific, verifiable claims about the response |
| `files` | string[] | Yes | Skill files relevant to the eval |
