# skills_paper — Detailed Skills Report

A complete walkthrough of every plugin, skill, and sub-skill in the **`skills-paper`** Claude Code marketplace (`github.com/mklayek/skills_paper`). The marketplace covers the full research-paper lifecycle for deep-learning, GPR, geophysics, seismology, and remote-sensing work:

> **plan → find gaps → write → review → present → document → report.**

All writing skills follow the IEEE-TGRS house style of **Ge et al. (2024) ("Wavelet-GAN")**, enforce strict global rules (US English, tense, equations, figures, citations), and use an honest **"Yet to be developed"** policy so partial manuscripts never get fabricated results.

---

## 📑 Contents

1. [Marketplace at a glance](#1-marketplace-at-a-glance)
2. [Install and use](#2-install-and-use)
3. [ai-paper](#3-ai-paper) — write DL/GPR papers in Ge-style
4. [arch-paper](#4-arch-paper) — archaeological GPR papers, Goodman style
5. [research-gap](#5-research-gap) — gap detection and proposals
6. [compose-plan](#6-compose-plan) — structured development plans
7. [paper-reviewer](#7-paper-reviewer) — journal-style paper review
8. [ppt-mkl](#8-ppt-mkl) — presentations (PPTX + Beamer + MD)
9. [doc-tools](#9-doc-tools) — read, maintain, and explain documentation
10. [seismo-report](#10-seismo-report) — seismological interpretation reports (MD/HTML/PDF/DOCX)
11. [Cross-cutting writing rules](#11-cross-cutting-writing-rules)

---

## 1. Marketplace at a glance

| Plugin | Skill(s) | Category | What it does |
|---|---|---|---|
| **`ai-paper`** | `ai-paper` | writing | Write DL/GPR/geophysics/remote-sensing papers or single sections in Ge-style, with bundled paper and thesis templates. |
| **`arch-paper`** | `arch-paper` | writing | Write archaeological GPR (time-slice / depth-slice) papers in Goodman house style, with a five-tier interpretation discipline and per-section templates. |
| **`seismo-report`** | `seismo-report` | writing | Turn seismological data into a chapter-wise, publication-quality interpretation report with a formal title page and MD/HTML/LaTeX-PDF/DOCX output; detects the study type (event, waveform/FAS, source parameters, ground-motion, FWI, ambient noise) and builds the full chapter set. |
| **`research-gap`** | `research-gap` | research | Identify research gaps from uploaded papers or links and propose novel research projects. |
| **`compose-plan`** | `compose-plan` | planning | Generate a structured development plan (architecture + TODO) before any code is written. |
| **`paper-reviewer`** | `review` | review | Analyze a paper PDF as a rigorous journal reviewer and produce a comprehensive review report. |
| **`ppt-mkl`** | `ppt-mkl` | presentation | Turn one plain-text deck source into a **PPTX** (native editable equations), a **Beamer PDF**, a **.tex**, and a **.md** in a consistent lecture style. |
| **`doc-tools`** | `doc-readermkl`, `documentation-agent`, `md-updater`, `methods-read-doc` | docs | Read, maintain, update, and **explain** project and research docs; `methods-read-doc` builds beginner-accessible math explainers with PDF/DOCX output. |

**Repository layout**

```
skills_paper/
├── .claude-plugin/marketplace.json      # marketplace manifest (lists the plugins)
├── README.md
├── SKILLS_REPORT.md                     # this report
├── AI_humanization_writing_instructions.md   # shared human-voice writing rules
├── AI-Paper.md                          # standalone, self-contained ai-paper spec
├── thesis_guidelines_master.md          # version-independent thesis / report master template
└── plugins/
    ├── ai-paper/       plugin.json + skills/ai-paper/SKILL.md + templates/(+sections/)
    ├── arch-paper/     plugin.json + skills/arch-paper/SKILL.md + templates/(master, per_paper, sections, skill)
    ├── research-gap/   plugin.json + skills/research-gap/SKILL.md
    ├── compose-plan/   plugin.json + skills/compose-plan/SKILL.md
    ├── paper-reviewer/ plugin.json + skills/review/SKILL.md
    ├── ppt-mkl/        plugin.json + skills/ppt-mkl/SKILL.md + DECK_SPEC.md + template.deck + scripts/
    └── doc-tools/      plugin.json + skills/{doc-readermkl,documentation-agent,md-updater,methods-read-doc}/
```

Every plugin is authored by **Mrinal Kanti Layek — Geophysics & AI Lab, Chonnam National University**.

---

## 2. Install and use

Add the marketplace once, then install whichever plugins you want.

```text
/plugin marketplace add mklayek/skills_paper      # register this repo as a marketplace

/plugin install ai-paper@skills-paper             # paper writing
/plugin install arch-paper@skills-paper           # archaeological GPR writing
/plugin install research-gap@skills-paper         # research-gap analysis
/plugin install compose-plan@skills-paper         # project planning
/plugin install paper-reviewer@skills-paper       # journal-style paper review
/plugin install ppt-mkl@skills-paper              # research presentations
/plugin install doc-tools@skills-paper            # doc reading / maintenance / explainers

/plugin                                            # browse and manage installed plugins
/plugin marketplace update skills-paper            # pull the latest after new commits
```

Plugin names install as `<plugin>@skills-paper` (the marketplace name is `skills-paper`).

**Manual install (no marketplace):** clone the repo and copy any skill folder into `~/.claude/skills/`, keeping `SKILL.md` inside its named folder.

**Use without installing (any LLM):** the `ai-paper` rules are fully self-contained in `AI-Paper.md` and in `plugins/ai-paper/skills/ai-paper/templates/AI_Paper_Writing_Skill_complete.md`. Paste either into a chat as the rule-set.

---

## 3. ai-paper

**Skill:** `ai-paper` · **Trigger:** writing, drafting, or completing a DL / GPR / geophysics / computer-vision / remote-sensing paper or any of its sections, or finishing a partially written manuscript.

### What it does
Writes complete or partial technical manuscripts in the IEEE-TGRS scientific style of Ge et al. (2024). It enforces a fixed move-structure, global writing rules, gap-to-contribution alignment, and an explicit placeholder for unfinished work. The core principle is that structure and rules are non-negotiable, and only the domain content is filled in. It never fabricates results. Unfinished sections get an explicit `> 🚧 Yet to be developed.` marker rather than a plausible but fake table.

### Sub-skill files (the template library)
Read the template matching the section before drafting. Bundled under `skills/ai-paper/templates/`:

| File | Role |
|---|---|
| `AI_Paper_Writing_Skill_complete.md` | All rules plus every section inline (portable single file). |
| `MASTER_PAPER_template.md` | **Read first.** Global rules, full paper skeleton, and the unfinished-section policy. |
| `sections/INTRODUCTION_template.md` | Section I, six moves with gap-to-contribution alignment. |
| `sections/METHODOLOGY_template.md` | Section II: A data, B transform, C model, D loss and evaluation. |
| `sections/EXPERIMENTS_template.md` | Section III: A setup, B comparison, C ablation, D field application. |
| `sections/GENERALIZATION_FINETUNING_template.md` | Section IV, capability demonstration. |
| `sections/APPLICATION_DOWNSTREAM_template.md` | Section V, downstream application. |
| `sections/CONCLUSION_template.md` | Section VI, contribution-mirror recap. |

### How to use
1. Install `ai-paper@skills-paper`, then ask to write or finish a paper or a named section.
2. The skill reads `MASTER_PAPER_template.md` for the global rules and skeleton, then the matching section template.
3. Provide the domain content (method, dataset, results). Anything not yet available is marked `Yet to be developed`, never invented.
4. Output follows the fixed move-structure with numbered figures and tables, bolded best metric, and glossed equations.

---

## 4. arch-paper

**Skill:** `arch-paper` · **Trigger:** writing or structuring an archaeological GPR paper or section, time-slice/depth-slice survey reporting, buried-feature interpretation, or Goodman-style archaeological-geophysics prose.

### What it does
Drafts and structures archaeological GPR manuscripts on one governing principle: the reader is grounded in the archaeological and historical stakes first, the technique second, results are fused with interpretation, every claim is hedged to its evidentiary tier, and the paper closes by returning to the archaeological question. GPR is treated as instrumental to an archaeological end, never an end in itself. It synthesizes three Goodman-lineage source papers into one reusable IMRaD backbone with a canonical section order, a copy-paste skeleton, a **five-tier interpretation discipline**, and a humanization gate that runs on every sentence.

Mandatory rules include a `YYYY-MM-DD` date on the first line and a default author block, both overridable.

### Sub-skill files (templates)
Under `skills/arch-paper/templates/`:

- **`master/`** — `MASTER_TEMPLATE.md`, `global_rules_checklists.md`, `humanization_integration.md`, `comparison_report.md`.
- **`per_paper/`** — analyses of the three source papers: `paper1_goodman1995_analysis.md`, `paper2_goodman2011_analysis.md`, `paper3_goodman2014_analysis.md`.
- **`sections/`** — 17 numbered per-section templates from `00_title_authors_keywords.md` through `16_acknowledgements_supplementary.md` (abstract, introduction, study area, geological setting, materials and methods, acquisition, processing, equations, results, interpretation, discussion, conclusions, references, figures, tables).
- **`skill/`** — `arch-paper.md`, `usage_guide.md`, `implementation_notes.md`.

### When NOT to use
Non-archaeological geophysics with no buried-feature interpretation, a pure signal-processing or hardware paper, a modeling or simulation study with no site, or a literature review that is not a primary survey report.

### How to use
Install `arch-paper@skills-paper`, then ask to write the paper or a section. Supply site, antenna frequency, grid, targets, results, and figures. The skill emits the dated skeleton, fills sections in canonical order, and hedges every interpretive claim to its evidence tier.

---

## 5. research-gap

**Skill:** `research-gap` (internal name `research-gapmkl`) · **Trigger:** the user uploads papers, provides research links, or asks for gap analysis, literature review, or novel idea generation.

### What it does
Identifies and formulates novel research ideas by analyzing existing literature and detecting gaps. It works from uploaded PDFs, documents, or web links.

### Workflow
1. **Document analysis** — extract and summarize contributions, datasets, algorithms, and conclusions.
2. **Literature search** — search for closely related studies, recent publications, and known limitations.
3. **Gap detection** — compare against the broader landscape to surface knowledge gaps, unresolved problems, methodological limitations, and unexplored applications.
4. **Idea generation** — propose a unique idea built on the most promising gap.
5. **Proposal writing** — produce a structured research proposal document.

The skill coordinates internal sub-agents for the analysis, search, and synthesis stages.

### How to use
Install `research-gap@skills-paper`, then upload the source papers or paste links and ask for a gap analysis or a new project proposal.

---

## 6. compose-plan

**Skill:** `compose-plan` · **Trigger:** planning a new coding project, designing a geophysical workflow, or organizing a complex code-generation task.

### What it does
Generates a structured development plan **before any code is written**, for geophysics, GPR, seismic, and AI/ML scientific-computing projects. It produces a clear architecture and a TODO execution plan, not final code.

### What a plan contains
- Problem definition, algorithmic approach, and directory structure.
- **Scalability planning** (parallel data loading, GPU acceleration, batch processing, checkpointing, resume, logging).
- **Implementation phases** — Phase 1 structure, Phase 2 core algorithm, Phase 3 data pipeline, Phase 4 visualization and output, Phase 5 examples and testing, Phase 6 documentation. Each phase maps to TODO tasks.
- A **mathematical model section** when a scientific algorithm is involved (formulation, equations, parameter definitions, assumptions).

### Critical constraint
The skill **never** generates full code implementations. It only produces the plan. Code is generated later in separate steps.

### How to use
Install `compose-plan@skills-paper`, describe the project, and receive the architecture plus a phased TODO list to execute afterward.

---

## 7. paper-reviewer

**Skill:** `review` · **Command:** `/review` · **Trigger:** analyze a paper PDF as a journal reviewer.

### What it does
Analyzes an academic paper PDF as a rigorous journal reviewer and produces a comprehensive review report with major and minor comments, journal-guideline compliance checks, and section-by-section feedback.

### Input
Create a `review.json` in the project root and run `/review` with no arguments:

```json
{
  "pdf": "papers/my-paper.pdf",
  "journal": "Nature Communications",
  "url": "https://www.nature.com/ncomms/submit/guidelines",
  "guidelines": "guidelines/nature-comms.pdf",
  "refs": ["papers/ref1.pdf", "papers/ref2.pdf"],
  "lang": "en"
}
```

`pdf` and `journal` are required, and at least one of `url` or `guidelines` must be present. `refs` and `lang` are optional.

### Workflow (phased, multi-agent)
1. **Parse and validate** `review.json`.
2. **Collect data (Phase 0)** — load the journal guidelines (from URL or a downloaded PDF), read the target paper, and read any reference papers.
3. **Literature scout and journal-trend analysis (Phase 1)** — an internal Literature Scout agent extracts key terms, analyzes cited references, finds related papers, flags missing key references, and summarizes the domain context.
4. **Section-by-section review** — major and minor comments plus guideline-compliance checks.
5. **Generate the report.**

### How to use
Install `paper-reviewer@skills-paper`, add the PDF and (optionally) guideline and reference PDFs, write `review.json`, then run `/review`.

---

## 8. ppt-mkl

**Skill:** `ppt-mkl` · **Trigger:** build a research presentation, slide deck, PPTX, or Beamer PDF from a paper section, methods document, or report, especially in the MKL lecture style.

### What it does
One plain-text source (a `.deck` file) renders to **four** artefacts that all look the same: a **PPTX** with native editable Office-Math (OMML) equations, a **Beamer PDF**, a **.tex**, and a **.md**. The core principle is that equations are always native OMML, never faked with Unicode, so they stay editable and print correctly. The scripts handle this via pandoc.

### Sub-skill files
Under `skills/ppt-mkl/`:

| File | Role |
|---|---|
| `SKILL.md` | Overview, workflow, build commands, style contract, common mistakes, and the House writing rules. |
| `DECK_SPEC.md` | The strict deck mini-language: line prefixes, inline formatting, title rules, slide budget, and the mandatory equation-pretext rule. |
| `template.deck` | A worked example deck to copy and adapt. |
| `scripts/build_styled_slides.py` | Deck to PPTX (native OMML equations, styled bullets, figure with caption). |
| `scripts/deck_to_beamer.py` | Deck to Markdown, Beamer `.tex`, and Beamer PDF. Imports `build_styled_slides.py`, so keep both scripts together. |

### The deck mini-language (essentials)
| Line | Renders as |
|---|---|
| `# Section title` | Section-divider slide. |
| `== PREFIX : Title with **red** phrase` | New slide with an underlined title. |
| `- text` / `-- text` / `--- text` | Checkbox, red star, and small-dot bullet levels. |
| `$$ latex $$ (7)` | Centred equation with a red `---(7)` tag in the right margin. |
| `!key:` / `!so:` | Bold takeaway line / purple "Therefore…" intuition line. |
| `!fig: /abs/f.png 55% \| Figure 1. caption` | Bottom-anchored figure with an italic caption centred beneath it. |
| `!ref:` / `!note:` | Reference entry / speaker note. |
| Inline | `$math$`, `**maroon term**`, `==yellow highlight==`, `@@Author (year)@@` citation. |

**Equation pretext (mandatory):** every `$$…$$` is preceded by a `-` statement that names what the equation establishes, ending in a plain connecting phrase and a colon (for example `formulated as below:`, `described as:`, `given by:`). The builder warns on any missing lead-in, missing connector, bolded connector, or missing bold phrase, so a clean build has zero warnings.

### Build commands
```bash
S=<skill>/scripts
python3 $S/build_styled_slides.py talk.deck --out /abs/out/talk.pptx \
    --title "…" --subtitle "…" --author "…" --foot "short footer" [--no-date] [--no-page]
python3 $S/deck_to_beamer.py talk.deck --out-dir /abs/out --name talk \
    --title "…" --subtitle "…" --author "…" --foot "short footer" [--no-date] [--no-page]
```

`--no-date` and `--no-page` drop the date and the page number from the footer. Verify by rendering the PPTX to PDF and by checking the OMML equation count is non-zero.

### How to use
Install `ppt-mkl@skills-paper`, point the skill at a paper or methods section, let it author the `.deck`, then build both back-ends and review several rendered slides.

---

## 9. doc-tools

Four documentation skills in one plugin.

### 9a. doc-readermkl
**What it does:** reads, analyzes, and extracts information from documentation and research files. **Supported formats:** Markdown, text, PDF, Word (`.doc`, `.docx`), and spreadsheets (`.xls`, `.xlsx`). Use it whenever documents must be read and understood, specific information extracted, figures or references interpreted, or the user asks about content in project or uploaded files.

### 9b. documentation-agent
**What it does:** continuously maintains all project `.md` and `.txt` documentation. It modifies existing docs to match code changes, documents new scripts and features, keeps directory descriptions accurate, records workflow changes, and creates docs for new modules. Use it after significant code changes, new scripts, feature additions, or structure changes.

### 9c. md-updater
**What it does:** maintains the standard project documentation set whenever code or structure changes: `README.md` (overview, features, quick start, changelog summary), `Commands.md` (commands, CLI arguments, examples, return codes), `Installation.md` (environment setup), and a Manual. Works with `.md`, `.pdf`, and `.txt`.

### 9d. methods-read-doc
**What it does:** builds a self-contained, beginner-accessible companion to a technical or math section. It keeps every original equation verbatim and wraps it in layered explanation, so a non-specialist can follow the whole derivation while an expert still sees the exact math. Output is one Markdown file plus a matching PDF and DOCX, named `[Methods_read<NN>]_<YYYYMMDD>_<topic>.{md,pdf,docx}`.

**Per-equation anatomy (required, in order):**
1. The equation verbatim in `$$…$$` with its original `\tag{n}`, never renumbered.
2. `**Symbols in (n):**` a bulleted list defining every symbol, operator, subscript, superscript, constant, and notation construct.
3. `**Discussion.**` what the equation says and why it matters.
4. `**In simple terms:**` an expanded plain-language walkthrough of about 8 to 12 sentences.
5. `**Physical significance (<domain>):**` ties it to the real problem.

**Per-subsection:** `##### N. Title` headings, each closing with a rectangular **Key terms box** (a Markdown blockquote, concepts in `***bold italic***`), and an optional schematic (TikZ compiled to PNG).

**Sub-skill files** under `skills/methods-read-doc/`:

| File | Role |
|---|---|
| `SKILL.md` | The layered anatomy, document skeleton, writing style, and the strict `MD → TEX → PDF → DOCX` build order. |
| `build.md` | Copy-paste build recipe: pandoc to `.tex`, inject the preamble (mdframed boxes, 1.15 spacing, `newunicodechar`), compile twice, then build the DOCX. |
| `make_refbox.py` | Builds `refbox15.docx`, a reference DOCX with a bordered "Block Text" box style and 1.15-spaced Normal. |
| `references/AI_humanization_writing_instructions.md` | The human-voice writing rules applied to every added sentence. |

**Build order (strict):** MD → TEX → PDF → DOCX. The PDF is compiled from the generated `.tex`, not straight from Markdown. For a large section, split by part across subagents, then stitch preamble plus parts plus the equation index and references, and verify the `\tag` count matches the source with no duplicates.

### How to use
Install `doc-tools@skills-paper`. Ask to read or summarize a document (`doc-readermkl`), keep docs in sync after code changes (`documentation-agent`, `md-updater`), or produce a dumbed-down but detailed math explainer with a matching PDF and DOCX (`methods-read-doc`).

---

## 10. seismo-report

**Plugin:** `seismo-report` · **Skill:** `seismo-report` · **Category:** writing

Modeled on `arch-paper`, but for **seismology**. It turns whatever inputs exist — figures (waveforms, spectrograms, Fourier amplitude spectra, response spectra, focal mechanisms, station maps, time histories, FWI model panels), Markdown notes, PDFs, CSV/XLSX tables, and published papers — into a comprehensive, chapter-wise interpretation report. The guiding principle is interpretation over description: it reads the data for what it implies about the source, path, and site, and reasons toward a conclusion.

**Report-type detection.** The skill first classifies the study (earthquake event analysis, seismic hazard, waveform analysis, source-parameter estimation, ground-motion simulation, **FWI results**, ambient-noise analysis, or GPR-seismic comparison) via `templates/report_type_classifier.md`, then builds the chapter set that fits.

**Chapters.** The full ordered set (`templates/MASTER_REPORT_TEMPLATE.md`): Title Page, Index, Executive Summary, Table of Contents, Introduction, Objectives, Background, Study Area, Dataset Description, Instrumentation, Methodology, Mathematical Background, Data Processing Workflow, Results, Figures and Tables, Interpretation, Discussion, Validation, Comparison with Published Studies, Conclusions, Limitations, Future Work, References, Appendices, Glossary, Abbreviations. Any chapter without supporting input keeps its heading and reads **`Yet to be developed`**. Every abbreviation and symbol is defined on first use, and per-input interpretation recipes live in `templates/per_analysis_protocols.md`.

**Title page.** A formal, centered title page with an auto-generated title, the date, optional project info and document version, and a fixed author block (Dr. Mrinal Kanti Layek, Geophysics & AI Lab, Chonnam National University — with the Korean affiliation line), from `templates/title_page.md`.

**Formatting.** DOCX and PDF render in **Times New Roman 12 pt, 1.15 line spacing, first-line indent, justified**, with a styled heading hierarchy (section bold 16 pt → sub-section 14 pt → sub-sub-section 13 pt → paragraph 12 pt regular → sub-paragraph 12 pt italic) and Korean-aware fonts (Malgun Gothic on DOCX via the East-Asian font, xeCJK on PDF). Headings are authored as ATX Markdown so pandoc maps them to real Word/LaTeX heading styles with automatic section numbering and a table of contents. The single source of truth is `templates/formatting_spec.md`, implemented by `scripts/make_reference_docx.py` (the DOCX style reference), `scripts/preamble_seismo.tex` (xelatex), and `scripts/seismo.css` (HTML).

**Build order.** `scripts/build_report.py` produces outputs in a fixed order: Markdown master → HTML → figures → **user approval** → LaTeX → PDF → optional DOCX and PPTX (PDF/DOCX are gated behind explicit flags so nothing renders before approval). Writing style follows `reference/AI_humanization_writing_instructions.md` (US English, no em dashes, first-line indent, varied openers, equations in `$…$`, real author-date citations). There is **no page limit**.

**How to run (Windows / PowerShell):**

```powershell
& "$env:USERPROFILE\.conda\envs\seismo\python.exe" `
    <skill>\scripts\build_report.py REPORT.md --html            # HTML (safe, pre-approval)
& "$env:USERPROFILE\.conda\envs\seismo\python.exe" `
    <skill>\scripts\build_report.py REPORT.md --pdf --docx      # after approval
```

Dependencies: pandoc, python-docx, and a xelatex engine (MiKTeX/TeX Live). A worked example lives in `examples/example_fwi_report/`, and the whole specification is duplicated in `seismo-report.md` for standalone use.

---

## 11. Cross-cutting writing rules

Enforced by `ai-paper` and shared across the writing and doc skills. The full human-voice rule-set is in **`AI_humanization_writing_instructions.md`** at the repo root.

- **US English.** Acronyms as `full name (ACRONYM)` on first use, one term per concept.
- **Tense.** Present for design and facts, past for what was done.
- **Equations.** `$…$` / `$$…$$` with `\tag{n}` inside the block, every symbol glossed. Never `\(...\)`, `\[...\]`, or a bare `\begin{equation}`.
- **Figures and tables.** Numbered in order (tables in Roman), referenced before they appear, the proposed method placed last, the best metric bolded.
- **Punctuation and voice.** Replace em dashes and parenthetical asides, avoid semicolons in casual prose, remove mid-sentence ellipses, use colons sparingly, vary sentence starts, and prefer simple words.
- **No fabrication.** Unrun work gets `> 🚧 Yet to be developed.` with Planned content and Depends-on notes, never a fake table.

---

*Author of the marketplace and all plugins: Mrinal Kanti Layek — Geophysics & AI Lab, Department of Energy & Resources Engineering, Chonnam National University.*
