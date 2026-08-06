---
name: seismo-report
description: Use when writing, drafting, or structuring a scientific interpretation report of seismological data (earthquake event analysis, waveform/FAS/response-spectra analysis, source-parameter estimation, ground-motion simulation, FWI results, ambient-noise study, GPR-seismic comparison) from a set of figures, MD notes, PDFs, CSV/XLSX, or a published paper, and when turning those into a publication-quality chapter-wise technical report, journal manuscript basis, project report, or PhD thesis chapter with a formal title page and MD/HTML/LaTeX-PDF/DOCX output.
---

# seismo-report

## Overview

&nbsp;&nbsp;&nbsp;&nbsp;This skill writes a comprehensive, publication-quality seismological interpretation report from whatever inputs exist, which are figures, Markdown notes, PDFs, CSV or Excel tables, and published papers. The governing principle is interpretation over description. The report explains the physics, reads the waveforms and spectra for what they imply about the source, path, and site, and reasons toward a conclusion rather than narrating axes and colours. It reads as though an experienced seismologist prepared it. The report is chapter-wise, every abbreviation and symbol is defined on first use, every figure sits at the start of its section, and the whole document passes the humanization gate on every sentence. There is no page limit.

## When to use

- The user asks to write, draft, or structure a seismological report, technical report, manuscript basis, or thesis chapter from figures, notes, tables, or a paper.
- The inputs are seismic figures such as waveforms, spectrograms, Fourier amplitude spectra, response spectra, focal mechanisms, station maps, time histories, or FWI model panels, plus any MD, PDF, CSV, or XLSX context.
- The user wants scientific interpretation and reasoning, not a caption list.

Do NOT use this skill for a pure code-documentation task, a non-seismological report, or a bare figure-caption set with no interpretive intent.

## Mandatory rules

- The document begins with the current date on line one in `YYYY-MM-DD` form.
- A formal title page with the fixed bilingual author block always follows the date. See `templates/title_page.md`.
- The Index comes right after the title page.
- Report-type detection runs first, before any chapter is drafted, to pick the emphasized chapter set. See `templates/report_type_classifier.md`.
- Figures sit at the start of each section, ahead of the continuous interpretive prose. See `templates/figures_and_captions.md`.
- Any chapter without supplied content keeps its heading and reads `Yet to be developed`, verbatim. All other chapters are still completed.
- Every abbreviation, symbol, and variable is expanded on first appearance. No abrupt logical jumps.
- The humanization gate applies to every sentence, including captions and table notes. See `templates/humanization_gate.md`.
- Interpretation over description throughout. Each observation carries its physical reasoning and significance for the source, path, or site.
- Outputs build in this order and no earlier: Markdown master, then HTML, then figures, then the user approval checkpoint, then LaTeX, then PDF, then optional DOCX and PPTX on request. See `scripts/build_report.py`.
- The HTML deliverable is the **web style**: one self-contained page with a fixed LEFT docked Table of Contents (scrollspy highlights the current section), a floating toolbar (Contents / Print-PDF / Full-width / A-/A+ / Top / Reset), click-to-zoom lightbox on every figure, light theme, Times New Roman body, embedded high-resolution figures, and **offline MathJax (SVG)** equations with the right-click Contextual Menu and right-aligned `\tag{N}` numbers. Build it with `to_html` in `scripts/build_report.py`. See `templates/html_web_style.md` for the full spec and the MathJax gotchas (SVG bundle, no autoload-only macros such as `\boldsymbol`, `$$ ... \tag{N}$$` numbering, and the finalize step that makes MathJax render offline).
- The DOCX export is Times New Roman, 12 pt, 1.15 line spacing, first-line paragraph indent, and justified alignment, with the full heading hierarchy. See `templates/formatting_spec.md`.
- Chapters and sections are authored as ATX Markdown headings (`#` through `#####`), styled per the descending hierarchy in `templates/formatting_spec.md`, never as bold or italic pseudo-headings. Pick ONE numbering scheme and hold it across all exports: either automatic (`--number-sections`, no manual prefix in the heading text) or manual (write `## 6.2 ...` and drop `--number-sections` everywhere so nothing double-numbers). The web-style HTML (`to_html`) uses manual heading numbers, so when it is the target, author the numbers into the headings and keep `--number-sections` off for DOCX/PDF too.
- There is no page limit. The skill never truncates chapters to fit a length target.

## Chapter map

Chapters below are authored as ATX headings (`#`) styled and auto-numbered per `templates/formatting_spec.md`; the numbers in this table are reference labels only, not literal heading text.

