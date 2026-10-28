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
| ⭐ **`ppt-minimal-skill-v5`** *(default for slide decks)* | `ppt-minimal-skill-v5` | **v5 of the teaching-deck builder** (v4 + the user's PPT rules): **no equation, figure, page or section numbers and no footers** (printed captions cropped out of figures too), **every source equation** (inventory + coverage check) with detailed derivations and ▸ symbol lines, native editable equations with **LHS/RHS colors alternating per equation** (black/deep blue, dark red/green), **every source figure** with enriched bullets, **22 pt** body, subtitles only where a definition starts, **source section names as titles** with "(continued)", a **title font and color per section** (Copperplate Gothic default), archive-first, a Markdown copy, and a tested build chain (`scripts/`: pandoc-OMML equations, splitter calibration, PowerPoint-COM export that never closes other decks, coverage, number and layout checks). |
| **`ppt-minimal-skill-v6`** *(arrow-chain slides, on request)* | `ppt-minimal-skill-v6` | **v6 of the teaching-deck builder**: body text chosen **per slide**, a **source slide** (bullets close to the source wording) or a **chain slide** (**Concept → original principle or mechanism → physical meaning, implication or application**, a run of the source sentence kept in the middle). **Arrow direction is decided per bullet** (→ "leads to", ← "is caused by", read-aloud test), every segment gets **its own color**, formats **alternate from bullet to bullet**. **Since 6.1 it shares v7's frame and titles**: the **class title slide** (method name, method group, Lecture NN, asked before building) and **Thank you slide** (`frame.py`, editable), a **font, dark color and title bullet per topic**, **centered topic start** and **left-aligned continued** titles, light or no title fill, a **gold oval** for key titles, a **black topic label** (white text) for source sub-parts (`'Section › Sub-part'`), **Figure : description (source)** captions directly under the image, and continuous **Times New Roman 18 pt** symbol lines. `qa.py` checks chains, topic titles and frame slides. |
| **`ppt-minimal-skill-v7`** *(all-arrow class decks, on request)* | `ppt-minimal-skill-v7` | **v7 of the teaching-deck builder**: v6's frame, titles, captions and symbol lines, with **every bullet an arrow chain** (no source slides, the build stops on a plain bullet) and **one line per bullet**: words that would wrap move to the next bullet (`fontwidths.py` measures the real fonts, `oneline_check.py` checks the PowerPoint render). Never a "Definition:" subtitle. Ships `examples/c1_example_v7.js` and `assets/frame_template.pptx`. |
| **`ppt-minimal-mkl`** *(v4, superseded by v5)* | `ppt-minimal-mkl` | Build a **minimal, white, classroom-ready PPTX teaching deck** from any source (PDF incl. scanned chapters, MD/HTML/TXT/DOCX, a URL, or a researched topic): white footer-free slides, **◆/■/● title level markers** instead of section numbers, rotating underlined subtitle styles, alternating bullet fonts, **pattern-backed section dividers**, half-and-half text/figure layout, **native editable PowerPoint equations** (built-up OMML) with derivation steps, sequential numbers and per-symbol gloss lines, comparison tables, all working files under **`CWD/temp/<NN>_<name>/`**, and a required QA pass (validation, US-English scan, equation render, layout contact sheets). |
| **`ppt-mkl`** | `ppt-mkl` | Build a research presentation from a paper/methods section: one plain-text deck source renders to **PPTX** (native editable equations), **Beamer PDF**, **.tex** and **.md** in a consistent lecture style (underlined titles, checkbox/star bullets, source equation numbers, figure slides). |
| **`doc-tools`** | `doc-readermkl`, `documentation-agent`, `md-updater`, `methods-read-doc` | Read, maintain, update, and **explain** project/research docs (.md/.txt/.pdf/.doc/.xls); `methods-read-doc` builds beginner-accessible math/methods "read" explainers — per-symbol glossaries, boxed definitions, TikZ schematics **and ray/physics diagrams** (e.g. GPR acquisition geometry → hyperbola → polarity), plus full self-contained **`Fig. N.`** captions (hanging-indent, 3 pt below body, one preamble macro) — with matching PDF/DOCX. |
| **`note-makingmkl`** | `note-makingmkl` | Turn source study/teaching material (Word **.docx**, Markdown, PDF, scanned pages) into a **tight, black-and-white LaTeX → PDF teaching-notes** document: reorganised into a clean **section/subsection** hierarchy, with bounded **KEY POINT / NOTE / RESULT / DEFINITION** boxes, wrapping `tabularx` tables, **in-flow (`[H]`) figures**, page numbers and native equations. Improves low-res images (re-typesets scanned tables and equation crops), then runs a **completeness audit** against the source. Ships a reusable B&W `preamble.tex`, authoring rules and a pandoc extraction script. |
| **`tex-notes-mkl`** | `tex-notes-mkl` | Build **short, simplified two-column LaTeX → PDF lecture notes** (11 pt, A4, Times, 2–4 pages or the user's page limit) that explain **what a source's equations mean and why they matter**: every source equation with its number (chapter prefix dropped, e.g. (8.38) → (38)), **"Reading the equation"** bullets on the physical meaning of each term, limiting cases, practical use on field data, algebra **verified numerically in Python**, 1–3 **matplotlib figures computed from the equations**, a small numbers table, a `booktabs` summary table, a green **key-message box** and a navy **"in plain words"** closing box. Ships the preamble template, page-limit fitting steps and a required QA pass (log, page count, contact sheet, US-English scan). Delivers the **PDF + .tex**. |
| **`ppt-to-pptx`** | `ppt-to-pptx-restyle` | **Restyle / rebuild an existing PowerPoint** (`.pptx`) into the clean MKL lecture style as a **slide-for-slide mirror** — keep the exact text and figures, **transcribe screenshot equations/definitions into real editable text and native equations**, keep genuine diagrams, and render a styled **PPTX + Beamer PDF** via `ppt-mkl`. Ships `extract_pptx.py` (verbatim text + per-slide images via slide rels), `build_mirror_deck.py` (per-slide deck with auto-montaged figures) and `sanitize_deck.py` (LaTeX-safe paths/characters). |

### Which slide-deck skill? ⭐

**`ppt-minimal-skill-v5` is the default for making a PPT** (it replaces `ppt-minimal-mkl` v4). Reach for it whenever the ask is "make a deck / PPTX / slides / lecture
presentation" from a source or a topic. It is the newest builder (v5) and the one to use unless a reason below applies.

| Situation | Use |
|---|---|
| Any new deck from a PDF, chapter, notes, MD/HTML/DOCX, a URL or a researched topic | **`ppt-minimal-skill-v5`** (default) |
| "v6" is named, or **arrow-style / arrow-chain slides** (Concept → mechanism → meaning) mixed with source-style slides are asked for | `ppt-minimal-skill-v6` |
| "v7" is named, or a class deck where **every bullet is an arrow chain** on one line is asked for | `ppt-minimal-skill-v7` |
| The older v4 style is asked for by name (sequential equation numbers, rotating subtitles) | `ppt-minimal-mkl` |
| You want the same content as a **Beamer PDF / .tex** alongside the PPTX, or the checkbox-bullet research-talk style | `ppt-mkl` |
| You already have a `.pptx` and want it **restyled slide-for-slide** | `ppt-to-pptx` |
| The deliverable is a printable **notes document**, not slides | `note-makingmkl` |
| Short **two-column notes explaining the significance of equations** (with computed figures, a page limit) | `tex-notes-mkl` |

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
    ├── ppt-minimal-skill-v5/  .claude-plugin/plugin.json + skills/ppt-minimal-skill-v5/SKILL.md + scripts/ + examples/ + reference/PPT_INSTRUCTIONS.md
    ├── ppt-minimal-skill-v6/  .claude-plugin/plugin.json + skills/ppt-minimal-skill-v6/SKILL.md + scripts/ (chain() renderer, frame.py, topic titles, ARROW CHAINS qa) + assets/frame_template.pptx + examples/c1_example_v6.js + reference/ARROW_NOTES_FORMAT.md
    ├── ppt-minimal-skill-v7/  .claude-plugin/plugin.json + skills/ppt-minimal-skill-v7/SKILL.md + scripts/ (all-chain renderer, one-line bullets, fontwidths.py, oneline_check.py, frame.py) + assets/frame_template.pptx + examples/c1_example_v7.js
    ├── ppt-minimal-mkl/  .claude-plugin/plugin.json + skills/ppt-minimal-mkl/SKILL.md   (v4, superseded)
    ├── ppt-to-pptx/      .claude-plugin/plugin.json + skills/ppt-to-pptx-restyle/SKILL.md + scripts/(extract_pptx.py, build_mirror_deck.py, sanitize_deck.py)
    ├── doc-tools/        .claude-plugin/plugin.json + skills/{doc-readermkl,documentation-agent,md-updater,methods-read-doc}/SKILL.md
    ├── note-makingmkl/   .claude-plugin/plugin.json + skills/note-makingmkl/SKILL.md + references/(preamble.tex, authoring_rules.md) + scripts/extract_source.sh
    └── tex-notes-mkl/    .claude-plugin/plugin.json + skills/tex-notes-mkl/SKILL.md   (preamble template inside SKILL.md)
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
/plugin install ppt-minimal-skill-v5@skills-paper # DEFAULT deck builder (v5) - minimal white teaching decks (PPTX)
/plugin install ppt-minimal-skill-v6@skills-paper # v6 deck builder - mixed source/arrow-chain slides + class frame and topic titles (on request)
/plugin install ppt-minimal-skill-v7@skills-paper # v7 deck builder - all arrow-chain, one-line bullets, class frame and topic titles (on request)
/plugin install ppt-minimal-mkl@skills-paper      # v4 deck builder (superseded by v5)
/plugin install ppt-mkl@skills-paper              # research presentations (PPTX + Beamer)
/plugin install doc-tools@skills-paper            # doc reading / maintenance
/plugin install note-makingmkl@skills-paper       # notes -> tight B&W LaTeX/PDF teaching notes
/plugin install tex-notes-mkl@skills-paper        # short two-column equation-explainer notes (LaTeX/PDF)

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
