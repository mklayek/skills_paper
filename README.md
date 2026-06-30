# skills_paper — AI-Paper Writing Skill & Templates

A Claude skill (and a set of portable templates) for writing **deep-learning / GPR / geophysics /
computer-vision / remote-sensing** research manuscripts in the **IEEE-TGRS scientific style of Ge et al. (2024)
("Wavelet-GAN")**. It enforces a fixed move-structure, global writing rules (US English, tense, equations,
figures, citations), gap↔contribution alignment, and an honest **"Yet to be developed"** policy for unfinished
work — so a partial manuscript never gets fabricated results.

---

## What's in here

```
skills_paper/
├── SKILL.md                                   # the Claude skill definition (rules + workflow)
├── AI-Paper.md                                # standalone, self-contained companion spec (whole skill in one file)
├── thesis_guidelines_master.md                # version-independent thesis / technical-report master template
└── templates/
    ├── AI_Paper_Writing_Skill_complete.md     # ALL rules + ALL sections inline (portable single file)
    ├── MASTER_PAPER_template.md               # global rules + full paper skeleton — READ FIRST
    └── sections/
        ├── INTRODUCTION_template.md           # §I  (6 moves, gap↔contribution)
        ├── METHODOLOGY_template.md            # §II (A data · B transform · C model · D loss/eval)
        ├── EXPERIMENTS_template.md            # §III (setup · compare · ablation · field)
        ├── GENERALIZATION_FINETUNING_template.md  # §IV capability demonstration
        ├── APPLICATION_DOWNSTREAM_template.md      # §V downstream application
        └── CONCLUSION_template.md             # §VI contribution-mirror recap
```

- **Just want to write a paper now?** Read `templates/MASTER_PAPER_template.md` first, then the relevant
  `templates/sections/*.md`. Everything is also inlined in `templates/AI_Paper_Writing_Skill_complete.md`.
- **Want it as an auto-loading Claude skill?** Install `SKILL.md` (see below).

---

## Clone

```bash
git clone https://github.com/mklayek/skills_paper.git
cd skills_paper
```

---

## Install

### Option A — as a Claude Code skill (auto-discovered)

Claude Code loads skills from your skills directory. Copy the skill folder so the layout is
`.../skills/ai-paper/SKILL.md` (+ its `templates/`):

```bash
# user-level skills (available in every project)
mkdir -p ~/.claude/skills/ai-paper
cp -a SKILL.md templates ~/.claude/skills/ai-paper/

# OR project-level (only this repo/project)
mkdir -p .claude/skills/ai-paper
cp -a SKILL.md templates .claude/skills/ai-paper/
```

> Path note: some Claude Code setups use a plugin marketplace dir
> (e.g. `~/.claude-oh/local-marketplace/plugins/ai-paper/skills/ai-paper/`). If yours does, copy into that
> `skills/ai-paper/` location instead. The only requirement is that `SKILL.md` sits in a folder named `ai-paper`
> with its `templates/` beside it.

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
