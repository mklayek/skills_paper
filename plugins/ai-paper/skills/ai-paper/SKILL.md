---
name: ai-paper
description: Use when writing, drafting, or completing a deep-learning / GPR / geophysics / computer-vision / remote-sensing research paper or any of its sections (abstract, introduction, methodology, experiments, ablation, generalization, application, conclusion), or when a manuscript is partially done and needs the remaining sections developed in a consistent journal style.
---

# AI-Paper — Write DL/Geophysics Papers in "Ge-Style"

## Overview
Writes complete or partial technical manuscripts in the IEEE-TGRS scientific style of Ge et al. 2024
("Wavelet-GAN"). It enforces a fixed move-structure, global writing rules (US English, tense, equations,
figures, citations), gap↔contribution alignment, and an honest "Yet to be developed" policy for unfinished work.

**Core principle:** structure and rules are non-negotiable; only the domain content is filled in. Never
fabricate results — unfinished sections get an explicit placeholder, never a plausible fake table.

## Template Library (read before drafting)
Templates are **bundled with this skill** (`./templates/`); read the one matching the section you write.
The single-file edition `templates/AI_Paper_Writing_Skill_complete.md` contains everything inline.

```
<this-skill>/templates/
├── AI_Paper_Writing_Skill_complete.md  # ALL rules + all sections inline (portable single file)
├── MASTER_PAPER_template.md            # GLOBAL rules + full skeleton + unfinished-section policy — READ FIRST
└── sections/
    ├── INTRODUCTION_template.md            # I  (6 moves, gap↔contribution)
    ├── METHODOLOGY_template.md             # II (A data · B transform · C model · D loss/eval)
    ├── EXPERIMENTS_template.md             # III (A setup · B compare · C ablation×3 · D field)
    ├── GENERALIZATION_FINETUNING_template.md   # IV capability demonstration
    ├── APPLICATION_DOWNSTREAM_template.md       # V downstream application
    └── CONCLUSION_template.md              # VI contribution-mirror recap
```
> NAS mirror (kept in sync): `/nas/DATA1/GPRutility_simulations/Q_TEMPLATE_for_Claude/Paper/`.

Each section template gives: role · rhetorical function · paragraph flow · component slots ·
domain-agnostic fill-in sentences · citation/figure/equation rules · length/tone · transition · checklist.

## Workflow
1. **Read `MASTER_PAPER_template.md`** for global rules + the assembled skeleton.
2. **Determine scope** — whole paper, or specific sections? What work is actually done vs pending?
3. **Emit the full skeleton first** (every I–VI heading + subsections, correct IEEE numbering) — even for pending parts.
4. **For each section, read its `sections/*.md`** and fill the slots with the user's project content.
5. **Apply global rules every time** (see Non-Negotiables).
6. **Mark pending work** with the placeholder (see below) — never invent numbers/figures/tables.
7. **Verify** against the Master Checklist + each section's checklist before declaring done.

## Non-Negotiables (global rules)
- **US English** throughout; one consistent term per concept; acronyms `full name (ACRONYM)` on first use.
- **Tense:** present for design/facts, past for what was done, consistent within a paragraph.
- **Equations:** `$…$` / `$$…$$` with `\tag{n}` **inside** the block; every symbol in math delimiters and
  glossed immediately after. NEVER `\(…\)`, `\[…\]`, or bare `\begin{equation}` (md→PDF breaks).
- **Figures/tables:** numbered in order (Tables in Roman numerals), referenced **before** they appear,
  self-contained captions, proposed method last/rightmost, best metric **bolded**.
- **Citations:** IEEE numeric; prior-art dense; **thesis, contributions, conclusion are citation-free**.
- **Gap↔Contribution 1:1:** Intro open-problems ↔ contributions ↔ the sections (IV/V) that demonstrate them.
- **Every results claim:** qualitative → quantitative → attribute to a **mechanism**; include a fairness caveat
  in comparisons; concede one honest limitation + remedy in external-validation/capability sections.

## "Yet to be developed" policy (unfinished manuscripts)
Preserve every heading; under any section whose work is not done, insert:
```
> 🚧 **Yet to be developed.**
> Planned content: [one-line description].
> Depends on: [data / experiment / result still pending].
```
Fully write everything that *can* be written now (intro, method design, loss/metric defs, completed
experiments). **Never fabricate** numbers, figures, or table values; a result without data gets the
placeholder, and figure callouts become `Fig. [N — pending]`.

## Common Mistakes
- Summarizing the method in the contributions list **with citations** → contributions are citation-free.
- Writing a results table before the experiment exists → use the placeholder.
- Mixing British spellings → US English only.
- Bare LaTeX `\[ \]` / `\( \)` in markdown → use `$…$` / `$$…$$`.
- Conclusion introducing new numbers/claims → it only mirrors substantiated contributions.

## Companion Spec
A standalone, self-contained specification of this skill is saved at
`/nas/DATA1/GPRutility_simulations/Q_TEMPLATE_for_Claude/Paper/AI-Paper.md` (same rules + skeleton, for
use outside this runtime or for human reference).
