---
name: drawio-export-tools
description: Decision guide for the third-party Draw.io export ecosystem by @rlespinasse. Covers
  docker-drawio-desktop-headless (base Docker), drawio-exporter (Rust backend), drawio-export
  (enhanced Docker), and drawio-export-action (GitHub Actions). Use when user mentions diagram
  export, CI/CD automation, batch processing, or Draw.io files. Helps select the right tool based on
  context. For pinning the export action in workflows, see pin-github-actions.
---

# Draw.io Export Tools - Optimized Decision Guide

**Third-party ecosystem by [@rlespinasse](https://github.com/rlespinasse) - NOT official Draw.io**

## Response Strategy

**ALWAYS start with context questions, then provide ONLY relevant section.**

### Initial Response Pattern

```text
1. Ask 2-3 targeted questions
2. Provide solution for their specific case (300-500 tokens)
3. Offer: "Need details on [X/Y/Z]? Just ask."
```

**DO NOT dump all options unless explicitly requested.**

---

## Quick Decision Flow (USE THIS FIRST)

Ask these questions in order:

**Q1: "Where are you exporting diagrams?"**

- GitHub Actions → Provide: [GitHub Action Section]
- Local/Scripts → Continue to Q2
- Other CI/CD → Provide: [Docker Export Section]

**Q2: "What's your goal?"** (if not GitHub Actions)

- Simple one-off export → Provide: [Base Docker Section]
- Batch with custom output layout → Provide: [Docker Export Section]
- Custom processing pipeline → Provide: [Advanced Section]
- Building a tool → Provide: [Advanced Section] (Rust library part)

**Q3: "Any special requirements?"** (if relevant)

- Output layout → Add: output folder and output mode
- Specific pages → Add: page options
- Pre/post processing → Add: scripting examples

---

## Tool Quick Reference (Keep This Loaded)

| Use Case       | Tool                             | One-Liner                                   |
| -------------- | -------------------------------- | ------------------------------------------- |
| GitHub Actions | `drawio-export-action`           | `uses: rlespinasse/drawio-export-action@v2` |
| Custom output  | `drawio-export`                  | `--output exports --output-mode absolute`   |
| Simple export  | `docker-drawio-desktop-headless` | `-x diagram.drawio -f pdf`                  |
| Custom tool    | `drawio-exporter`                | Rust library                                |

**Docs:** All tools at <https://github.com/rlespinasse/>

---

## Response Sections (Provide On-Demand)

### [GitHub Action Section]

**When to provide:** User mentions GitHub Actions, CI/CD, or automated commits

```yaml
- uses: rlespinasse/drawio-export-action@v2
  with:
    format: pdf,png,svg
    path: .
```

**Common options:** `format`, `path`, `output`, `transparent`, `scale`, `action-mode`

The action has no `output-mode` input: exports always go to the `output` folder next to each
source file (relative mode). For a single output tree, use `drawio-export` with `--output-mode absolute`.

**Offer:** "Need a custom output folder, specific pages, or workflow setup? Let me know."

**Full docs:** <https://github.com/rlespinasse/drawio-export-action>

---

### [Docker Export Section]

**When to provide:** User needs custom output structure, batch exports, or organized files

```bash
docker run -v $(pwd):/data rlespinasse/drawio-export \
  --format pdf \
  --output dist \
  --output-mode absolute \
  diagrams/
```

**Output options** (from the `drawio-exporter` CLI, which `drawio-export` wraps):

- `-f, --format` - adoc, md, jpg, pdf, png, svg, xml (default `pdf`)
- `-o, --output <folder>` - exported folder name (default `export`)
- `--output-mode relative|absolute` - `relative` (default) exports next to each source file;
  `absolute` exports under a single output folder mirroring the source tree
- `--remove-page-suffix` - drop the page suffix for single-page files
- `--on-changes` - export only files newer than their exports (`--git-ref <ref>` limits to files changed since a git reference)

**Offer:** "Need more output layout examples or CLI options?"

**Full docs:** <https://github.com/rlespinasse/drawio-export>

---

### [Base Docker Section]

**When to provide:** Simple one-off export, validation, or full CLI control

```bash
docker run -v $(pwd):/data -w /data \
  rlespinasse/drawio-desktop-headless \
  -x diagram.drawio -f pdf
```

**Essential options:**

- `-f <format>` - pdf, png, svg, jpg
- `-o <output>` - custom filename
- `-t` - transparent PNG
- `--scale <n>` - resolution
- `-a` - all pages
- `--check` - validate only

**Image variants:** `latest` (full, Unicode and CJK fonts) is the default. Use the `minimal` tag
(`rlespinasse/drawio-desktop-headless:minimal`) for Western fonts only and a much smaller image.

**Offer:** "Need batch export, page selection, or error handling?"

**Full docs:** <https://github.com/rlespinasse/docker-drawio-desktop-headless>

---

### [Advanced Section]

**When to provide:** User needs custom processing, pre/post hooks, or pipeline integration
or wants to build a custom tool with the Rust `drawio-exporter` library.

Read [references/advanced-and-rust.md](references/advanced-and-rust.md) and offer: "What specific processing do you need?"

---

## Detailed Options (Provide ONLY When Asked)

- Complete CLI flags or GitHub Action inputs: read [references/full-options.md](references/full-options.md)
- Permission errors, timeouts, debug mode: read [references/troubleshooting.md](references/troubleshooting.md)

---

## Response Examples

### Example 1: User says "export diagrams in GitHub Actions"

**Response:**

```text
Use drawio-export-action:

[GitHub Action Section - 150 tokens]

Need custom naming or multi-format exports? Let me know.
```

### Example 2: User says "batch export with custom names"

**Response:**

```text
Use drawio-export with --output and --output-mode:

[Docker Export Section - 200 tokens]
[Show 2-3 common patterns]

Need more examples or other options?
```

### Example 3: User says "I need custom processing during export"

**Response:**

```text
First, let me understand:
1. What custom processing? (watermarks, metadata, transformations?)
2. Before export, during, or after?
3. GitHub Actions or local?

Then provide: [Advanced Section] tailored to their answer
```

### Example 4: User asks comprehensive question

**If user asks: "what can I customize?"**

**Response:**

```text
Depends on your use case. Are you:
1. Using GitHub Actions? → [show action options]
2. Need a custom output layout? → [show output options]
3. Need custom processing? → [show advanced]

Or would you like a full overview? (This will be comprehensive)
```

**Only if they confirm "full overview" → provide all sections**

---

## Key Principles

1. **Ask first, provide second** - 2-3 questions before solutions
2. **Targeted responses** - Only relevant section (200-500 tokens)
3. **Progressive disclosure** - Offer more details, don't assume
4. **Validate before executing** - Confirm understanding before running commands
5. **No unsolicited extras** - Only create files if explicitly requested

## Token Budget Guidelines

- Initial response: 200-400 tokens (questions + context)
- Targeted solution: 300-500 tokens (one section + examples)
- Comprehensive (if requested): 1500-2000 tokens (multiple sections)
- Default to smallest appropriate response

---

## Conversation Flow Template

```text
User: [mentions draw.io export]

Claude:
1. Acknowledge + quick context
2. Ask 2-3 targeted questions
3. [Wait for answer]

User: [provides context]

Claude:
1. Provide ONLY relevant section (300-500 tokens)
2. Include 1-2 practical examples
3. Offer: "Need [other option]? Just ask."
4. If executing commands: confirm understanding first

User: [follow-up or clarification]

Claude:
1. Provide additional requested details
2. Or adjust solution based on clarification
3. Still keep focused on their specific need
```

---

## When User Asks Broad Questions

**"What can I do?" / "How do I customize?" / "What are my options?"**

**Response pattern:**

```text
There are several approaches depending on your need:

[Quick reference table - 100 tokens]

What's your specific use case?
1. [Most common scenario]
2. [Second most common]
3. [Something else]

I'll provide the exact solution once I understand your goal.
```

**Do NOT provide all 4 levels immediately**

---

## Success Metrics

**Efficient conversation:**

- 2-4 turns to solution
- 500-1000 tokens per response
- 0 rejected commands
- 0 unsolicited file creation

**Less efficient (avoid):**

- 5+ turns to solution
- 2000+ tokens per response
- Trial-and-error commands
- Creating files user didn't ask for
