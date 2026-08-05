# seismo-report — Specification & Usage Document

&nbsp;&nbsp;&nbsp;&nbsp;This document is the standalone specification for the `seismo-report` skill. It exists as a companion to `SKILL.md`, which carries the trigger and the operative in-session instructions, so that the full rule set is also readable and runnable outside a Claude session, as project documentation, and as an onboarding reference for anyone extending the skill.

## 1. Purpose

&nbsp;&nbsp;&nbsp;&nbsp;The skill turns whatever seismological inputs exist into a comprehensive, chapter-wise, publication-quality report with a formal title page and a controlled Markdown-to-output build pipeline. The governing principle is interpretation over description. The report explains the physics, reads the waveforms and spectra for what they imply about the source, path, and site, and reasons toward a conclusion rather than narrating axes and colors. It reads as though an experienced seismologist prepared it, and it carries no page limit.

## 2. Accepted input kinds

&nbsp;&nbsp;&nbsp;&nbsp;The skill accepts any combination of the following, and gathers all of them before writing a single chapter.

- Figures — waveforms, spectrograms, Fourier amplitude spectra (FAS), response spectra, focal mechanisms, station maps, time histories, or full-waveform inversion (FWI) model panels.
- Markdown notes describing prior analysis, processing steps, or findings.
- PDF documents, including prior reports or literature.
- CSV or Excel (XLSX) tables of event parameters, station metadata, or measured quantities.
- Published papers, cited in the Comparison and References chapters using real author-date entries.

## 3. Report-type list

&nbsp;&nbsp;&nbsp;&nbsp;`templates/report_type_classifier.md` reads the gathered inputs and assigns one primary type, which sets the emphasized chapter subset while the full chapter list from Section 4 stays present regardless. The eight recognized types are earthquake event analysis, seismic hazard study, waveform analysis, source-parameter estimation, ground-motion simulation, FWI results, ambient-noise analysis, and GPR-seismic comparison. When several types apply, the dominant one is named in the Executive Summary and the union of emphasized chapters is kept. When none fits cleanly, the classifier defaults to earthquake event analysis and notes the ambiguity in the text.

## 4. Complete chapter list

&nbsp;&nbsp;&nbsp;&nbsp;Every report carries all twenty-five chapters below, in this order, sourced from `templates/MASTER_REPORT_TEMPLATE.md`. A chapter with no supporting input keeps its heading and reads `Yet to be developed`, verbatim, rather than being omitted.

| # | Chapter | What it carries |
|---|---|---|
| 1 | Title Page | The formal title page block from `templates/title_page.md`, with the fixed author block. |
| — | Index | Table of contents listing every chapter, page numbers finalized on export. |
| 2 | Executive Summary | Study type, data, headline result, main interpretation, in one block. |
| 3 | Table of Contents | Auto-generated on export; a placeholder note in the Markdown master. |
| 4 | Introduction | Seismological context, the event/region/problem, the knowledge gap, a roadmap sentence. |
| 5 | Objectives | The specific questions the study answers. |
| 6 | Background | Theory and prior work needed to read the results. |
| 7 | Study Area | Location, tectonic setting, station geometry, site conditions. |
| 8 | Dataset Description | What data and figures exist, counts, time span, components, bands. |
| 9 | Instrumentation | Sensors, sampling rate, response, network, positioning. |
| 10 | Methodology | The analysis approach end to end. |
| 11 | Mathematical Background | Equations with every symbol defined, assumptions, physical meaning. |
| 12 | Data Processing Workflow | The ordered chain: instrument correction, detrend, taper, filter, rotation, windowing. |
| 13 | Results | The measured outcomes, figures first, numbers stated. |
| 14 | Figures and Tables | The numbered inventory and captions. |
| 15 | Interpretation | What the results mean for source, path, and site, with reasoning. |
| 16 | Discussion | Synthesis, implications, engineering significance. |
| 17 | Validation | Checks against independent data or known solutions. |
| 18 | Comparison with Published Studies | Real author-date comparisons. |
| 19 | Conclusions | The generalized contribution, back to the objectives. |
| 20 | Limitations | Data, method, and resolution bounds. |
| 21 | Future Work | Concrete next steps. |
| 22 | References | Author-date, alphabetical, real works only, else `Yet to be developed`. |
| 23 | Appendices | Parameter tables, extra figures, else `Yet to be developed`. |
| 24 | Glossary | Defined terms. |
| 25 | Abbreviations | Expansions of every abbreviation used. |

