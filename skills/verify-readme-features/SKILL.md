---
name: verify-readme-features
description: Verifies that features listed in a README (or similar documentation) are actually
  implemented in the codebase. Use when user mentions verify features, check feature list,
  confirm README, validate documentation claims, or audit feature accuracy.
  Helps catch stale, missing, or inaccurate feature descriptions.
---

# Verify README Features

You are helping the user verify that every feature claim in their project's README (or similar
documentation file) is backed by actual implementation in the codebase.

## When to Use

- After updating a feature list in documentation
- Before a release, to ensure docs match reality
- When onboarding to a project and wanting to trust the README
- When refactoring or removing features that may still be documented

## Verification Process

### Step 1: Identify Feature Claims

1. **Read the documentation file** (default: `README.md` in the project root)
2. **Extract each feature claim** — every bullet point, heading, or sentence that describes
   a capability of the project
3. **Note specific sub-claims** — if a feature says "with X, Y, and Z", each of X, Y, and Z
   is a separate claim to verify

### Step 2: Search the Codebase

For each feature claim:

1. **Identify keywords** — extract the key terms that would appear in an implementation
   (function names, config keys, CSS classes, module names)
2. **Search source files** — use grep/glob to find implementations matching those keywords
3. **Read the relevant code** — confirm the implementation matches the claim, not just the name
4. **Note the evidence** — record the file path and line number(s) where the feature is implemented

### Step 3: Classify Each Claim

Assign one of these statuses:

| Status | Meaning |
| --------------- | ------------------------------------------------------------------ |
| **Confirmed** | Implementation found that matches the claim |
| **Partial** | Implementation exists but does not fully match the claim |
| **Not found** | No implementation found for this claim |
| **Overstated** | Implementation exists but the claim exaggerates its capabilities |

### Step 4: Report Results

Present results in a **summary table** grouped by documentation section, with columns:

| Feature | Status | Evidence |
| ------- | ------ | -------- |

Where:

- **Feature**: the claim as written in the documentation
- **Status**: one of the statuses from Step 3
- **Evidence**: file path and brief description of what was found (or what is missing)

### Step 5: Suggest Fixes

If any claims are **Partial**, **Not found**, or **Overstated**:

1. **Propose documentation edits** — rewrite claims to match reality
2. **Flag missing implementations** — if a documented feature should exist but does not,
   note it as a potential implementation gap
3. **Let the user decide** — do not auto-edit; present the suggestions for approval

## Parallelization Strategy

To verify efficiently:

- **Group related claims** by module or feature area
- **Search in parallel** — verify multiple independent claims concurrently
- **Read source files once** — if multiple claims reference the same file, read it once
  and verify all related claims together

## What to Search

Look for evidence in these locations, ordered by reliability:

1. **Source code** (`src/`, `lib/`, `app/`) — actual implementation
2. **Test files** — tests exercising the feature confirm it works
3. **Configuration schemas** — config keys mentioned in claims
4. **CSS/style files** — for UI-related claims (responsive, themes, overlays)
5. **Type definitions** — for API surface claims

Do **not** count documentation files as evidence — they are the claims, not the proof.

## Edge Cases

- **Third-party features**: If a claim describes a feature provided by a dependency (e.g.,
  "powered by Leaflet"), verify the dependency is declared and used, not that you wrote it
- **Configurable features**: If a claim says "configurable X", verify both the config option
  and the code that reads it
- **UI claims**: For "responsive", "accessible", or similar claims, check for CSS breakpoints,
  ARIA attributes, or relevant code — not just the presence of a CSS file

## Anti-patterns to Avoid

| Anti-pattern | Why it is wrong | Better alternative |
| -------------------------------- | ------------------------------- | ---------------------------------------- |
| Trusting file names alone | A file named `search.js` may not implement full-text search | Read the code and verify behavior |
| Counting docs as evidence | README claims cannot verify themselves | Only source code counts as evidence |
| Skipping sub-claims | "X with A, B, and C" has 4 claims | Verify each sub-claim independently |
| Reporting without evidence | "Confirmed" with no file reference is not verifiable | Always cite file and line |
| Verifying only the happy path | A feature may be partially implemented | Check for complete implementation |

## Example Output

```markdown
## Verification Results

### Section: Core Features

| Feature | Status | Evidence |
| --- | --- | --- |
| Full-text search across properties | Confirmed | `src/search.js:45` — multi-term matching with `.every()` |
| Responsive layout | Confirmed | `src/css/responsive.css:11-113` — 600px breakpoint with mobile adaptations |
| Dark mode | Not found | No dark mode implementation, toggle, or CSS variables found |
| Plugin system (extensible) | Overstated | `src/plugins.js` loads plugins but has no public API for third-party plugins |

### Suggested Fixes

- **Dark mode**: Remove from feature list or implement
- **Plugin system**: Reword to "internal plugin loading" or document the extension API
```

## Important Guidelines

- **Always read the source code** — do not guess or assume from file names
- **Verify every sub-claim** — "with hover highlighting" is a separate claim from "search"
- **Cite specific files and lines** — the user should be able to navigate to the evidence
- **Be honest about gaps** — the goal is accuracy, not validation
- **Do not modify code or docs** without user approval — this is an audit, not a fix
