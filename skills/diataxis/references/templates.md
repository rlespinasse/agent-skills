# Page Templates

## Tutorial template

See `tutorials.md` for writing principles.

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

## How-to guide template

See `how-to-guides.md` for writing principles.

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

## Explanation template

See `explanation.md` for writing principles.

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

## Reference template

See `reference.md` for writing principles.

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
