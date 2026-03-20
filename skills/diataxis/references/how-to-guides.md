# How-to Guides — Writing Guide

> Source: [diataxis.fr/how-to-guides](https://diataxis.fr/how-to-guides/)

How-to guides are directions that guide readers through real-world problems toward results.
They are goal-oriented — they help users get something done, correctly and safely.

## Essential Principle

How-to guides must be written from the perspective of the user, not of the machinery.
Guides are about goals, projects and problems — not about tools.

## Scope

Address specific, concrete goals:

- **Good:** "How to calibrate the radar array", "How to use fixtures in pytest"
- **Bad:** "How to build a web application" (too broad)

## Distinction from Tutorials

Tutorials and how-to guides are wholly distinct:

| Aspect | Tutorial | How-to guide |
| --- | --- | --- |
| Audience | Novice learner | Already-competent user |
| Purpose | Teach foundational skills | Help accomplish a specific goal |
| Completeness | Complete from start to finish | Starts and ends at reasonable points |
| Integration | Self-contained | Reader joins guide to their own work |
| Direction | "Follow me" | "Do this" |

## Writing Principles

### 1. Real-world Adaptability

Find ways to remain open to the range of real-world possibilities so users can adapt
guidance to their specific situation.

### 2. Practical Usability Over Completeness

Practical usability is more helpful than completeness. Focus on what the user needs
to get the job done, not on covering every edge case.

### 3. Executable Solutions

Describe an executable solution structured as a contract: if you are facing this situation,
following these steps will resolve it.

### 4. Logical Sequence

The fundamental structure is a sequence with logical ordering in time. Each step follows
naturally from the previous one.

### 5. Flow and Pacing

Must be grounded in patterns of the user's activities and thinking. Avoid requiring users
to repeatedly switch contexts between different tools or concepts. At its best, documentation
appears to "anticipate" the user.

### 6. Precise Naming

Titles must explicitly state what the guide demonstrates:

- **Good:** "How to integrate application performance monitoring"
- **Bad:** "Application performance monitoring"

## Language Conventions

- "This guide shows you how to..."
- "If you want x, do y."
- "Refer to the x reference guide for a full list of options."

## Anti-patterns

- Explaining tool mechanics (that belongs in explanation)
- Teaching foundational concepts (that belongs in tutorials)
- Including reference tables for completeness (that belongs in reference)
- Overly narrow procedures that only work in one exact scenario
- Digressions into background information
- Forcing the reader to context-switch between unrelated tools
- Ambiguous titles that don't state the goal

## Analogy

Recipes in a cookbook. They clearly define what will be achieved, address a specific question,
require basic competence, and exclude teaching and theoretical discussion.
