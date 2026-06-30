# 📐 Thesis / Technical-Report Guidelines — MASTER TEMPLATE

> **Status:** canonical, version-independent master. **Do not delete.**
> **Purpose:** the standard rule-set and structure for every project report, technical report,
> dissertation, project handbook, model documentation, and thesis-style document archived under
> `/nas/DATA1/GPRutility_simulations/C_codes/`.
> **Reusable across:** AI, GPR, seismic, inversion, machine-learning, and software-development projects.

## How to use this master (archival convention)

1. Whenever a new project is archived into `/C_codes`, **generate a project-specific copy**:
   ```
   thesis_guidelines_{version}_{date}_{time}.md
   # e.g. thesis_guidelines_wgan_pipe_v3_20260614_143000.md
   ```
   Place the copy in `/C_codes/` (and optionally inside the project archive folder).
2. Keep this `thesis_guidelines_master.md` as the **untouched canonical source**. Copies are
   derived from it and may be populated with project-relevant details; the master stays generic.
3. The project report itself (the thesis) lives **inside** the archive folder
   (`<archive>/<project>_thesis.md`), built to the structure defined here.
4. Filenames carry full provenance: `{project/version}_{date YYYYMMDD}_{time HHMMSS}`. Convert any
   relative dates to absolute. Time is 24-hour, local timezone noted in the document header.

---

# 1. Document Philosophy

| Principle | What it means in practice |
|---|---|
| **Reproducibility first** | Every claim must be runnable: exact commands, seeds, paths, versions. A reader with the archive and the environment file can re-derive every result. |
| **Long-term archival suitability** | Assume the report is opened years later, possibly on different hardware, by someone with **no prior context**. Avoid ephemeral references ("the usual script"); spell everything out. |
| **Self-contained reporting** | The document + its archive folder are sufficient on their own. No dependency on chat logs, tribal knowledge, or a live machine. |
| **Future-researcher readability** | Engineering-level explanations, structured headings, tables, captions, numbered equations, emoji/visual cues where they aid scanning — but never at the cost of precision. |
| **Publication readiness** | Math, figures, and structure should be close enough to journal/dissertation quality that sections can be lifted into a paper with minimal rework. |
| **Honesty over polish** | Document failure modes, regressions, and limitations explicitly. A faithful "this broke at epoch N" is more valuable than an airbrushed success story. Never fabricate numbers, folds, or results. |

---

# 2. Standard Report Structure

Every thesis-style report should contain these blocks, in order (expand/merge as the project needs,
but do not silently drop a block — mark it *N/A* with a one-line reason if it genuinely does not apply):

1. **Title page** — project/version name, quality tag, archive name + root path, date, author,
   affiliation, method/origin reference, best-model one-liner.
