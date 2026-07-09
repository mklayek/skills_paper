# skills_paper — Research-Paper Lifecycle Skills (Claude Code marketplace)

A **Claude Code plugin marketplace** (`skills-paper`) of skills covering the research-paper lifecycle for
**deep-learning / GPR / geophysics / remote-sensing** projects:

> **plan → find gaps → write → review → document.**

Writing follows the **IEEE-TGRS style of Ge et al. (2024) ("Wavelet-GAN")**, with strict global rules (US
English, tense, equations, figures, citations) and an honest **"Yet to be developed"** policy so partial
manuscripts never get fabricated results.

---

## Plugins in this marketplace

| Plugin | Skill(s) | What it does |
|---|---|---|
| **`ai-paper`** | `ai-paper` | Write DL/GPR/geophysics/remote-sensing papers or sections in Ge-style (+ paper & thesis templates). |
| **`arch-paper`** | `arch-paper` | Write archaeological GPR (time-slice / depth-slice) papers or sections in Goodman house style, with a five-tier interpretation discipline and reusable per-section templates. |
| **`research-gap`** | `research-gap` | Identify research gaps from uploaded papers/links and propose novel research projects. |
| **`compose-plan`** | `compose-plan` | Generate structured development plans for geophysics / GPR / seismic / AI-ML projects. |
| **`paper-reviewer`** | `review` | Analyze a paper PDF as a rigorous journal reviewer → comprehensive review report. |
| **`doc-tools`** | `doc-readermkl`, `documentation-agent`, `md-updater` | Read, maintain, and update project/research docs (.md/.txt/.pdf/.doc/.xls). |

---

## Repository layout (plugin-marketplace format)

```
skills_paper/
├── .claude-plugin/
│   └── marketplace.json                 # marketplace manifest — lists the plugins
├── README.md
├── AI-Paper.md                          # standalone, self-contained ai-paper spec (whole skill in one file)
├── thesis_guidelines_master.md          # version-independent thesis / technical-report master template
└── plugins/
    ├── ai-paper/         .claude-plugin/plugin.json + skills/ai-paper/SKILL.md + templates/(+sections/)
    ├── research-gap/     .claude-plugin/plugin.json + skills/research-gap/SKILL.md
    ├── compose-plan/     .claude-plugin/plugin.json + skills/compose-plan/SKILL.md
    ├── paper-reviewer/   .claude-plugin/plugin.json + skills/review/SKILL.md
    └── doc-tools/        .claude-plugin/plugin.json + skills/{doc-readermkl,documentation-agent,md-updater}/SKILL.md
```

---

## Install & use in Claude Code (recommended)

Add the marketplace once, then install whichever plugins you want:

```text
/plugin marketplace add mklayek/skills_paper      # register this repo as a marketplace

/plugin install ai-paper@skills-paper             # paper writing
/plugin install research-gap@skills-paper         # research-gap analysis
/plugin install compose-plan@skills-paper         # project planning
/plugin install paper-reviewer@skills-paper       # journal-style paper review
/plugin install doc-tools@skills-paper            # doc reading / maintenance

/plugin                                            # browse / manage installed plugins
/plugin marketplace update skills-paper            # pull the latest after new commits
```

Plugin names install as `<plugin>@skills-paper` (the marketplace name is `skills-paper`).

## Manual install (no marketplace)

Clone and copy any skill folder into your skills dir (`SKILL.md` must sit in its named folder):

```bash
git clone https://github.com/mklayek/skills_paper.git
mkdir -p ~/.claude/skills
cp -a skills_paper/plugins/ai-paper/skills/ai-paper ~/.claude/skills/        # one example
```

## Use without installing (any LLM)

The `ai-paper` rules are fully self-contained in `AI-Paper.md` (root) and
`plugins/ai-paper/skills/ai-paper/templates/AI_Paper_Writing_Skill_complete.md` — paste either into a chat as the
rule-set. Read `…/templates/MASTER_PAPER_template.md` first for the global rules + paper skeleton.

---

## Global writing rules (enforced by `ai-paper`)

- **US English**; acronyms `full name (ACRONYM)` on first use; one term per concept.
- **Tense:** present for design/facts, past for what was done.
- **Equations:** `$…$` / `$$…$$` with `\tag{n}` inside; every symbol glossed (never `\(...\)`, `\[...\]`, or bare `\begin{equation}`).
- **Figures/tables:** numbered in order (tables Roman), referenced before they appear, proposed method last, best metric **bolded**.
- **No fabrication:** unrun work gets `> 🚧 Yet to be developed.` (+ Planned content / Depends on) — never a fake table.

---

## Author

Mrinal Kanti Layek — Geophysics & AI Lab, Chonnam National University.
