# Contributing to Agent Skills

Thank you for your interest in contributing!

## Getting Started

1. **Fork and clone the repository**

   ```bash
   git clone https://github.com/rlespinasse/agent-skills.git
   cd agent-skills
   ```

2. **Install prerequisites**

   - [just](https://github.com/casey/just) - Command runner
   - [Node.js](https://nodejs.org/) (LTS) - For npx tooling

3. **Set up git hooks**

   ```bash
   just setup
   ```

   This configures `core.hooksPath` to use `.githooks/`, which runs `just sync` and
   `just pre-commit` automatically before every commit.

4. **Verify everything works**

   ```bash
   just check
   ```

## Creating a New Skill

1. Scaffold the skill:

   ```bash
   just new-skill my-skill-name
   ```

   This creates `my-skill-name/SKILL.md` and `my-skill-name/evals/evals.json` with boilerplate.

2. **Write the description** — this is the most important part. It determines when agents activate your skill.
   Include what the skill does, trigger phrases, and scope boundaries:

   ```yaml
   description: Guide for choosing the right testing framework for Node.js projects.
     Use when user mentions unit testing, test runner, Jest, Vitest, or Mocha.
   ```

3. **Write the skill content** — structure it as: decision flow first, quick reference second, details last.
   Keep SKILL.md under 500 lines. See [Skill Specification Reference](docs/reference-skill-spec.md) for
   frontmatter requirements, directory structure, and description patterns.

4. **Write evals** — replace the boilerplate in `evals/evals.json` with real test scenarios. Cover the main
   decision paths (5-7 evals minimum), include a scope boundary test and an ambiguous request test.
   See the [Evals Schema](docs/reference-skill-spec.md#evals-schema) for field definitions.

5. **Commit** (the pre-commit hook runs sync and checks automatically):

   ```bash
   git add skills/my-skill-name/
   git commit -m "feat: add my-skill-name skill"
   ```

## Making Changes

1. Create a branch: `git checkout -b feat/my-feature`
2. Make your changes
3. Commit with [Conventional Commits](https://www.conventionalcommits.org/) format
   (the pre-commit hook syncs generated files, fixes formatting, and runs all checks):
   `<type>(<scope>): <subject>`

   ```bash
   feat(skill): add kubernetes-tools skill
   fix(drawio): correct installation command in documentation
   ```

   Validate: `just validate-commit "feat(skill): add new skill"`

## Maintaining Skills

- **Update a skill**: edit `SKILL.md`, run `just pre-commit`, commit
- **Fix markdown linting**: run `just lint-fix`, then `just lint` for remaining issues
- **Fix generated files out of sync**: run `just sync`
- **Remove a skill**: delete the directory, run `just sync`, commit as breaking change

## Writing Style

- **Structure:** Decision flow first, quick reference second, detailed docs last
- **Tone:** Direct and instructional — write as if briefing an agent. Active voice.
- **Formatting:** Bold key terms on first use. Use code blocks and tables. Lines under 120 characters.
- **Clarity:** Be specific. Include concrete examples. State what the skill does NOT cover.

## Pull Request Process

1. Ensure `just check` passes
2. Describe what, why, and how it was tested
3. Maintainers will merge after approval
4. semantic-release automatically creates a release

## Release Process

Releases are fully automated. When code is pushed to `main`:

1. **CI runs** — linting, validation, all checks
2. **If CI passes** — semantic-release analyzes commits, determines version bump, generates CHANGELOG.md,
   creates GitHub release

You don't need to manually version or release.

## Questions or Issues?

- Read the [Skill Specification Reference](docs/reference-skill-spec.md) for frontmatter, evals, and conventions
- Read [CLAUDE.md](CLAUDE.md) for AI agent guidelines
- Review the [Agent Skills specification](https://agentskills.io/specification)
- Check existing [issues](https://github.com/rlespinasse/agent-skills/issues) or open a new one

## Code of Conduct

Be respectful and constructive in all interactions. We're here to build helpful tools for the community.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
