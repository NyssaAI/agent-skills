# Skills Directory

This directory contains the canonical agent skills for `agent-skills` inside `repo_root` (see [`../docs/GLOSSARY.md`](../docs/GLOSSARY.md) for authoritative Ubiquitous Language).

## Skill Structure

Each skill lives in its own subdirectory named after the skill. Multi-workflow domains (`para-vault`, `write-like-me`) are structured as **Sibling Facade Skills** alongside peer `manage-file-operations`:

```text
skills/
└── <skill-name>/
    ├── SKILL.md          # Primary entrypoint & triage facade (required)
    ├── workflows/        # Focused action runbooks for Sibling Facade Skills
    └── references/       # Detailed schemas, checklists, and rules loaded on-demand
```

Host-specific `harness-adapter` glue (such as Hermes `harness-adapters/hermes/plugin.py`) lives under [`../harness-adapters/`](../harness-adapters/), never inside `skills/<skill-name>/agents/`.

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
