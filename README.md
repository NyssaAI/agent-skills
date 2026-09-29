# NyssaAI Agent Skills

Version: **0.1.0**

Foundational skills and conventions for how Jeremy and NyssaAI's AI agents organize information, manage files, and carry out work. Built with a universal layout compatible with **Google Antigravity (AGY)**, **Claude Code**, **OpenAI Codex**, **OpenClaw**, and **Hermes Agent**.

---

## Installation & Usage

### 1. Claude Code

#### Via NyssaAI Curated Marketplace (Recommended)
```bash
/plugin marketplace add github.com/NyssaAI/plugin-marketplace
/plugin install agent-skills@nyssaai
```

#### Direct Repository Add
```bash
/plugin add github.com/NyssaAI/agent-skills
```

### 2. OpenAI Codex

Add to your `.codex` configuration or clone into your skills directory:
```bash
git clone https://github.com/NyssaAI/agent-skills.git
```
Codex discovers skills via `.codex-plugin/plugin.json` and `skills/`.

### 3. Google Antigravity (AGY)

Include as a workspace customization in `.agents/` or install globally via `~/.gemini/config/plugins/`. Discovered automatically via `gemini-extension.json` and `.agents/plugins.json`.

### 4. OpenClaw & Hermes Agent

Both runtimes natively read the AgentSkills.io standard directory:
```bash
git clone https://github.com/NyssaAI/agent-skills.git
```
Point your agent runtime or extra skills directory to `./skills/`.

---

## Skills Catalog

| Skill | Description | Supported Agents |
| :--- | :--- | :--- |
| [**`para-vault`**](skills/para-vault/) | Apply PARA placement and vault conventions for layout, metadata, indexes, and archiving. | AGY, Claude, Codex, OpenClaw, Hermes |
| [**`file-management`**](skills/file-management/) | Manage files and folders generally, including time-bound naming, `.temp/` intermediate work, and safe operations. | AGY, Claude, Codex, OpenClaw, Hermes |

---

`file-management` handles general naming and safe file operations. `para-vault` adds the folder, metadata, navigation, and workflow conventions for PARA vaults. Use both when a vault task needs general file operations.

## Repository Structure

```
.
├── .agents/
│   └── plugins.json                   # Antigravity skill declarations
├── .claude-plugin/
│   └── plugin.json                    # Claude Code plugin manifest
├── .codex-plugin/
│   └── plugin.json                    # Codex plugin manifest
├── gemini-extension.json              # Antigravity extension metadata
├── AGENTS.md                          # Universal agent instruction anchor
├── CLAUDE.md                          # Claude Code reference
├── GEMINI.md                          # Antigravity reference
├── skills/                            # Canonical skills directory
│   ├── para-vault/                    # PARA placement and vault conventions
│   │   ├── SKILL.md
│   │   ├── agents/openai.yaml
│   │   └── references/
│   │       ├── folder-conventions.md
│   │       ├── navigation.md
│   │       ├── frontmatter-schemas.md
│   │       └── file-workflows.md
│   └── file-management/               # File conventions and operations
│       ├── SKILL.md
│       ├── agents/openai.yaml
│       └── references/
│           └── safe-operations.md
├── LICENSE                            # MIT License
└── README.md
```

---

## Adding a New Skill

1. Create a new directory under `skills/<skill-name>/`.
2. Add a `SKILL.md` with standard frontmatter:
   ```yaml
   ---
   name: <skill-name>
   description: >-
     A concise description explaining when the agent should trigger this skill.
   ---

   # Skill Name

   ## Workflow
   Step-by-step guidance.
   ```
3. If the skill has complex rules or schemas, put them into `references/` and link to them using relative paths.
4. Optional: add `agents/openai.yaml` if you want custom prompt starters or titles in OpenAI Codex UI.

---

## Evaluation

The [evaluation suite](evals/README.md) provides 24 isolated behavioral cases, a weighted scoring rubric with critical failure gates, and reproducible evidence exports. See the [rubric and coverage](docs/eval-suite.md).

## License

[MIT](LICENSE) © 2026 NyssaAI
