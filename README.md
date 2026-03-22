# Agent Skills by @rlespinasse

A collection of [Agent Skills](https://agentskills.io/) for AI coding assistants.

## Available Skills

### claude-code-usage-report

Generates a token usage and cost estimation report for Claude Code sessions.  Analyzes local session JSONL files to
report per-model token consumption, API-equivalent  costs, and per-project breakdowns. Use when user mentions token
usage, cost report,  spending, usage report, session stats, or how much Claude Code costs. Supports filtering  by date
range, project, or plan type.

### conventional-commit

Guides committing staged (indexed) git files using the Conventional Commits specification  and commit message best
practices. Use when user mentions commit, git commit, conventional commit,  commit message, staged files, or indexed
files. Helps craft well-structured, meaningful commit messages.

### diataxis

Helps maintain documentation pages based on the Diataxis method. Analyzes existing docs, classifies pages into
tutorials/how-to/explanation/reference categories, identifies gaps, and helps create or restructure documentation
following Diataxis principles. Use when user mentions documentation structure, Diataxis, doc categories, tutorials vs
how-to guides, or reorganizing docs.

### drawio-export-tools

Decision guide for the third-party Draw.io export ecosystem by @rlespinasse. Covers docker-drawio-desktop-headless
(base Docker), drawio-exporter (Rust backend), drawio-export (enhanced Docker), and drawio-export-action (GitHub
Actions). Use when user mentions diagram export, CI/CD automation, batch processing, or Draw.io files. Helps select the
right tool based on context.

### french-language

Ensures all project content is written in proper French with correct accents, grammar,  and typography. Use when user
mentions french, français, langue française, accents, orthographe,  typographie, or when working on a project that
requires French language content. Also use when  generating any text-based file (SVG, Mermaid, PlantUML, Draw.io, HTML,
CSV, JSON, YAML, etc.)  in a French-language project. Helps enforce French writing conventions across all file types.

### local-branches-status

Reports the status of all local git branches with remote sync state, main branch diff,  worktree path, last activity
date, and content description. Use when user mentions branch status,  branch overview, local branches, branch report,
or branch summary. Helps understand the state of  all branches at a glance.

### pin-github-actions

Migrates GitHub Actions workflows to use pinned commit SHAs instead of  tags, resolves the latest release versions,
flags major version jumps, and configures  Dependabot with grouped updates. Use when user mentions pin actions, pinned
versions,  SHA pinning, GitHub Actions security, dependabot setup, or supply-chain security.

### verify-pr-logs

Checks GitHub Actions CI logs on a pull request, diagnoses failures,  and guides the agent to implement fixes. Use when
user mentions CI failing, check  PR logs, fix pipeline, GitHub Actions errors, workflow failures, build broken, tests
failing on PR, or debug CI. Focuses on PR-scoped CI analysis only.

### verify-readme-features

Verifies that features listed in a README (or similar documentation) are actually  implemented in the codebase. Use
when user mentions verify features, check feature list,  confirm README, validate documentation claims, or audit
feature accuracy.  Helps catch stale, missing, or inaccurate feature descriptions.

## Installation

### Via npx (recommended)

Install all skills:

```bash
npx skills add rlespinasse/agent-skills
```

Install specific skill:

```bash
npx skills add rlespinasse/agent-skills/drawio-export-tools
```

### Via Claude Code plugin

This repository includes a `.claude-plugin/marketplace.json` manifest for Claude Code plugin installation:

```bash
/plugin marketplace add rlespinasse/agent-skills
/plugin install drawio-export-tools
```

## Supported Agents

These skills work with:

- Claude Code
- Cursor
- VS Code
- GitHub Copilot
- Gemini CLI
- And 30+ other AI coding assistants

## Related Projects

- [docker-drawio-desktop-headless](https://github.com/rlespinasse/docker-drawio-desktop-headless) - Base Docker image
- [drawio-exporter](https://github.com/rlespinasse/drawio-exporter) - Rust backend
- [drawio-export](https://github.com/rlespinasse/drawio-export) - Enhanced Docker wrapper
- [drawio-export-action](https://github.com/rlespinasse/drawio-export-action) - GitHub Action

## About

Author: [@rlespinasse](https://github.com/rlespinasse)

These skills follow the [Agent Skills specification](https://agentskills.io/specification)
and are designed to help AI agents effectively use the Draw.io export ecosystem.

## Contributing

Contributions are welcome! See the [Contributing Guidelines](CONTRIBUTING.md) for full details, and the
[Skill Specification Reference](docs/reference-skill-spec.md) for frontmatter and evals requirements.

### Quick Start for Contributors

```bash
# Create a new skill
just new-skill my-skill-name

# Validate and test
just check

# Commit with conventional format
git commit -m "feat(skill): add my-skill-name"
```

## License

MIT License - see [LICENSE](LICENSE) file for details.