## 5. Formatting rules

&nbsp;&nbsp;&nbsp;&nbsp;The formatting contract, sourced from `templates/formatting_spec.md`, applies identically across DOCX, PDF, and HTML export, so the reader sees the same document regardless of the output chosen.

- Body text is Times New Roman, 12 pt, with Korean runs set in an East-Asian font (Malgun Gothic) so 한글 renders correctly wherever the author block appears.
- Line spacing is 1.15 (multiple) throughout the body.
- The first line of every paragraph is indented 0.5 in. No indent is applied inside tables.
- Body text is justified.
- The heading hierarchy descends in emphasis by level: Section (`#` / `**1. X**`) is 16 pt bold, matching Word Heading 1 and LaTeX `\section`; Sub-section (`##`) is 14 pt bold, Heading 2, `\subsection`; Sub-sub-section (`###`) is 13 pt bold, Heading 3, `\subsubsection`; Paragraph (`####`) is 12 pt regular weight, not bold, Heading 4, `\paragraph`; Sub-paragraph (`#####`) is 12 pt italic, Heading 5, `\subparagraph`. Section titles run one to two points bolder and bigger than the body, and each deeper level carries a visibly different format, ending in a regular-weight paragraph head and an italic sub-paragraph head.
- Figures, tables, and equations are numbered automatically. Figures are "Figure N" in order of first in-text mention, tables are "Table N", equations are "(N)". Captions sit under figures and above tables.
- Sections are auto-numbered on export through pandoc's `--number-sections`.

## 6. The fixed author block

&nbsp;&nbsp;&nbsp;&nbsp;Every title page carries this block, verbatim, unless the user explicitly overrides it:

```
Dr. Mrinal Kanti Layek
Postdoctoral Researcher | 박사후 연구원
Geophysics & AI Lab, Department of Energy & Resources Engineering,
Chonnam National University, Gwangju, Republic of Korea [61186]
지구물리 및 인공지능 연구실, 에너지자원공학과, 전남대학교, 광주광역시, 대한민국 [61186]
Email — layek.mk@gmail.com
Mrinal Kanti Layek — github.com/mklayek
```

## 7. Build order (contract)

&nbsp;&nbsp;&nbsp;&nbsp;Outputs are produced in a fixed sequence and never out of order, since the whole point of the checkpoint is that nothing downstream of HTML gets built on unreviewed prose.

1. Markdown master — the authored `report.md` (or `REPORT.md`), following the chapter list in Section 4 and the humanization gate.
2. HTML — rendered from the Markdown with `scripts/build_report.py --html`, always allowed, and the first artifact the user reviews.
3. Figures — copied and numbered into the report's `figs/` directory per `templates/figures_and_captions.md`.
4. User approval checkpoint — the user reviews the HTML (and the figures) before anything else is built. This step is mandatory and is never skipped.
5. LaTeX — the xelatex header include from `scripts/preamble_seismo.tex` is applied through pandoc, after approval only.
6. PDF — compiled from the Markdown with `scripts/build_report.py --pdf`, after approval only.
7. Optional DOCX and PPTX, on request — `scripts/build_report.py --docx` and `--pptx`, after approval only.

## 8. Supporting-file list

&nbsp;&nbsp;&nbsp;&nbsp;The skill maintains a small family of supporting files alongside the report, each documented as a template in `templates/supporting_files.md`.

- `REPORT.md` — the master editable report.
- `HANDOUT.md` — continuation memory across sessions.
- `figure_inventory.md` — the numbered figure list with source paths and captions.
- `bibliography.md` — author-date entries, real works only.
- `glossary.md` — defined terms.
- `abbreviations.md` — expansions of every abbreviation used.
- `equation_index.md` — numbered equations with page or section reference.
- `processing_log.md` — dated build actions.

## 9. How to run (PowerShell)

&nbsp;&nbsp;&nbsp;&nbsp;The build orchestrator is `scripts/build_report.py`, called through the `seismo` conda environment's interpreter. HTML is always allowed; DOCX, PDF, and PPTX are gated behind explicit flags so the approval checkpoint in Section 7 is enforced by the tool itself, not only by convention.

