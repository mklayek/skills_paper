# skills_paper — AI-Paper Writing Skill & Templates

A Claude skill (and a set of portable templates) for writing **deep-learning / GPR / geophysics /
computer-vision / remote-sensing** research manuscripts in the **IEEE-TGRS scientific style of Ge et al. (2024)
("Wavelet-GAN")**. It enforces a fixed move-structure, global writing rules (US English, tense, equations,
figures, citations), gap↔contribution alignment, and an honest **"Yet to be developed"** policy for unfinished
work — so a partial manuscript never gets fabricated results.

---

## What's in here

This repo is a **Claude Code plugin marketplace** (`.claude-plugin/marketplace.json`) named **`skills-paper`**,
providing the **`ai-paper`** plugin:

```
skills_paper/
├── .claude-plugin/
│   └── marketplace.json                       # marketplace manifest (lists plugins)
├── README.md
├── AI-Paper.md                                # standalone, self-contained companion spec (whole skill in one file)
├── thesis_guidelines_master.md                # version-independent thesis / technical-report master template
└── plugins/
    └── ai-paper/                              # the plugin
        ├── .claude-plugin/
        │   └── plugin.json                    # plugin manifest
        └── skills/
            └── ai-paper/
                ├── SKILL.md                   # the Claude skill definition (rules + workflow)
                └── templates/
                    ├── AI_Paper_Writing_Skill_complete.md   # ALL rules + ALL sections inline (portable)
                    ├── MASTER_PAPER_template.md             # global rules + full paper skeleton — READ FIRST
                    └── sections/                            # §I Introduction … §VI Conclusion templates
```

- **Easiest in Claude Code?** Add the marketplace and install the plugin (see Install → Option A).
- **Just want to write a paper now (any LLM)?** Read
  `plugins/ai-paper/skills/ai-paper/templates/MASTER_PAPER_template.md` first, then the relevant `sections/*.md`.
  Everything is also inlined in `AI-Paper.md` (root) and `…/templates/AI_Paper_Writing_Skill_complete.md`.

---

## Clone

```bash
git clone https://github.com/mklayek/skills_paper.git
cd skills_paper
```

---

## Install

### Option A — as a Claude Code plugin marketplace (recommended)

This repo is a **Claude Code plugin marketplace** (`.claude-plugin/marketplace.json`), so you can add it and
install the plugin directly inside Claude Code — no manual file copying:

```text
/plugin marketplace add mklayek/skills_paper     # register this repo as a marketplace
/plugin install ai-paper@skills-paper            # install the plugin (name@marketplace)
/plugin                                           # browse / manage installed plugins
/plugin marketplace update skills-paper           # pull the latest after new commits
```

The marketplace is named **`skills-paper`** and provides the **`ai-paper`** plugin (which carries the
`ai-paper` skill under `plugins/ai-paper/skills/ai-paper/`).

### Option B — manual skill copy (no marketplace)

Copy the skill folder so the layout is `.../skills/ai-paper/SKILL.md` (+ its `templates/`):

```bash
git clone https://github.com/mklayek/skills_paper.git
mkdir -p ~/.claude/skills
cp -a skills_paper/plugins/ai-paper/skills/ai-paper ~/.claude/skills/   # user-level (all projects)
# OR project-level:  cp -a skills_paper/plugins/ai-paper/skills/ai-paper .claude/skills/
```

> The only requirement is that `SKILL.md` sits in a folder named `ai-paper` with its `templates/` beside it.

Restart / reopen Claude Code so it re-scans skills. Verify it loaded by checking the available-skills list (the
skill is named **`ai-paper`**).

### Option B — templates only (no skill install, works with any LLM)

No setup needed. Hand `AI-Paper.md` (or `templates/AI_Paper_Writing_Skill_complete.md`) to any Claude/LLM session
as the rule-set, then ask it to draft your paper. Both files are fully self-contained.

---

## Use in Claude

### If installed as a skill (Option A)

Invoke it explicitly or let Claude auto-trigger it when you ask for paper work:

```
/ai-paper
```
or just:
```
Write the Methodology section of my paper on <your model> using the ai-paper skill.
```

Claude will: read `MASTER_PAPER_template.md` for global rules → emit the full I–VI skeleton → fill each section
from your project content using the matching `sections/*.md` → mark unfinished parts "Yet to be developed."

### If using templates only (Option B)

Paste the relevant template into the chat and give your project facts, e.g.:

```
Here is MASTER_PAPER_template.md: <paste>.
My project: <model name, dataset, method, results, what's done vs pending>.
Draft Section III (Experiments) following the template's rules. Mark unrun experiments
"Yet to be developed" — do not fabricate tables.
```

### Workflow (what the skill does)

1. Read `MASTER_PAPER_template.md` (global rules + assembled skeleton).
2. Determine scope — whole paper, or specific sections; what's done vs pending.
3. Emit the full I–VI skeleton (correct IEEE numbering) — even for pending parts.
4. For each section, read its `sections/*.md` and fill the slots with your content.
5. Apply the global rules every time (below).
6. Mark pending work with the placeholder — never invent numbers/figures/tables.
7. Verify against the Master Checklist before declaring done.

---

## Global rules (enforced by the skill)

- **US English**; one consistent term per concept; acronyms `full name (ACRONYM)` on first use.
- **Tense:** present for design/facts, past for what was done; consistent within a paragraph.
- **Equations:** `$…$` / `$$…$$` with `\tag{n}` **inside** the block; every symbol glossed. Never `\(...\)`,
  `\[...\]`, or bare `\begin{equation}` (md→PDF breaks).
- **Figures/tables:** numbered in order (tables in Roman numerals), referenced **before** they appear,
  self-contained captions, proposed method last/rightmost, best metric **bolded**.
- **Citations:** IEEE numeric by default; thesis/contributions/conclusion are citation-free. (Short author–year,
  e.g. `(Ge et al., 2024)`, is also supported if you ask for it.)
- **Gap ↔ Contribution 1:1:** intro open-problems ↔ contributions ↔ the sections that demonstrate them.
- **No fabrication:** unrun work gets the explicit placeholder, never a plausible fake table:
  ```
  > 🚧 Yet to be developed.
  > Planned content: [one-line description].
  > Depends on: [data / experiment / result still pending].
  ```

---

## Thesis / technical-report template

`thesis_guidelines_master.md` is a separate, version-independent master for **theses, dissertations, technical
reports, and model documentation** (Document Philosophy → Standard Report Structure → reproducibility/archival
rules). Derive a project-specific copy named `thesis_guidelines_{version}_{date}_{time}.md`; keep the master
generic.

---

## Author

Mrinal Kanti Layek — Geophysics & AI Lab, Chonnam National University.
