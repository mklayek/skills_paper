# skills_paper — Research-Paper Lifecycle Skills (Claude Code marketplace)

A **Claude Code plugin marketplace** (`skills-paper`) of skills covering the research-paper lifecycle for
**deep-learning / GPR / geophysics / seismology / remote-sensing** projects:

> **plan → find gaps → write → review → document → report.**

It also ships **technical-report** generators — `seismo-report` turns seismological data straight into a
chapter-wise, publication-quality interpretation report (MD/HTML/PDF/DOCX).

Writing follows the **IEEE-TGRS style of Ge et al. (2024) ("Wavelet-GAN")**, with strict global rules (US
English, tense, equations, figures, citations) and an honest **"Yet to be developed"** policy so partial
manuscripts never get fabricated results.

---

## Plugins in this marketplace

| Plugin | Skill(s) | What it does |
|---|---|---|
| **`ai-paper`** | `ai-paper` | Write DL/GPR/geophysics/remote-sensing papers or sections in Ge-style (+ paper & thesis templates). |
| **`arch-paper`** | `arch-paper` | Write archaeological GPR (time-slice / depth-slice) papers or sections in Goodman house style, with a five-tier interpretation discipline and reusable per-section templates. |
| **`seismo-report`** | `seismo-report` | Turn seismological inputs (figures, MD, PDF, CSV/XLSX, papers) into a chapter-wise, publication-quality **interpretation report** — detects the study type (event analysis, waveform/FAS/response-spectra, source parameters, ground-motion simulation, **FWI**, ambient noise, GPR-seismic comparison), builds the full chapter set, and renders **MD → HTML → LaTeX-PDF → DOCX** with a formal title page (Times New Roman 12 pt, 1.15 spacing, first-line indent, justified, styled heading hierarchy; Korean-aware). |
| **`research-gap`** | `research-gapmkl` | Identify research gaps from uploaded papers/links and propose novel research projects. |
| **`compose-plan`** | `compose-plan` | Generate structured development plans for geophysics / GPR / seismic / AI-ML projects. |
| **`paper-reviewer`** | `review` | Analyze a paper PDF as a rigorous journal reviewer → comprehensive review report. |
| **`ppt-mkl`** | `ppt-mkl` | Build a research presentation from a paper/methods section: one plain-text deck source renders to **PPTX** (native editable equations), **Beamer PDF**, **.tex** and **.md** in a consistent lecture style (underlined titles, checkbox/star bullets, source equation numbers, figure slides). |
| **`ppt-minimal-mkl`** | `ppt-minimal-mkl` | Build a **minimal, white, classroom-ready PPTX teaching deck** from any source (PDF incl. scanned chapters, MD/HTML/TXT/DOCX, a URL, or a researched topic): white footer-free slides, **◆/■/● title level markers** instead of section numbers, rotating underlined subtitle styles, alternating bullet fonts, **pattern-backed section dividers**, half-and-half text/figure layout, **native editable PowerPoint equations** (built-up OMML) with derivation steps, sequential numbers and per-symbol gloss lines, comparison tables, all working files under **`CWD/temp/<NN>_<name>/`**, and a required QA pass (validation, US-English scan, equation render, layout contact sheets). |
| **`doc-tools`** | `doc-readermkl`, `documentation-agent`, `md-updater`, `methods-read-doc` | Read, maintain, update, and **explain** project/research docs (.md/.txt/.pdf/.doc/.xls); `methods-read-doc` builds beginner-accessible math/methods "read" explainers — per-symbol glossaries, boxed definitions, TikZ schematics **and ray/physics diagrams** (e.g. GPR acquisition geometry → hyperbola → polarity), plus full self-contained **`Fig. N.`** captions (hanging-indent, 3 pt below body, one preamble macro) — with matching PDF/DOCX. |
| **`note-makingmkl`** | `note-makingmkl` | Turn source study/teaching material (Word **.docx**, Markdown, PDF, scanned pages) into a **tight, black-and-white LaTeX → PDF teaching-notes** document: reorganised into a clean **section/subsection** hierarchy, with bounded **KEY POINT / NOTE / RESULT / DEFINITION** boxes, wrapping `tabularx` tables, **in-flow (`[H]`) figures**, page numbers and native equations. Improves low-res images (re-typesets scanned tables and equation crops), then runs a **completeness audit** against the source. Ships a reusable B&W `preamble.tex`, authoring rules and a pandoc extraction script. |
| **`ppt-to-pptx`** | `ppt-to-pptx-restyle` | **Restyle / rebuild an existing PowerPoint** (`.pptx`) into the clean MKL lecture style as a **slide-for-slide mirror** — keep the exact text and figures, **transcribe screenshot equations/definitions into real editable text and native equations**, keep genuine diagrams, and render a styled **PPTX + Beamer PDF** via `ppt-mkl`. Ships `extract_pptx.py` (verbatim text + per-slide images via slide rels), `build_mirror_deck.py` (per-slide deck with auto-montaged figures) and `sanitize_deck.py` (LaTeX-safe paths/characters). |

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
    ├── seismo-report/    .claude-plugin/plugin.json + skills/seismo-report/SKILL.md + seismo-report.md + templates/ + scripts/ (build_report.py, make_reference_docx.py, preamble_seismo.tex, seismo.css) + reference/ + examples/ + tests/
    ├── research-gap/     .claude-plugin/plugin.json + skills/research-gap/SKILL.md
    ├── compose-plan/     .claude-plugin/plugin.json + skills/compose-plan/SKILL.md
    ├── paper-reviewer/   .claude-plugin/plugin.json + skills/review/SKILL.md
    ├── ppt-mkl/          .claude-plugin/plugin.json + skills/ppt-mkl/SKILL.md + DECK_SPEC.md + template.deck + scripts/
    ├── ppt-minimal-mkl/  .claude-plugin/plugin.json + skills/ppt-minimal-mkl/SKILL.md
    ├── ppt-to-pptx/      .claude-plugin/plugin.json + skills/ppt-to-pptx-restyle/SKILL.md + scripts/(extract_pptx.py, build_mirror_deck.py, sanitize_deck.py)
    ├── doc-tools/        .claude-plugin/plugin.json + skills/{doc-readermkl,documentation-agent,md-updater,methods-read-doc}/SKILL.md
    └── note-makingmkl/   .claude-plugin/plugin.json + skills/note-makingmkl/SKILL.md + references/(preamble.tex, authoring_rules.md) + scripts/extract_source.sh
```

---

## Install & use in Claude Code (recommended)

Add the marketplace once, then install whichever plugins you want:

```text
/plugin marketplace add mklayek/skills_paper      # register this repo as a marketplace

/plugin install ai-paper@skills-paper             # paper writing
/plugin install arch-paper@skills-paper           # archaeological GPR papers
/plugin install seismo-report@skills-paper        # seismological interpretation reports (MD/HTML/PDF/DOCX)
/plugin install research-gap@skills-paper         # research-gap analysis
/plugin install compose-plan@skills-paper         # project planning
/plugin install paper-reviewer@skills-paper       # journal-style paper review
/plugin install ppt-mkl@skills-paper              # research presentations (PPTX + Beamer)
/plugin install ppt-minimal-mkl@skills-paper      # minimal white teaching decks (PPTX)
/plugin install doc-tools@skills-paper            # doc reading / maintenance
/plugin install note-makingmkl@skills-paper       # notes -> tight B&W LaTeX/PDF teaching notes

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
