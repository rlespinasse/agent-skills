# Create Your First Agent Skill

In this tutorial, we will create an agent skill from scratch, validate it, and prepare it
for contribution. By the end, you will have a working skill that AI coding assistants can use.

## Before you begin

- Clone the repository and `cd` into it
- Install [just](https://github.com/casey/just) (command runner)
- Install [Node.js](https://nodejs.org/) (LTS) for `npx` tooling
- Verify your setup by running:

```bash
just check
```

You should see all checks passing with no errors.

## Step 1: Scaffold the skill

Run the `new-skill` command with a kebab-case name. We will create a skill called
`greeting-style` that helps agents choose an appropriate greeting tone.

```bash
just new-skill greeting-style
```

The output should look something like:

```text
📝 Creating new skill: greeting-style...
✅ Created new skill: skills/greeting-style
📝 Edit skills/greeting-style/SKILL.md to add your skill documentation
🧪 Edit skills/greeting-style/evals/evals.json to add test scenarios
```

This created two files:

- `skills/greeting-style/SKILL.md` -- the skill definition (with boilerplate to fill in)
- `skills/greeting-style/evals/evals.json` -- test scenarios (with placeholder entries)

## Step 2: Write the frontmatter

Open `skills/greeting-style/SKILL.md`. The scaffolded file starts with YAML frontmatter
between `---` markers. Replace the boilerplate with a real name and description.

The **description** is the most important part -- it tells AI agents when to activate your
skill. Include what the skill does, trigger keywords, and scope boundaries.

```yaml
---
name: greeting-style
description: Helps choose an appropriate greeting tone and style for messages,
  emails, and chat responses. Use when user mentions greeting, salutation, email tone,
  formal vs informal, or professional communication style.
---
```

Notice that the description follows the pattern: *what it does*, then *trigger phrases*
starting with "Use when user mentions".

## Step 3: Write the skill content

Below the frontmatter, replace the boilerplate body with the skill documentation. Structure
it as: **decision flow first**, then **quick reference**, then **detailed guidance**.

```markdown
# Greeting Style Guide

You are helping the user choose an appropriate greeting style for their communication context.

## Decision Flow

1. **Identify the medium** -- email, chat message, letter, or code comment
2. **Identify the audience** -- colleague, manager, client, open-source community
3. **Identify the tone** -- formal, semi-formal, or casual

## Quick Reference

| Context             | Tone        | Example greeting             |
| ------------------- | ----------- | ---------------------------- |
| Client email        | Formal      | "Dear Ms. Johnson,"         |
| Team Slack message  | Casual      | "Hey team,"                  |
| PR review comment   | Semi-formal | "Thanks for the PR!"        |
| Cover letter        | Formal      | "Dear Hiring Manager,"      |

## Detailed Guidance

### Formal

Use for external communication, first contact, or hierarchical contexts.
Avoid contractions and slang.

### Semi-formal

Use for colleagues you interact with regularly. Contractions are fine,
but keep the tone professional.

### Casual

Use for close teammates in informal channels. Emojis and shorthand are acceptable
when they match the team culture.

## What This Skill Does Not Cover

- Email body structure or closing phrases
- Cultural greeting norms outside English-speaking contexts
```

Keep the file under 500 lines. If you need more detail, create a `references/` subdirectory
and link to files there.

## Step 4: Write evals

Open `skills/greeting-style/evals/evals.json` and replace the boilerplate with real test
scenarios. Each eval describes a user prompt and what the agent should do in response.

Aim for 5-7 evals covering the main decision paths, plus a scope boundary test and an
ambiguous request test.

```json
[
  {
    "id": "formal-client-email",
    "prompt": "I need to write a greeting for a cold email to a potential client.",
    "expected_output": "Recommends a formal greeting appropriate for first-contact client email",
    "assertions": [
      "suggests a formal tone",
      "provides a concrete greeting example",
      "mentions the context is external or first-contact communication"
    ],
    "files": [
      "skills/greeting-style/SKILL.md"
    ]
  },
  {
    "id": "casual-team-chat",
    "prompt": "What's a good way to greet my team in our daily standup Slack message?",
    "expected_output": "Recommends a casual greeting suitable for internal team chat",
    "assertions": [
      "suggests a casual tone",
      "provides a concrete greeting example",
      "acknowledges the informal channel context"
    ],
    "files": [
      "skills/greeting-style/SKILL.md"
    ]
  },
  {
    "id": "scope-boundary-email-body",
    "prompt": "How should I structure the body of my email after the greeting?",
    "expected_output": "Recognizes that email body structure is outside the skill's scope",
    "assertions": [
      "does not provide detailed email body guidance",
      "acknowledges the limitation or redirects the user"
    ],
    "files": [
      "skills/greeting-style/SKILL.md"
    ]
  },
  {
    "id": "ambiguous-tone",
    "prompt": "I need a greeting for a message.",
    "expected_output": "Asks clarifying questions about the audience, medium, and desired tone",
    "assertions": [
      "does not assume a tone without context",
      "asks about the audience or medium to narrow down the recommendation"
    ],
    "files": [
      "skills/greeting-style/SKILL.md"
    ]
  },
  {
    "id": "pr-review-greeting",
    "prompt": "How should I start a PR review comment?",
    "expected_output": "Recommends a semi-formal greeting for code review context",
    "assertions": [
      "suggests a semi-formal or professional-but-friendly tone",
      "provides a concrete example suitable for a PR comment"
    ],
    "files": [
      "skills/greeting-style/SKILL.md"
    ]
  }
]
```

Each eval has a unique `id`, a `prompt` the user might type, an `expected_output` summary,
and `assertions` that can be verified against the agent's response.

## Step 5: Validate the skill

Run the test command to check that your skill passes all structural validations:

```bash
just test-skill greeting-style
```

The output should end with:

```text
✅ Skill greeting-style is valid and ready
```

If validation fails, read the error messages -- they reference the
[Agent Skills specification](https://agentskills.io/specification) and tell you exactly
what to fix.

## Step 6: Run all checks

Before committing, run the full check suite to make sure nothing else is broken:

```bash
just check
```

All checks should pass. If markdown linting fails, run `just lint-fix` and check again.

## What you have built

You now have a complete agent skill with:

- **`SKILL.md`** -- frontmatter with name and description, plus structured documentation
  that guides agents through decision-making
- **`evals/evals.json`** -- test scenarios that define expected behavior for common,
  boundary, and ambiguous cases

## Next steps

- Read the [Skill Specification Reference](reference-skill-spec.md) for the full list
  of frontmatter fields and directory conventions
- Review existing skills in `skills/` for more complex examples (decision trees,
  reference subdirectories, helper scripts)
- Read [CONTRIBUTING.md](../CONTRIBUTING.md) for the pull request and commit process
- Test your skill locally:

  ```bash
  npx skills add /path/to/agent-skills/skills/greeting-style
  ```