2. **Executive summary** — a **one-page** standalone summary on the first page (what it is, how it
   works, what's new, the headline result, the key caveat, how to reproduce).
3. **Table of contents.**
4. **Project overview** — objective, key objectives, contributions, version summary, archive info.
5. **Problem statement** — the precise task, inputs/outputs, constraints, success criteria.
6. **Literature / research context** — prior work, the method's origin, why this approach.
7. **Methodology** — end-to-end workflow, design philosophy, pipelines (train/val/inference).
8. **Mathematics** — losses, objectives, optimization, regularization, with numbered equations.
9. **Architecture** — high-level + layer-by-layer, blocks, normalization, skip/feature flow.
10. **Implementation** — software architecture, key modules, configuration, environment.
11. **Experiments** — setup, parameters, datasets, commands, per-experiment observations.
12. **Results** — quantitative + qualitative + visual; tables and curves.
13. **Discussion** — interpretation, what worked, why, comparison with previous versions.
14. **Limitations** — honest scope and failure modes.
15. **Conclusions.**
16. **Future work.**
17. **References.**
18. **Appendices** — full commands, configs, dataset paths, folder trees, extra figures/tables.

---

# 3. Mandatory Technical Sections

A complete report **must** include all of the following (each with subsections, tables, figures,
equations, source paths, examples, and implementation notes as relevant):

- **Algorithm description** — overview, design philosophy, component workflows, advantages,
  limitations.
- **Mathematical formulations** — every loss/objective written out, symbols defined, numbered.
- **Architecture diagrams** — overall network, generator/encoder, discriminator/decoder, blocks.
- **Workflow diagrams** — training, validation, inference, data generation, loss flow.
- **Source-code inventory** — every important script: purpose, inputs, outputs, full path.
- **Dataset inventory** — every dataset: source, counts, format, splits, full path.
- **Configuration inventory** — all hyperparameters and where they live (launcher/argparse/YAML).
- **Hardware details** — CPU/GPU model, count, memory, driver.
- **Software environment** — language, framework, CUDA/cuDNN, library versions, OS.
- **Training commands** — primary, resume, multi-GPU, alternatives (canonical, grouped form).
- **Inference commands** — single, batch, test-dataset paths, output locations.
- **Reproducibility guide** — environment → data → train → validate → infer → troubleshoot.

---

# 4. Documentation Rules

- **Every major script must be explained** — its role in the pipeline, not just its name.
- **Every important folder must be described** — what it holds and why.
- **All paths must be documented** — absolute paths; note local-scratch vs NAS vs archive copies.
- **All datasets must include source information** — origin, how produced, counts, format, splits.
- **All checkpoints must be traceable** — version, epoch, selection metric value, file path, and the
  exact config/architecture flags needed to load them.
- **All figures must have captions** — what it shows, axes/units, which checkpoint/epoch produced it.
- **All tables must have titles** — and clear column headers with units.
- **All equations must be numbered** where appropriate, and every symbol defined on first use.
- **No silent gaps** — if a standard section does not apply, state *N/A* with a one-line reason
  (e.g. "no k-fold: single seeded 90/10 split").

---

# 5. Figure Guidelines

Recommended figure set (include those that apply; caption every one):
- **Architecture figures** — overall network; per-branch/sub-network detail; block internals.
- **Workflow figures** — training loop; inference pipeline; data-generation flow; loss-flow diagram.
- **Result figures** — representative input→output examples; success cases.
- **Comparison figures** — vs previous versions; vs baselines; ablations.
- **Training curves** — loss(es) and learning rate vs epoch.
- **Validation curves** — selection metric vs epoch, best-epoch marked.
- **Inference examples** — real-data examples, including **failure cases**.

**Formatting:** publication-quality — readable fonts, labeled axes with units, consistent
colormaps/scales across compared panels, legible at print size. ASCII diagrams are acceptable inside
markdown for portability, but reference the high-resolution PNG/PDF assets stored in the archive.
Each figure gets a number and a caption (`**Figure N.** …`).

---

# 6. Mathematical Documentation Rules

- **Define symbols** — maintain a notation block; define each symbol on first use.
- **Define variables** — shapes/ranges/units for tensors and scalars (e.g. `T ∈ [0,1]^{1×256×256}`).
- **Explain assumptions** — modeling assumptions (e.g. additive `D = T + C + N`), data ranges,
  independence/detach choices.
- **Provide derivations where possible** — at least the optimization update and how gradients flow.
- **Discuss significance of equations** — what each term does, why its weight, expected effect on
  training. Number equations `(1), (2), …` and reference them in the text.

---

# 7. Experiment Documentation Rules

Document each experiment/run with this fixed schema:
- **Objective** — the question the run answers.
- **Setup** — model/version, environment, hardware.
- **Parameters** — full hyperparameters (or a diff vs the canonical config).
- **Datasets** — which data, split, counts, paths.
- **Commands** — exact, copy-pasteable, canonical grouped form.
- **Outputs** — checkpoints, logs, figures, and their paths.
- **Observations** — what happened, including anomalies and regressions.
- **Conclusions** — what to keep, what to change next.

---

# 8. Source-Code Documentation Rules

For every important file, record:
- **File purpose** — one-paragraph role in the system.
- **Inputs** — arguments, data formats, expected paths.
- **Outputs** — produced files/objects and their formats/locations.
- **Dependencies** — libraries and other project modules it relies on.
- **Usage examples** — a runnable invocation.
- **Full source path** — live path and archived path.

---

# 9. Results Documentation Rules

- **Quantitative results** — metric tables with units; best value bolded; selection criterion stated.
- **Qualitative results** — described behavior (e.g. "selective declutter; blanks empty scenes").
- **Visual results** — captioned example figures.
- **Failure cases** — explicit; the most useful part of an honest report.
- **Strengths / weaknesses** — balanced summary.
- **Comparison with previous versions** — a version table with the headline metric and verdict.

---

# 10. Archival Rules

Each archive under `/C_codes/000_<project>_<version>_<date>_<tag>/` must contain:
- **Code snapshot** — full repo, excluding caches (`__pycache__`, `*.pyc`, `.git`).
- **Documentation snapshot** — all `docs/`, README/HANDOUT/CHANGELOG/CLAUDE, plans, specs.
- **Configuration snapshot** — launchers + argparse defaults (and any YAML/JSON); checkpoints embed a
  `config` dict.
- **Environment information** — `environment_pip_freeze.txt` (or `conda env export`), plus OS/CUDA/
  driver/GPU details in the report.
- **Training commands** — in the report and as `.sh` launchers.
- **Inference commands** — in the report and as `.sh` launchers.
- **Best checkpoint(s)** — at minimum the selected best (+ resume + a milestone); traceable filename.
- **Representative outputs** — inference grids/figures, reconstruction previews, training log.
- **The thesis** — `<project>_thesis.md` built to this structure, with a one-page summary first.
- **Manifest** — `ARCHIVE_MANIFEST.md` (contents checklist + metadata) and `PROJECT_STRUCTURE.txt`.

**Naming:** archive folder `000_<project>_<version>_<date>_<tag>` (tag ∈ {`good`, `wip`, `baseline`,
…}). Artifact filenames carry version · epoch · key stat · date · time. Never overwrite a prior
version in place — copy, rename, version-stamp (freeze old → fork → stamp).

---

# 11. Reproducibility Checklist

Tick every item before declaring an archive complete:
- [ ] **Dataset available** — path documented, counts/format/splits recorded, source traceable.
- [ ] **Scripts available** — train/infer/datagen scripts archived, paths listed.
- [ ] **Commands available** — exact canonical commands in the report.
- [ ] **Environment available** — pip/conda freeze + OS/CUDA/driver/GPU recorded.
- [ ] **Checkpoints available** — best (+ resume) archived and traceable; load flags documented.
- [ ] **Results reproducible** — best metric re-derivable; inference outputs regenerable; seed fixed.

---

# 12. Future-Project Checklist

When archiving any new project into `/C_codes`:
- [ ] **Project completed** (or checkpointed at a defined state).
- [ ] **Report completed** — thesis built to this structure, one-page summary first.
- [ ] **Diagrams generated** — architecture + workflow + loss-flow.
- [ ] **Figures generated** — training/validation curves, inference examples, failure cases.
- [ ] **Paths verified** — every path in the report exists and is correct.
- [ ] **Archive created** — code + docs + config + env + checkpoints + outputs.
- [ ] **Mirror archive completed** — copy/mirror to the required NAS location(s); never fail the
      workflow if NAS is unavailable — log one warning and continue.
- [ ] **Metadata recorded** — archive date, version, experiment id, author, tags/keywords.
- [ ] **Guideline copy generated** — `thesis_guidelines_{version}_{date}_{time}.md` placed in `/C_codes`.

---

## Appendix — Recommended Thesis Section Skeleton (28-part, expandable)

A proven, comprehensive ToC (use as-is or trim per project; sections may be *N/A* with a reason):

```
1  Executive Summary                 15 Fold-wise Analysis (or single-split note)
2  Project Background                 16 Loss and Metric Analysis
3  Complete System Overview           17 Best Model Documentation
4  Algorithm Description              18 Source Code Inventory
5  Mathematical Foundations          19 Reproducibility Guide
6  Model Architecture                20 Scientific Significance
7  Architecture Figures              21 Engineering Significance
8  Dataset Description               22 Environment and Dependencies
9  Data Generation Workflow          23 Archive Metadata
10 Training Configuration            24 Lessons Learned
11 Training Commands                 25 Future Work
12 Validation Workflow               26 Appendices (commands/config/paths/trees/figures/tables)
13 Inference Workflow                27 References (papers/docs/code/internal reports)
14 Results and Evaluation            28 Revision History
```

Each numbered section carries detailed subsections (e.g. 6.1 High-Level Architecture … 6.12
Computational Complexity). Long reports (>100 pages) are expected and encouraged for flagship
projects — but the **one-page summary on page 1 is mandatory**.

---

*Master template — keep permanently in `/nas/DATA1/GPRutility_simulations/C_codes/`. Generate a
timestamped project copy (`thesis_guidelines_{version}_{date}_{time}.md`) for each new archived
project, populated with project-relevant details where available.*