| Chapter | What to write |
|---|---|
| 1. Title Page | The formal title page block from `templates/title_page.md`, with the fixed author block. |
| Index | Table of contents listing every chapter, page numbers finalized on export. |
| 2. Executive Summary | One block covering study type, data, headline result, and main interpretation. |
| 3. Table of Contents | Auto-generated on export; a placeholder note in the Markdown master. |
| 4. Introduction | Seismological context, the event/region/problem, the knowledge gap, a roadmap sentence. |
| 5. Objectives | The specific questions the study answers. |
| 6. Background | Theory and prior work needed to read the results. |
| 7. Study Area | Location, tectonic setting, station geometry, site conditions. |
| 8. Dataset Description | What data and figures exist, counts, time span, components, bands. |
| 9. Instrumentation | Sensors, sampling rate, response, network, positioning. |
| 10. Methodology | The analysis approach end to end. |
| 11. Mathematical Background | Equations with every symbol defined, assumptions, physical meaning. |
| 12. Data Processing Workflow | The ordered chain: instrument correction, detrend, taper, filter, rotation, windowing. |
| 13. Results | The measured outcomes, figures first, numbers stated. |
| 14. Figures and Tables | The numbered inventory and captions. |
| 15. Interpretation | What the results mean for source, path, and site, with reasoning. |
| 16. Discussion | Synthesis, implications, engineering significance. |
| 17. Validation | Checks against independent data or known solutions. |
| 18. Comparison with Published Studies | Real author-date comparisons. |
| 19. Conclusions | The generalized contribution, back to the objectives. |
| 20. Limitations | Data, method, and resolution bounds. |
| 21. Future Work | Concrete next steps. |
| 22. References | Author-date, alphabetical, real works only, else `Yet to be developed`. |
| 23. Appendices | Parameter tables, extra figures, else `Yet to be developed`. |
| 24. Glossary | Defined terms. |
| 25. Abbreviations | Expansions of every abbreviation used. |

## Workflow

1. Gather every input, which are figures, MD, PDF, CSV, XLSX, and any paper. Read them.
2. Classify the report type with `templates/report_type_classifier.md` and pick the chapter set.
3. Emit the dated skeleton from `templates/MASTER_REPORT_TEMPLATE.md`, title page first via `templates/title_page.md`, then the Index.
4. Place each section's figures first, then write the continuous interpretive body.
5. Add the quantitative summaries and tables from `templates/quantitative_summary.md`.
6. Run the humanization gate from `templates/humanization_gate.md` on every paragraph.
7. Build outputs in order with `scripts/build_report.py`: Markdown, then HTML, then figures, then STOP for user approval. After approval, LaTeX, then PDF, then optional DOCX and PPTX.
8. Maintain the supporting files from `templates/supporting_files.md`.

## Reference files

- `templates/MASTER_REPORT_TEMPLATE.md` - the full chapter skeleton with placeholders.
- `templates/title_page.md` - the formal title page and the fixed author block.
- `templates/formatting_spec.md` - heading hierarchy and DOCX/LaTeX/HTML formatting.
- `templates/humanization_gate.md` - the enforceable per-sentence writing rules.
- `templates/report_type_classifier.md` - report-type detection and chapter selection.
- `templates/per_analysis_protocols.md` - per-input interpretation recipes.
- `templates/figures_and_captions.md` - the figures-at-section-start contract and captions.
- `templates/quantitative_summary.md` - required numeric summaries and tables.
- `templates/supporting_files.md` - REPORT.md, HANDOUT.md, glossary, abbreviations, equation index, bibliography, figure inventory, and processing log.
- `scripts/build_report.py` - the MD → HTML → LaTeX/PDF → DOCX/PPTX build orchestrator.

## Quality checklist

- [ ] Document begins with the current date, then the title page with the fixed author block.
- [ ] Report type was classified and the chapter set matches it.
- [ ] Every chapter is present and in order; missing ones read `Yet to be developed`.
- [ ] Figures sit at the beginning of each section; each body is continuous interpretive prose.
- [ ] Every abbreviation, symbol, and equation term is defined on first use.
- [ ] Quantitative summaries and tables appear where the data supports them.
- [ ] Humanization gate passed: US English, no em dashes, minimal semicolons/commas, varied openers, no numbered lists in prose, equations in `$...$`, paragraphs indented.
- [ ] Outputs built in order; LaTeX/PDF/DOCX only after the user approved the HTML.
- [ ] DOCX is Times New Roman 12 pt, 1.15 spacing, first-line indent, justified, with the heading hierarchy.
