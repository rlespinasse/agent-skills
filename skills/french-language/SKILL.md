---
name: french-language
description: Ensures all project content is written in proper French with correct accents, grammar,
  and typography. Use when user mentions french, français, langue française, accents, orthographe,
  typographie, or when working on a project that requires French language content. Also use when
  generating any text-based file (SVG, Mermaid, PlantUML, Draw.io, HTML, CSV, JSON, YAML, etc.)
  in a French-language project. Helps enforce French writing conventions across all file types.
---

# Enforce French Language Conventions

You are helping the user ensure that all project content is written in proper French,
with correct accents, grammar, and typographic conventions.

This skill applies to **all generated or edited files** that contain human-readable French text,
not just documentation.

## When to Use

- The project's CLAUDE.md or documentation specifies French as the primary language
- The user asks to write, review, or fix French content
- The user mentions accents, orthographe, typographie, or langue française
- Files contain French text with missing or incorrect accents
- **Generating any file** (SVG, Mermaid, PlantUML, Draw.io, HTML, CSV, JSON, YAML, etc.)
  in a project configured for French

## Pre-flight Checks

Before making changes, always:

1. **Check the project's language configuration** — look for CLAUDE.md, README, or other
   configuration files that specify the project language
2. **Identify which files contain French text** — scan all file types, not just markdown
3. **Ask the user before making bulk changes** — especially when fixing accents across many files

## French Writing Rules

### Accents and Special Characters

French accents are **mandatory**, not optional. Missing accents change word meaning
and are considered spelling errors.

| Character | Name | Examples |
| --------- | ---- | -------- |
| é | accent aigu | réalisateur, qualité, équipe, périmètre |
| è | accent grave | stratège, modèle, problème, critère |
| ê | accent circonflexe | être, clôture, rôle, bâtisseur |
| à | a accent grave | à, déjà, voilà |
| ù | u accent grave | où |
| ô | o accent circonflexe | contrôle, rôle, clôture, binôme |
| î | i accent circonflexe | maître, connaître |
| ç | cédille | ça, français, leçon, reçu |
| ë, ï, ü | tréma | Noël, naïf, ambiguïté |

### Common Missing Accent Patterns

When reviewing or generating French text, watch for these frequently missed accents:

| Wrong | Correct | Context |
| ----- | ------- | ------- |
| qualite | qualité | noun ending in -ité |
| securite | sécurité | noun ending in -ité |
| perimetre | périmètre | noun ending in -ètre |
| deploiement | déploiement | noun with dé- prefix |
| developpeur | développeur | noun with dé- prefix |
| stratege | stratège | noun ending in -ège |
| modele | modèle | noun ending in -èle |
| cloture | clôture | noun with ô |
| equipe | équipe | noun with é |
| role | rôle | noun with ô |
| etre | être | verb with ê |
| batisseur | bâtisseur | noun with â |
| retrospective | rétrospective | noun with é |
| responsabilites | responsabilités | plural noun with é |

### Technical Terms

Technical English terms commonly used in French tech contexts should be **kept in English**:

- Sprint, Backlog, Product Owner, Scope, Deadline
- CI/CD, DevOps, LLMOps, API, SDK
- RACI, SOW, ROI, NPS, KPI
- Pull Request, Code Review, Merge Request
- Framework, Pipeline, Prompt Engineering

**Rule:** if the term is universally used in English in French tech culture, keep it.
If a standard French equivalent exists and is commonly used, prefer the French version.

### French Typography

French typography differs from English in several ways:

| Rule | Example |
| ---- | ------- |
| Space before `:` `;` `!` `?` | `Attention : ceci est important` |
| No space before `,` `.` | `Bonjour, comment allez-vous.` |
| Guillemets for quotes | `« texte »` (with non-breaking spaces) |
| Ordinals | 1er, 2e, 3e (not 1ème, 2ème) |
| Capitalization | Less capitalization than English — `Modèle opératoire` not `Modèle Opératoire` |

**Note on generated files:** Typography rules (spaces before punctuation, guillemets)
may not be practical in all file formats. Prioritize correct accents in all cases;
apply typography rules when the format supports them without breaking rendering.

## Process

### Step 1: Discover Content to Review

Scan the project for **all files** containing French text:

