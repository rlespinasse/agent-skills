# Agent Skills by @rlespinasse

A collection of [Agent Skills](https://agentskills.io/) for AI coding assistants.

## Available Skills

### drawio-export-tools

Decision guide for the third-party Draw.io export ecosystem by @rlespinasse. Covers docker-drawio-desktop-headless
(base Docker), drawio-exporter (Rust backend), drawio-export (enhanced Docker), and drawio-export-action (GitHub
Actions). Use when user mentions diagram export, CI/CD automation, batch processing, or Draw.io files. Helps select the
right tool based on context.

## Installation

Install all skills:

```bash
npx skills add rlespinasse/agent-skills
```

Install specific skill:

```bash
npx skills add rlespinasse/agent-skills/drawio-export-tools
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

More skills coming soon! Watch this repository for updates.

## License

MIT License - see [LICENSE](LICENSE) file for details.
