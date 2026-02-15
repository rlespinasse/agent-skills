---
name: drawio-export-tools
description: Decision guide for the third-party Draw.io export ecosystem by @rlespinasse. Covers docker-drawio-desktop-headless (base Docker), drawio-exporter (Rust backend), drawio-export (enhanced Docker), and drawio-export-action (GitHub Actions). Use when user mentions diagram export, CI/CD automation, batch processing, or Draw.io files. Helps select the right tool based on context.
---

# Draw.io Export Tools - Decision Guide

A unified skill covering the **third-party Draw.io export ecosystem created by GitHub user [@rlespinasse](https://github.com/rlespinasse)**.

**Important:** These tools are NOT official Draw.io products. They are
community-developed tools that wrap and enhance Draw.io Desktop's CLI for
automation purposes.

**Start by understanding user context, then recommend the right tool.**

## Decision Tree (START HERE)

Ask these questions to guide tool selection:

### 1. Are you using GitHub Actions?

**YES** → Use **`drawio-export-action`**
**NO** → Continue to #2

### 2. Do you need enhanced features?

(Custom output structure, organized exports, advanced options)
**YES** → Use **`drawio-export`**
**NO** → Continue to #3

### 3. Is this a simple one-off export?

**YES** → Use **`docker-drawio-desktop-headless`**
**NO** → Continue to #4

### 4. Are you building a custom tool?

**YES** → Use **`drawio-exporter`** (Rust backend)
**NO** → Start with `docker-drawio-desktop-headless`

## Ecosystem Overview

**Creator:** All tools below are created and maintained by [@rlespinasse](https://github.com/rlespinasse)

```text
┌─────────────────────────────────────────┐
│ docker-drawio-desktop-headless          │  ← Foundation (by rlespinasse)
│ Base Docker image with headless Draw.io │
└────────────────┬────────────────────────┘
                 │
                 ├─→ Direct use (simple exports)
                 │
                 ↓
┌─────────────────────────────────────────┐
│ drawio-exporter                         │  ← Rust backend (by rlespinasse)
│ Enhanced export logic and features      │
└────────────────┬────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────┐
│ drawio-export                           │  ← Enhanced Docker (by rlespinasse)
│ User-friendly wrapper with organization │
└────────────────┬────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────┐
│ drawio-export-action                    │  ← GitHub Action (by rlespinasse)
│ CI/CD integration                       │
└─────────────────────────────────────────┘
```

**Key Principle:** Use the highest appropriate level. Don't use low-level tools
when high-level ones fit.

**Attribution:** These are third-party community tools, not official Draw.io
products. They leverage Draw.io Desktop's CLI capabilities for automation.

## Tool Quick Reference

### 1. drawio-export-action (GitHub Actions)

**When to use:**

- Exporting diagrams in GitHub Actions workflows
- Automated diagram processing on commits/PRs
- CI/CD integration

**Quick pattern:**

```yaml
- uses: rlespinasse/drawio-export-action@v2
  with:
    format: pdf
    path: diagrams/
```

**Docs:** <https://github.com/rlespinasse/drawio-export-action>

---

### 2. drawio-export (Enhanced Docker)

**When to use:**

- Batch exports with custom output organization
- Need to control output directory structure
- Advanced export configurations
- Local automation scripts

**Quick pattern:**

```bash
docker run -v $(pwd):/data rlespinasse/drawio-export \
  --format pdf --output exports/ diagrams/
```

**Key features:**

- Output organization control
- Multiple format support
- Built on drawio-exporter (Rust backend)

**Docs:** <https://github.com/rlespinasse/drawio-export>

---

### 3. docker-drawio-desktop-headless (Base Docker)

**When to use:**

- Simple one-off exports
- Direct control over Draw.io CLI
- Custom scripts where you control everything
- Testing or debugging

**Quick patterns:**

Export to PDF:

```bash
docker run -v $(pwd):/data -w /data \
  rlespinasse/drawio-desktop-headless -x diagram.drawio -f pdf
```

Batch export:

```bash
docker run -v $(pwd):/data -w /data \
  rlespinasse/drawio-desktop-headless -x -r -f pdf diagrams/
```

Validate:

```bash
docker run -v $(pwd):/data -w /data \
  rlespinasse/drawio-desktop-headless --check diagram.drawio
```

**Common options:**

- `-x` - Export, `-f <format>` - pdf/png/svg/jpg
- `-r` - Recursive, `-t` - Transparent (PNG)
- `-a` - All pages, `-p <n>` - Specific page
- `--scale <n>` - Scale, `--border <n>` - Border
- `--check` - Validate only

**Timeout handling:**

```bash
docker run -e DRAWIO_DESKTOP_COMMAND_TIMEOUT=30s \
  -v $(pwd):/data -w /data \
  rlespinasse/drawio-desktop-headless -x large.drawio
```

**Docs:** <https://github.com/rlespinasse/docker-drawio-desktop-headless>

---

### 4. drawio-exporter (Rust Backend)

**When to use:**

- Building custom export tools
- Need Rust library integration
- Extending functionality programmatically

**Note:** This is a backend component. Most users should use drawio-export (Docker wrapper) instead.

**Docs:** <https://github.com/rlespinasse/drawio-exporter>

## Common Workflows

### Workflow 1: "Export diagrams in my CI/CD"

→ **Use drawio-export-action**

```yaml
name: Export Diagrams
on: [push]
jobs:
  export:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: rlespinasse/drawio-export-action@v2
        with:
          format: pdf
          path: docs/diagrams/
```

### Workflow 2: "Batch export with organized output"

→ **Use drawio-export**

```bash
docker run -v $(pwd):/data rlespinasse/drawio-export \
  --format pdf,png \
  --output exports/{folder}/{basename}-{format}.{ext} \
  diagrams/
```

### Workflow 3: "Quick export one diagram"

→ **Use docker-drawio-desktop-headless**

```bash
docker run -v $(pwd):/data -w /data \
  rlespinasse/drawio-desktop-headless -x architecture.drawio -f pdf
```

### Workflow 4: "Validate all diagrams"

→ **Use docker-drawio-desktop-headless**

```bash
for file in diagrams/*.drawio; do
  docker run -v $(pwd):/data -w /data \
    rlespinasse/drawio-desktop-headless --check "$file"
done
```

## Error Handling

### Permission Errors (non-root user)

```bash
docker run -u $(id -u):$(id -g) -e HOME=/data/home \
  -v /etc/passwd:/etc/passwd -v $(pwd):/data -w /data \
  rlespinasse/drawio-desktop-headless -x diagram.drawio
```

### Timeouts (large diagrams)

```bash
docker run -e DRAWIO_DESKTOP_COMMAND_TIMEOUT=60s \
  -v $(pwd):/data -w /data \
  rlespinasse/drawio-desktop-headless -x large.drawio
```

### Debug Mode

```bash
docker run -e SCRIPT_DEBUG_MODE=true \
  -v $(pwd):/data -w /data \
  rlespinasse/drawio-desktop-headless -x diagram.drawio
```

## Decision Examples

**User says:** "I need to export diagrams in my GitHub Actions workflow"
→ **Recommend:** drawio-export-action
→ **Why:** Built specifically for GitHub Actions, easiest integration

**User says:** "I want to export all diagrams and organize them by type"
→ **Recommend:** drawio-export
→ **Why:** Supports output path templates and organization

**User says:** "I need to quickly export this one diagram to PDF"
→ **Recommend:** docker-drawio-desktop-headless
→ **Why:** Direct, simple, no overhead

**User says:** "I'm building a tool that exports diagrams with custom logic"
→ **Recommend:** drawio-exporter (if Rust) or docker-drawio-desktop-headless (if scripting)
→ **Why:** Low-level access for custom integration

## Important Notes

- **Always start with context questions** before recommending a tool
- **Prefer higher-level tools** (action > export > headless) unless there's a reason to go lower
- **Don't over-engineer:** If base Docker works, don't suggest the enhanced version
- **Link to docs:** All tools have comprehensive documentation
- **Test first:** Validate diagrams before batch exporting

## When This Skill Activates

- User mentions Draw.io diagram export
- User asks about diagram automation
- User needs CI/CD diagram processing
- User wants to batch process .drawio files
- User mentions any of the four tool names

## Important Disclaimers

**Always communicate to users:**

1. These are **third-party tools by [@rlespinasse](https://github.com/rlespinasse)**, not official Draw.io products
2. They are **community-maintained** and wrap Draw.io Desktop CLI
3. For official Draw.io support, refer to [diagrams.net](https://www.diagrams.net/) or [Draw.io Desktop](https://github.com/jgraph/drawio-desktop)
4. These tools are **provided as-is** under their respective licenses