- **Documentation:** `*.md` files
- **Diagrams and visuals:** `*.svg`, `*.drawio`, `*.puml`, `*.mmd` (Mermaid)
- **Web content:** `*.html`, `*.htm`, `*.vue`, `*.jsx`, `*.tsx`
- **Data files:** `*.csv`, `*.json`, `*.yaml`, `*.yml`, `*.toml`
- **Presentations:** `*.tex`, `*.adoc`, `*.rst`
- **Configuration:** `CLAUDE.md`, `README.md`, `*.properties`, `*.ini`
- **Code:** comments and string literals in source files

### Step 2: Analyze and Report

For each file, identify:

- Missing or incorrect accents
- Grammar issues
- Typography issues (spaces before colons, etc.)
- Inconsistent language (mixing French and English in non-technical contexts)

Present findings as a table:

```text
| File | Issue | Wrong | Correct |
|------|-------|-------|---------|
| docs/roles.md | Missing accent | qualite | qualité |
| diagram.svg | Missing accent | deploiement | déploiement |
| data.csv | Missing accent | responsabilite | responsabilité |
```

### Step 3: Apply Fixes

After user approval:

1. Use `Edit` with `replace_all=true` for each correction pattern across each file
2. For each file format, respect the format-specific guidelines below
3. Verify no regressions after applying fixes

### Step 4: Validate

After applying fixes:

1. Search for remaining common missing accent patterns
2. Confirm all files are consistent
3. Report any terms you're unsure about (ask the user for guidance)

## Format-Specific Guidelines

### SVG Files

- **Only modify text content** inside `<text>` elements — never touch coordinates,
  styles, or structure
- **Check text fits** — accented characters may be slightly wider; verify text
  still fits within its container
- **Use UTF-8 characters** — not XML entities (`é` not `&#233;`)
- **Linters may reformat** — SVG optimizers (SVGO) may reformat the file after
  edits. This is expected and should not be reverted

### Mermaid Diagrams (`.mmd`, embedded in markdown)

- Accents work natively in node labels: `A[Qualité] --> B[Sécurité]`
- For labels with special characters, use quotes: `A["Clôture du projet"]`
- Test rendering after adding accents — some Mermaid renderers may
  have issues with certain characters in edge labels

### PlantUML Files (`.puml`)

- Accents work in labels and notes: `:Vérification du périmètre;`
- Use UTF-8 encoding — add `@startuml` without BOM
- Accents in participant names may require quoting:
  `participant "Développeur GenAI" as Dev`

### Draw.io / diagrams.net Files (`.drawio`)

- These are XML files — accents work natively in `value` attributes
- Edit the XML directly or use the visual editor
- Watch for HTML-encoded entities that should be UTF-8 characters

### CSV Files

- Ensure UTF-8 encoding (not Latin-1/ISO-8859-1)
- Accents in field values: `"Qualité","Sécurité","Périmètre"`
- Some spreadsheet tools may re-encode — verify encoding after export

### JSON / YAML Files

- Accents work natively in string values: `"rôle": "Développeur"`
- JSON requires UTF-8 by specification
- YAML supports UTF-8 natively — no quoting needed for accented values

### HTML Files

- Use UTF-8 encoding: `<meta charset="UTF-8">`
- Use actual UTF-8 characters, not HTML entities (`é` not `&eacute;`)
- Check `<title>`, `<meta>`, `alt` attributes, `aria-label`, and visible text

## Generating New Files

When generating any new file that will contain French text:

1. **Write with accents from the start** — do not generate without accents
   and fix later
2. **Use UTF-8 encoding** for all file types
3. **Apply the correct accents as you write** — refer to the common patterns
   table above
4. **Keep technical terms in English** — do not translate universally used
   English terms
5. **Validate before presenting** — re-read your generated content for
   missing accents before showing it to the user

## Important Guidelines

- **Never remove accents** — if unsure whether a word needs an accent, keep it
- **Preserve technical terms in English** — do not translate Sprint, Backlog, etc.
- **Ask before bulk changes** — present the list of fixes before applying them
- **One pattern at a time** — when using `replace_all`, fix one word pattern per edit
  to avoid unintended replacements
- **Context matters** — some words change meaning with/without accents
  (e.g., "ou" = or, "où" = where). Always consider context
- **UTF-8 everywhere** — always use UTF-8 encoding, never Latin-1 or other legacy encodings
- **Generate correctly from the start** — it's cheaper to write accents correctly
  the first time than to fix them after the fact
