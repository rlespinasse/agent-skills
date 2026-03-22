# Claude Instructions for Agent Skills Repository

This repository contains [Agent Skills](https://agentskills.io/) for AI coding assistants.

## Project Overview

**Purpose**: A curated collection of agent skills that help AI assistants effectively use specific tools and ecosystems.

**Author**: [@rlespinasse](https://github.com/rlespinasse)

**Target Audience**: AI coding assistants (Claude Code, Cursor, VS Code Copilot, etc.)

## Repository Structure

```text
agent-skills/
├── README.md              # Main repository documentation (auto-generated skills section)
├── CONTRIBUTING.md        # Contributing guidelines
├── LICENSE                # MIT License
├── justfile               # Development task automation
├── .markdownlint.json     # Markdown linting configuration
├── .claude-plugin/
│   └── marketplace.json   # Claude Code plugin manifest (auto-generated)
├── docs/
│   └── reference-skill-spec.md    # Skill specification reference
└── skills/{skill-name}/   # Individual skill directories
    ├── SKILL.md           # Skill specification and documentation
    └── evals/
        └── evals.json     # Skill test scenarios
```

## Agent Skills Specification

All skills MUST follow the [Agent Skills specification](https://agentskills.io/specification). Each skill is a
kebab-case directory with a `SKILL.md` file containing YAML frontmatter (`name` and `description`) and
structured documentation.

See [Skill Specification Reference](docs/reference-skill-spec.md) for frontmatter requirements, directory
structure, evals schema, and description patterns.

## Development Guidelines

### Creating New Skills

1. **Use the justfile**: `just new-skill skill-name`
2. **Follow naming conventions**: Use kebab-case
3. **Write clear descriptions**: The frontmatter `description` is crucial for skill activation
4. **Include examples**: Show practical usage patterns
5. **Document edge cases**: Help agents make correct decisions

### Testing

Before committing:

1. Run `just autofix` - Formats, syncs generated files, fixes linting, and runs all checks
2. Manually test skill installation: `npx skills add rlespinasse/agent-skills/skill-name`

Generated files and formatting are automatically fixed by the autofix workflow on same-repo PRs.

Run `just` with no arguments to list all available commands.

## Git Workflow

### Commits

**IMPORTANT**: This project uses [Conventional Commits](https://www.conventionalcommits.org/) and automated
releases. An autofix workflow on PRs automatically syncs generated files (`README.md`, `marketplace.json`),
formats the justfile, and fixes markdown formatting. See [Commit Message Guidelines](CONTRIBUTING.md#making-changes)
for format and validation.

### Branches

- `main` - Production-ready code
- Feature branches for new skills or significant changes
- Use descriptive branch names: `feature/new-skill-name`

### Pull Requests

When creating PRs:

- Ensure all checks pass (`just check`)
- Update README.md if adding new skills
- Include examples of skill usage
- Mention any related issues

## Important Constraints

### What to Avoid

1. **Don't modify .markdownlint.json** without discussion
2. **Don't skip validation** - Always run `just validate` before committing
3. **Don't create skills without SKILL.md** - It's required by the spec
4. **Don't use camelCase or snake_case** for skill names - Use kebab-case
5. **Don't make skills too broad** - Each skill should have a focused purpose

### Quality Standards

- All markdown files must pass linting
- All skills must validate successfully
- SKILL.md frontmatter must be valid YAML
- Descriptions must be concise but informative
- Code examples must be tested and accurate

## Skill Categories

Current categories (expand as needed):

- **Tool Ecosystems**: Guide agents through related tool choices (e.g., drawio-export-tools)
- **Workflow Patterns**: Common development workflows
- **Decision Guides**: Help agents make context-appropriate choices

## Documentation Philosophy

- **Think like an agent**: What context would you need to make good decisions?
- **Be explicit**: Don't assume domain knowledge
- **Include anti-patterns**: Help agents avoid common mistakes
- **Attribution matters**: Always credit tool authors and clarify official vs. third-party

See [Writing Style](CONTRIBUTING.md#writing-style) for content structure and formatting guidelines.

## Releases

Releases are fully automated. When commits are pushed to `main`, CI runs checks and — if they pass — triggers
semantic-release to version, generate CHANGELOG.md, and create a GitHub release.

See the [Release Process](CONTRIBUTING.md#release-process) in CONTRIBUTING.md for details.

## Maintenance

- Review and update skills as tools evolve
- Check for broken links in documentation
- Update examples to match current tool versions
- Respond to issues and PRs promptly

## Resources

- [Skill Specification Reference](docs/reference-skill-spec.md)
- [Contributing Guidelines](CONTRIBUTING.md)
- [Agent Skills Specification](https://agentskills.io/specification)
- [Agent Skills Directory](https://agentskills.io/)
- [Just Command Runner](https://github.com/casey/just)
- [Markdownlint](https://github.com/DavidAnson/markdownlint)

## Attribution

When working with this repository:

- Respect existing skill authorship
- Credit tool creators in skill documentation
- Clarify official vs. community/third-party tools
- Link to authoritative documentation

---

**Remember**: Skills are used by AI agents to help developers. Write clear, actionable content that helps
agents make good decisions in context.