```powershell
# From the directory containing report.md
& "$env:USERPROFILE\.conda\envs\seismo\python.exe" `
  "C:\Users\user\.claude\skills\seismo-report\scripts\build_report.py" `
  report.md --html

# After the user approves the HTML, build the remaining outputs on request
& "$env:USERPROFILE\.conda\envs\seismo\python.exe" `
  "C:\Users\user\.claude\skills\seismo-report\scripts\build_report.py" `
  report.md --docx --pdf --pptx
```

&nbsp;&nbsp;&nbsp;&nbsp;To regenerate the DOCX style reference used by `--docx` (`scripts/reference_seismo.docx`), run `make_reference_docx.py` directly:

```powershell
& "$env:USERPROFILE\.conda\envs\seismo\python.exe" `
  "C:\Users\user\.claude\skills\seismo-report\scripts\make_reference_docx.py"
```

&nbsp;&nbsp;&nbsp;&nbsp;To run the skill's test suite:

```powershell
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD=1
& "$env:USERPROFILE\.conda\envs\seismo\python.exe" -m pytest `
  "C:\Users\user\.claude\skills\seismo-report\tests" -q
```

## 10. Implementation notes

&nbsp;&nbsp;&nbsp;&nbsp;Each template and script has a single, narrow responsibility, so a change to one rule touches one file.

- `templates/MASTER_REPORT_TEMPLATE.md` — the full chapter skeleton, Title Page through Abbreviations, with the date-on-line-one header and the fill-instruction placeholders for every chapter.
- `templates/title_page.md` — the copy-paste title page block and the Index block, plus the notes on how the author block renders across export formats.
- `templates/humanization_gate.md` — the enforceable per-sentence writing rules: no em dashes, minimal semicolons and commas, first-line paragraph indent, varied sentence openers, no numbered lists inside prose, equations in `$...$`, real author-date in-text references.
- `templates/formatting_spec.md` — the single source of truth for heading sizes and weights and body formatting, implemented identically by `make_reference_docx.py`, `preamble_seismo.tex`, and `seismo.css`.
- `templates/report_type_classifier.md` — the decision table mapping observed inputs to a primary report type and its emphasized chapters.
- `templates/per_analysis_protocols.md` — the interpretation recipe for each figure or data kind, from waveforms and Fourier amplitude spectra through focal mechanisms and FWI model panels, each naming what to read and the physical reasoning to attach.
- `templates/figures_and_captions.md` — the figures-at-section-start structural contract and the caption style, including the requirement that every caption carry at least one measured value with units.
- `templates/quantitative_summary.md` — the recurring seismological quantities to report where the data supports them, with example tables.
- `templates/supporting_files.md` — the templates and one-line purpose for each file in Section 8.
- `scripts/make_reference_docx.py` — builds `reference_seismo.docx`, exposing `build_reference(out_path: Path) -> Path`, tested by `tests/test_reference_docx.py`.
- `scripts/build_report.py` — the orchestrator, exposing `to_html`, `to_docx`, and `to_pdf`, plus the CLI described in Section 9, tested by `tests/test_build_report.py`.
- `scripts/preamble_seismo.tex` — the xelatex header include for the PDF path, mirroring the heading hierarchy from `formatting_spec.md`.
- `scripts/seismo.css` — the HTML stylesheet, mirroring the same heading hierarchy and body formatting for the HTML path.
- `examples/example_fwi_report/` — a worked example (`report.md` plus `figs/fig1_model_grid.png`) that exercises the title page, one interpreted Results chapter, and the HTML/DOCX build in one pass.
- `tests/` — `test_reference_docx.py` asserts the DOCX styles match `formatting_spec.md`; `test_build_report.py` asserts HTML and DOCX get produced from a minimal Markdown master through pandoc.

---

Dr. Mrinal Kanti Layek
Postdoctoral Researcher | 박사후 연구원
Geophysics & AI Lab, Department of Energy & Resources Engineering,
Chonnam National University, Gwangju, Republic of Korea [61186]
지구물리 및 인공지능 연구실, 에너지자원공학과, 전남대학교, 광주광역시, 대한민국 [61186]
Email — layek.mk@gmail.com
Mrinal Kanti Layek — github.com/mklayek
