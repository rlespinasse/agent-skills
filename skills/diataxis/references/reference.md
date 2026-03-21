# Reference — Writing Guide

> Source: [diataxis.fr/reference](https://diataxis.fr/reference/)

Reference documentation provides technical descriptions of the machinery and how to operate it.
It is information-oriented, containing propositional or theoretical knowledge that users
consult during their work.

## Purpose

To describe, as succinctly as possible, and in an orderly way. Reference is led by the
product it describes — APIs, classes, functions, configuration options, CLI commands.

## User Need

Users need truth and certainty — firm platforms on which to stand while they work. Reference
must be wholly authoritative with no doubt or ambiguity.

## Nature

One hardly reads reference material — one **consults** it. It should be austere, structured
for lookup, not for sequential reading.

## Writing Principles

### 1. Describe and Only Describe

Neutral description is the key imperative. The tone should be austere, uncompromising,
neutral, objective, and factual. Structure should align with the machinery itself.

**Anti-pattern:** Introducing instruction ("first do this, then...") or explanation
("the reason this works is...") into reference material. Instead, link to the appropriate
how-to guide or explanation page.

### 2. Adopt Standard Patterns

Reference is most useful when consistent. Users should find information where they expect it,
in a familiar format. Resist the urge to vary structure or demonstrate vocabulary range —
uniformity serves the reader.

### 3. Respect the Structure of the Machinery

Documentation structure should mirror the product's structure so users can navigate both
simultaneously. If the code has modules, the reference should have corresponding sections.

### 4. Provide Examples

Examples illustrate usage succinctly. They should demonstrate, not instruct or explain.
Keep them minimal and focused on showing how something is used, not teaching a concept.

## Language Conventions

State facts. Use precise, declarative language:

- List commands, options, operations, features, flags, limitations, error messages
- Use conditionals for constraints: "You must use a. You must not apply b unless c. Never d."
- Avoid narrative prose or persuasive language

## Analogy

Food packaging — consumers expect standardized information (nutritional data, storage
instructions, ingredients) in predictable formats. No recipes, no marketing claims — just
facts presented with legal-level rigor and consistency.
