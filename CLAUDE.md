# Claude Instructions for Agent Skills Repository

This repository contains [Agent Skills](https://agentskills.io/) for AI coding assistants.

## Project Overview

**Purpose**: A curated collection of agent skills that help AI assistants effectively use specific tools and ecosystems.

**Author**: [@rlespinasse](https://github.com/rlespinasse)

**Target Audience**: AI coding assistants (Claude Code, Cursor, VS Code Copilot, etc.)

## Repository Structure

```text
agent-skills/
├── README.md              # Main repository documentation
├── LICENSE                # MIT License
├── justfile               # Development task automation
├── .markdownlint.json     # Markdown linting configuration
└── {skill-name}/          # Individual skill directories
    └── SKILL.md           # Skill specification and documentation
```

## Agent Skills Specification

All skills MUST follow the [Agent Skills specification](https://agentskills.io/specification):

### Required Structure

1. **Directory name**: kebab-case skill name (e.g., `drawio-export-tools`)
2. **SKILL.md file**: Must contain:
   - YAML frontmatter with `name` and `description` fields
   - Comprehensive skill documentation
   - Clear usage guidelines

### SKILL.md Template

```yaml
---
name: skill-name
description: Brief description (1-2 sentences) that helps agents understand when to activate this skill
---

# Skill Title

[Detailed documentation goes here]
```

## Development Guidelines

### Creating New Skills

1. **Use the justfile**: `just new-skill skill-name`
2. **Follow naming conventions**: Use kebab-case
3. **Write clear descriptions**: The frontmatter `description` is crucial for skill activation
4. **Include examples**: Show practical usage patterns
5. **Document edge cases**: Help agents make correct decisions

### Skill Content Best Practices

- **Start with context**: Explain what the skill covers
- **Include decision trees**: Help agents choose between options
- **Provide quick references**: Make common tasks easy to find
- **Add disclaimers**: Clarify third-party vs official tools
- **Link to documentation**: Reference authoritative sources
- **Use clear headings**: Make content scannable

### Code Style

- **Markdown**: Follow .markdownlint.json rules
  - Max line length: 120 characters
  - Code blocks and tables exempt from line length
  - HTML allowed (MD033: false)
  - First line heading not required (MD041: false)
- **YAML frontmatter**: Always include name and description
- **Code examples**: Use appropriate syntax highlighting

### Testing

Before committing:

1. Run `just check` - Validates markdown and skill structure
2. Run `just lint-fix` - Auto-fix formatting issues
3. Manually test skill installation: `npx skills add rlespinasse/agent-skills/skill-name`

## Common Tasks

Use the justfile for all development tasks:

```bash
just                    # List all available commands
just new-skill name     # Create a new skill
just lint               # Check markdown formatting
just lint-fix           # Auto-fix markdown issues
just validate           # Validate skill structure
just check              # Run all checks
just list-skills        # List all available skills
just pre-commit         # Run before committing
```

## Git Workflow

### Commits

**IMPORTANT**: This project uses [Conventional Commits](https://www.conventionalcommits.org/) and automated releases.

**Required format:**

```text
<type>(<scope>): <subject>
```

**Valid types:**

- `feat`: New feature or skill (triggers minor release)
- `fix`: Bug fix (triggers patch release)
- `build`: Build system changes (triggers patch release)
- `docs`: Documentation changes
- `style`: Code style changes (triggers patch release)
- `refactor`: Code refactoring (triggers patch release)
- `test`: Adding or updating tests
- `chore`: Maintenance tasks
- `ci`: CI/CD changes
- `perf`: Performance improvements

**Examples:**

```bash
feat(skill): add terraform-tools skill
fix(drawio): correct installation command in README
docs(readme): update contributing section
chore(deps): update markdownlint-cli to v0.43.0
```

**Breaking changes:**

```bash
feat(skill)!: redesign SKILL.md frontmatter structure

BREAKING CHANGE: frontmatter now requires 'category' field
```

**Validate your commit message before committing:**

```bash
just validate-commit "feat(skill): add new skill"
```

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

### For Skill Authors

- **Think like an agent**: What context would you need to make good decisions?
- **Be explicit**: Don't assume domain knowledge
- **Provide alternatives**: Show multiple approaches when applicable
- **Include anti-patterns**: Help agents avoid common mistakes
- **Attribution matters**: Always credit tool authors and clarify official vs. third-party

### For Skill Content

- **Decision trees first**: Start with "when to use this" logic
- **Quick reference second**: Common patterns for copy-paste
- **Details last**: Comprehensive options and edge cases
- **Examples throughout**: Show, don't just tell

## File Organization

```text
skill-name/
├── SKILL.md           # Required: Main skill documentation
├── examples/          # Optional: Example files
└── assets/            # Optional: Images, diagrams, etc.
```

Currently, we keep skills simple with just SKILL.md, but subdirectories are allowed if needed.

## Releases

### Automated Releases

This project uses [semantic-release](https://semantic-release.gitbook.io/) for automated versioning and releases.

**How it works:**

1. When commits are pushed to `main`, **CI workflow** triggers automatically:
   - Linting checks
   - Skill structure validation
   - All tests must pass
2. **If CI succeeds**, the **Release workflow** is automatically triggered:
   - Analyzes commit messages
   - Determines next version number:
     - `fix`: patch version (0.0.x)
     - `feat`: minor version (0.x.0)
     - `BREAKING CHANGE`: major version (x.0.0)
   - Generates CHANGELOG.md
   - Creates GitHub release with release notes
   - Publishes to npm registry
3. **If CI fails**, release workflow is skipped and no release occurs

**Testing releases locally:**

```bash
just release-dry-run  # See what would be released without actually releasing
```

### Release Process

**For maintainers:**

1. Ensure all commits follow Conventional Commits format
2. Merge PR to `main` branch
3. GitHub Actions automatically handles the release
4. Check GitHub Releases and npm for published version

**Manual verification:**

```bash
npm run test          # Run all checks
just validate-commit "feat: example message"  # Validate commit format
```

## Maintenance

### Regular Tasks

- Review and update skills as tools evolve
- Check for broken links in documentation
- Update examples to match current tool versions
- Respond to issues and PRs promptly

### Version Management

- Versions are managed automatically by semantic-release
- CHANGELOG.md is automatically generated and updated
- GitHub releases are created automatically
- npm package is published automatically

## Resources

- [Agent Skills Specification](https://agentskills.io/specification)
- [Agent Skills Directory](https://agentskills.io/)
- [Just Command Runner](https://github.com/casey/just)
- [Markdownlint](https://github.com/DavidAnson/markdownlint)

## Questions or Issues?

- Check existing skills for examples
- Review the Agent Skills specification
- Open an issue for clarification
- Refer to justfile for development commands

## Attribution

When working with this repository:

- Respect existing skill authorship
- Credit tool creators in skill documentation
- Clarify official vs. community/third-party tools
- Link to authoritative documentation

---

**Remember**: Skills are used by AI agents to help developers. Write clear, actionable content that helps
agents make good decisions in context.
