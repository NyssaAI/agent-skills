# Skills Directory

This directory contains individual agent skills for the NyssaAI ecosystem.

## Skill Structure

Each skill lives in its own subdirectory named after the skill:

```
skills/
└── <skill-name>/
    ├── SKILL.md          # Primary instruction file (required)
    ├── scripts/          # Optional helper scripts executed by the agent
    ├── references/       # Optional detailed documentation loaded on-demand
    └── examples/         # Optional reference implementations or patterns
```

## Anatomy of a `SKILL.md`

Every `SKILL.md` starts with YAML frontmatter:

```yaml
---
name: your-skill-name
description: Clear, actionable description of when the agent should activate this skill. Include trigger keywords and use cases.
---

# Skill Title

## Overview
What this skill accomplishes and key principles.

## Workflow / Instructions
Step-by-step guidance for the agent to follow.
```

## Skill Guidelines

1. **Progressive Disclosure**: Only the `name` and `description` are loaded into agent context initially. The full `SKILL.md` is loaded on-demand when relevant.
2. **Action-Oriented**: Write clear, imperative procedures that instruct the agent on what tools to call, how to validate output, and how to handle errors.
3. **Keep Boundaries Explicit**: Skills should focus on a specific capability or workflow.
