# Contributing to Agent Skills

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Getting Started

1. **Fork and clone the repository**

   ```bash
   git clone https://github.com/rlespinasse/agent-skills.git
   cd agent-skills
   ```

2. **Install prerequisites**

   - [just](https://github.com/casey/just) - Command runner
   - [Node.js](https://nodejs.org/) (LTS) - For npm dependencies

3. **Install dependencies**

   ```bash
   just install
   ```

4. **Verify everything works**

   ```bash
   just check
   ```

## Development Workflow

### Creating a New Skill

```bash
# Create skill boilerplate
just new-skill my-skill-name

# Edit the SKILL.md file
# Add comprehensive documentation

# Validate the skill
just validate

# Update README
just update-readme
```

### Making Changes

1. Create a new branch

   ```bash
   git checkout -b feat/my-feature
   ```

2. Make your changes

3. Run checks

   ```bash
   just check          # Run all checks
   just lint-fix       # Auto-fix formatting issues
   ```

4. Commit with Conventional Commits format

   ```bash
   git add .
   git commit -m "feat(skill): add new terraform-tools skill"
   ```

## Commit Message Guidelines

This project uses [Conventional Commits](https://www.conventionalcommits.org/) for automated releases.

### Format

```text
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

### Types

- **feat**: New feature or skill (triggers minor release)
- **fix**: Bug fix (triggers patch release)
- **docs**: Documentation only changes
- **style**: Code style changes (formatting, missing semicolons, etc.)
- **refactor**: Code change that neither fixes a bug nor adds a feature
- **perf**: Performance improvement
- **test**: Adding missing tests or correcting existing tests
- **build**: Changes to build system or dependencies
- **ci**: CI configuration changes
- **chore**: Other changes that don't modify src or test files

### Scopes

- **skill**: Changes to a skill
- **readme**: Changes to README
- **justfile**: Changes to justfile
- **ci**: Changes to CI/CD
- **deps**: Dependency updates

### Examples

```bash
# Adding a new skill
feat(skill): add kubernetes-tools skill

# Fixing a bug
fix(drawio): correct installation command in documentation

# Updating documentation
docs(readme): add troubleshooting section

# Refactoring
refactor(justfile): simplify validation logic

# Breaking change
feat(skill)!: redesign SKILL.md frontmatter structure

BREAKING CHANGE: All skills now require a 'category' field in frontmatter
```

### Validate Your Commit Message

```bash
just validate-commit "feat(skill): add new skill"
```

## Code Quality

### Before Committing

Run the pre-commit checks:

```bash
just pre-commit
```

This will:

- Lint all markdown files
- Validate skill structure
- Ensure everything passes

### Continuous Integration

All pull requests are automatically tested via GitHub Actions:

- Markdown linting
- Skill validation
- Commit message format validation

## Skill Documentation Guidelines

### SKILL.md Structure

Each skill must have a `SKILL.md` file with:

1. **YAML Frontmatter** (required)

   ```yaml
   ---
   name: skill-name
   description: Brief description of what the skill does and when to use it
   ---
   ```

2. **Main heading**: Clear title for the skill

3. **Introduction**: Brief overview and context

4. **Decision trees**: Help agents choose between options

5. **Quick reference**: Common patterns and examples

6. **Detailed documentation**: Comprehensive information

7. **Examples**: Real-world usage scenarios

### Best Practices

- Write for AI agents, not just humans
- Include decision logic (when to use X vs Y)
- Provide concrete examples
- Link to authoritative documentation
- Clarify official vs third-party tools
- Keep descriptions concise in frontmatter
- Use clear, scannable headings

## Pull Request Process

1. **Create a pull request** against the `main` branch

2. **Describe your changes**
   - What does this PR do?
   - Why is this change needed?
   - How has it been tested?

3. **Ensure CI passes**
   - All checks must pass
   - Address any review comments

4. **Merge**
   - Maintainers will merge after approval
   - semantic-release will automatically create a release

## Release Process

Releases are fully automated with a two-stage workflow:

### Stage 1: CI Workflow (Quality Gate)

When code is pushed to `main`:

1. **CI workflow runs automatically**
   - Markdown linting
   - Skill structure validation
   - All tests

### Stage 2: Release Workflow (Automated Release)

**Only triggered if CI passes:**

1. **Release workflow automatically runs**
   - Analyzes commit messages
   - Determines version bump
   - Generates CHANGELOG.md
   - Creates GitHub release
   - Publishes to npm

**Important:** The release workflow is triggered by the CI workflow completing successfully. If CI fails,
no release occurs. This two-stage approach ensures quality and prevents broken releases.

You don't need to manually version or release!

## Questions or Issues?

- Check existing [issues](https://github.com/rlespinasse/agent-skills/issues)
- Read [CLAUDE.md](CLAUDE.md) for detailed guidelines
- Review the [Agent Skills specification](https://agentskills.io/specification)
- Open a new issue if you need help

## Code of Conduct

Be respectful and constructive in all interactions. We're here to build helpful tools for the community.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
