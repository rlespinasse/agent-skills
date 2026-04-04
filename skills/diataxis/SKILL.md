---
name: diataxis
description: Helps maintain documentation pages based on the Diataxis method. Analyzes existing docs, classifies pages into tutorials/how-to/explanation/reference categories, identifies gaps, and helps create or restructure documentation following Diataxis principles. Use when user mentions documentation structure, Diataxis, doc categories, tutorials vs how-to guides, or reorganizing docs.
---

# Maintain Documentation with the Diataxis Method

You are helping the user organize and maintain their project documentation following the Diataxis framework.

## What is Diataxis?

Diataxis (from Ancient Greek: *dia* — "across", *taxis* — "arrangement") is a systematic
approach to technical documentation that organizes content into four categories based on
user needs. See [diataxis.fr](https://diataxis.fr/) for the full framework.

| Category          | Orientation            | Purpose                                  | Form                |
| ----------------- | ---------------------- | ---------------------------------------- | ------------------- |
| **Tutorials**     | Learning-oriented      | Guide a beginner through learning        | A lesson            |
| **How-to guides** | Task-oriented          | Help accomplish a specific goal          | A series of steps   |
| **Explanation**   | Understanding-oriented | Deepen understanding through discussion  | A discursive essay  |
| **Reference**     | Information-oriented   | Provide precise technical descriptions   | Dry, accurate facts |

### The Compass — Two Axes for Classification

Use two questions to classify any content (see [references/compass.md](references/compass.md)):

| | Acquisition (study) | Application (work) |
| --- | --- | --- |
| **Action** (practical) | Tutorial | How-to guide |
| **Cognition** (theoretical) | Explanation | Reference |

1. **"Is this about action or cognition?"** — Does the reader do something or understand something?
2. **"Is this about acquisition or application?"** — Is the reader studying or working?

### Key Distinctions

- **Tutorials vs How-to guides**: Tutorials teach ("follow me") for learners;
  how-to guides direct ("do this") for practitioners. Tutorials are complete end-to-end;
  how-to guides start and end at reasonable points the reader joins to their own work.
- **Explanation vs Reference**: Explanation discusses why (discursive, admits opinion);
  reference states what (austere, authoritative, no ambiguity).
- **Action vs Cognition**: Tutorials and how-to guides are practical (doing).
  Explanation and reference are theoretical (knowing).
- **Acquisition vs Application**: Tutorials and explanation serve learning/studying.
  How-to guides and reference serve working/coding.

## Step 1: Discover Existing Documentation

1. **Scan the project for documentation files:**
   - Look for `docs/`, `doc/`, `documentation/` directories
   - Check for markdown files at the project root: `README.md`, `CONTRIBUTING.md`, `CHANGELOG.md`
   - Look for other documentation formats: `.rst`, `.adoc`, `.txt`
   - Check for documentation configuration: `mkdocs.yml`, `docusaurus.config.js`, `conf.py`, `antora.yml`, `hugo.toml`

2. **Read existing documentation** to understand what is already covered.

3. **If no documentation exists:**
   - Inform the user: "No documentation found. Let's create a documentation structure from scratch."
   - Skip to [Step 3: Propose Documentation Structure](#step-3-propose-documentation-structure)

## Step 2: Classify Existing Documentation

Analyze each documentation page and classify it into one of the four Diataxis categories.

### Respect Prior Classification Decisions

Before suggesting reclassification, check git history for deliberate prior moves:

```bash
git log --all --oneline --diff-filter=R -- 'docs/**/*.md'
```

If a file was intentionally moved between categories (e.g., a commit message like
`docs(diataxis): reclassify X as reference`), **respect that decision** unless the user
explicitly asks to revisit it. A prior deliberate reclassification reflects a judgment
that the compass alone may not capture — flag it to the user rather than overriding it.

### Classification Rules

Use the compass questions and these signals. For detailed writing guidance per category,
see the reference files in `references/`.

**A page is a Tutorial if it** (see [references/tutorials.md](references/tutorials.md)):

- Guides a beginner through a complete learning experience under the author's direction
- Has a clear starting point and end goal, delivering visible results at each step
- Uses first-person plural: "In this tutorial, we will...", "First, do x. Now, do y."
- Follows a sequential narrative where the reader learns by doing
- Focuses on learning acquisition, not on accomplishing a real-world task
- Minimises explanation — links out instead of digressing

**A page is a How-to guide if it** (see [references/how-to-guides.md](references/how-to-guides.md)):

- Addresses a specific, concrete goal from the user's perspective (not the tool's)
- Assumes the reader already has basic knowledge and knows what they want
- Uses precise titles: "How to integrate monitoring", not "Monitoring"
- Provides an executable solution: "if facing this situation, follow these steps"
- Starts and ends at reasonable points — reader joins it to their own work
- Stays practical without teaching concepts or including reference tables

**A page is Explanation if it** (see [references/explanation.md](references/explanation.md)):

- Discusses concepts, background, design decisions, or trade-offs
- Answers "Can you tell me about...?" — titles work with an implicit "About" prefix
- Makes connections between concepts and provides context (history, reasons, alternatives)
- Uses discursive prose that admits opinion and weighs multiple perspectives
- Could make sense to read away from the keyboard
- Resists absorbing instruction or reference material

**A page is Reference if it** (see [references/reference.md](references/reference.md)):

- Describes APIs, configurations, CLI flags, or data structures authoritatively
- Is structured for lookup (consulted, not read end-to-end)
- Is austere, factual, and precise — states facts using declarative language
- Mirrors the structure of the machinery it describes
- Uses consistent, standard patterns across all entries
- Provides minimal examples that demonstrate usage without teaching

### Mixed Content

Many pages contain content from multiple categories. Flag these for the user and suggest how to split them:

- "This page mixes tutorial content (the getting started section) with reference content
  (the API table). Consider splitting into a tutorial and a reference page."

### Boundary Cases

Some content types sit at the compass boundary. Do not apply the compass mechanically —
consider the page's **structure and intended use**:

- **Troubleshooting**: A lookup table of symptoms, causes, and fixes is **Reference**
  (structured for consultation, mirrors problem structure, austere facts). A page that
  walks through a diagnostic process step-by-step is **How-to** (goal-oriented sequence).
  The format determines the category, not the subject matter.
- **FAQ pages**: Individual Q&A entries are often **Reference** (lookup). A curated FAQ
  that builds understanding is **Explanation**.
- **Migration guides**: Step-by-step upgrade instructions are **How-to**. A discussion
  of what changed and why is **Explanation**.

When in doubt about a boundary case, consider: *how will the reader use this page?*
Consulted for lookup → Reference. Followed as steps → How-to.

### Present Classification Results

Present results as a table:

```text
| File                     | Current Category | Suggested Category | Notes              |
|--------------------------|------------------|--------------------|--------------------------------|
| docs/getting-started.md  | -                | Tutorial           | Good tutorial structure         |
| docs/api.md              | -                | Reference          | Contains some how-to content   |
| docs/architecture.md     | -                | Explanation        | Well-structured explanation     |
```

## Step 3: Propose Documentation Structure

Based on the analysis, propose a Diataxis-aligned directory structure.

### Standard Directory Layout

```text
docs/
  tutorials/           # Learning-oriented
    getting-started.md
    first-project.md
  how-to/              # Task-oriented
    install.md
    configure.md
    deploy.md
  explanation/         # Understanding-oriented
    architecture.md
    design-decisions.md
  reference/           # Information-oriented
    api.md
    configuration.md
    cli.md
```

### Adaptation Rules

- **Adapt to existing tooling**: If the project uses mkdocs, docusaurus, antora, hugo, or similar,
  propose a structure compatible with that tool's conventions.
- **Adapt to existing structure**: If the project already has a docs structure that partially aligns
  with Diataxis, propose minimal changes to align it fully rather than a complete restructure.
- **Keep what works**: Do not propose moving content that is already well-categorized.
- **Respect the project conventions**: If the project uses a specific naming convention
  (kebab-case, snake_case, etc.), follow it.

### Identify Documentation Gaps

After classifying existing content, identify missing pieces:

- **No tutorials?** Suggest creating a getting-started tutorial.
- **No how-to guides?** Suggest guides for the most common tasks (installation, configuration, deployment).
- **No explanation?** Suggest architecture or design decision documents.
- **No reference?** Suggest API, configuration, or CLI reference pages.

Present gaps clearly:

```text
Documentation gaps identified:
- [ ] Missing: Tutorial for getting started
- [ ] Missing: How-to guide for deployment
- [ ] Missing: Reference for configuration options
- [x] Covered: Architecture explanation exists
```

## Step 4: Execute Changes

**Always ask the user before making changes.** Present the plan and wait for approval.

### When Restructuring

1. Present the proposed file moves and renames
2. Wait for user approval
3. Move files to their new locations
4. Update any internal links between documentation pages
5. Update navigation configuration (mkdocs.yml, sidebar config, etc.) if applicable
6. Verify no broken links remain

### When Creating New Pages

1. Present which pages you suggest creating
2. Wait for user approval
3. Create pages with proper structure for their category:

**Tutorial template** (see [references/tutorials.md](references/tutorials.md) for writing principles):

```markdown
# [Title — state what we will build/create]

In this tutorial, we will [concrete goal — what the reader will have at the end].

## Before you begin

- [Prerequisite 1]

## Step 1: [First step — concrete action]

[Direct instruction. Show expected output after each step.]

The output should look something like:

    [example output]

## Step 2: [Second step — builds on previous]

[Direct instruction. Point out what to notice.]

Notice that [observation that closes a learning loop].

## What you've built

You have [concrete summary of achievement].

## Next steps

- [Link to next tutorial or related how-to guide]
```

**How-to guide template** (see [references/how-to-guides.md](references/how-to-guides.md) for writing principles):

```markdown
# How to [accomplish specific goal]

This guide shows you how to [task description].

## Prerequisites

- [Prerequisite — assume basic competence]

## Steps

### 1. [First step]

[Concise, actionable instruction]

### 2. [Second step]

[Concise, actionable instruction]

Refer to the [x reference](link) for a full list of options.

## Troubleshooting

### [Common problem]

If you want [x], do [y].
```

**Explanation template** (see [references/explanation.md](references/explanation.md) for writing principles):

```markdown
# [Topic — should read naturally after "About"]

[Opening paragraph that establishes context and scope]

## Background

[Historical context, design decisions, or foundational concepts]

## [Main concept]

[Discursive explanation — make connections, provide context, admit perspective]

The reason for [x] is because [historical/technical context].
[W] is better than [z] because [reasoning].

## Alternatives and trade-offs

[Discussion of other approaches and why this one was chosen]

## Further reading

- [Related resources]
```

**Reference template** (see [references/reference.md](references/reference.md) for writing principles):

```markdown
# [Component] Reference

[One-line description of what this reference covers]

## [Section — mirrors structure of the machinery]

| Parameter | Type   | Default | Description |
| --------- | ------ | ------- | ----------- |
| `name`    | string | -       | Description |

## [API/Function/Command]

**Signature:** `function_name(param1, param2)`

**Parameters:**

- `param1` (type) — Description
- `param2` (type) — Description

**Returns:** Description of return value

**Example:**

    result = function_name("value", 42)
```

1. Fill in content based on project analysis (source code, existing docs, configuration files)

### When Improving Existing Pages

If a page is already in the right category but needs improvement to better follow Diataxis principles:

1. Identify specific issues (mixed content, wrong tone, missing structure)
2. Present suggested changes to the user
3. Apply changes after approval

## Important Guidelines

- **Do not force the framework**: If the project is small and a single README covers everything
  well, say so. Diataxis is most valuable for projects with substantial documentation needs.
- **Be pragmatic**: A partially-organized documentation set is better than no documentation.
  Suggest incremental improvements rather than demanding perfection.
- **Preserve content**: When restructuring, never delete content. Move and reorganize,
  but keep all existing information.
- **Maintain links**: When moving files, update all cross-references and navigation configurations.
- **Respect the user's decisions**: If the user disagrees with a classification or restructuring
  suggestion, accept their decision and adjust accordingly.
- **Quality awareness**: Diataxis facilitates quality but cannot guarantee it — accuracy,
  completeness, and good writing remain the author's responsibility. See
  [references/quality.md](references/quality.md) for quality dimensions.
- **Use the compass when in doubt**: When classification is unclear or writing feels difficult,
  apply the two compass questions. See [references/compass.md](references/compass.md).

## Reference Documents

Detailed writing guidance for each category, extracted from [diataxis.fr](https://diataxis.fr/):

- [references/tutorials.md](references/tutorials.md) — Pedagogical principles, language conventions, anti-patterns
- [references/how-to-guides.md](references/how-to-guides.md) — Writing principles, scope, distinction from tutorials
- [references/explanation.md](references/explanation.md) — Characteristics, discussion areas, naming test
- [references/reference.md](references/reference.md) — Austerity principles, structure mirroring, examples
- [references/compass.md](references/compass.md) — Two-axis decision tool for classification
- [references/quality.md](references/quality.md) — Functional and deep quality dimensions
