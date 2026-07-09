---
name: arch-paper
description: Use when writing, drafting, or structuring an archaeological ground-penetrating-radar (GPR) research paper or manuscript section, covering time-slice/depth-slice surveys, buried-feature/anomaly interpretation, Goodman-style archaeological-geophysics writing, or generating a full paper skeleton from project info.
---

# arch-paper

## Overview

&nbsp;&nbsp;&nbsp;&nbsp;This skill drafts and structures archaeological ground-penetrating-radar (GPR) manuscripts on a single governing principle. The reader is grounded in the archaeological and historical stakes first, the technique is described second, results are fused with interpretation, every claim is hedged to its evidentiary tier, and the paper closes by returning to the archaeological question. GPR is instrumental to an archaeological end, never an end in itself. The skill synthesizes three Goodman-lineage source papers into one reusable IMRaD backbone with a canonical section order, a copy-paste manuscript skeleton, a five-tier interpretation discipline, and a humanization gate that runs on every sentence.

## When to use

Use this skill when the work shows any of these triggers.

- The user asks to write, draft, outline, or structure an archaeological GPR paper, chapter, or proceedings piece.
- The subject is time-slice or depth-slice survey reporting, buried-feature or anomaly interpretation, or radargram-to-archaeology inference.
- The user wants Goodman-style archaeological-geophysics prose, or a full manuscript skeleton generated from raw project info (site, antenna frequency, grid, targets, results, figures).
- A single section is needed (abstract, methods, interpretation, discussion) in the same house style.

Do NOT use this skill when the task is a non-archaeological geophysics paper with no buried-feature interpretation, a pure signal-processing or hardware paper, a GPR modeling or simulation study with no site, or a literature review that is not a primary survey report.

## Mandatory rules (ALWAYS)

- Every generated document BEGINS with the current date on the very first line in `YYYY-MM-DD` form, for example `2026-07-09`.
- The default author block is embedded at the top of every manuscript, immediately after the date line, unless the user overrides it.

```
Author: Mrinal Kanti Layek
Affiliation: Geophysics & AI Lab, Department of Energy & Resources Engineering,
Chonnam National University, Gwangju, Republic of Korea [61186]
(Korean: 지구물리 및 인공지능 연구실, 에너지자원공학과, 전남대학교, 광주광역시, 대한민국 [61186])
Email: layek.mk@gmail.com
```

- Any section without supplied content is written verbatim as `Yet to be developed`. Never invent site data, results, or citations to fill a gap.
- The humanization gate applies to every sentence the skill writes. No exceptions for captions, abstracts, or list items.
- The default document format is Times New Roman, 12 pt, 1.5 line spacing, with every paragraph first line indented except inside tables.

## Workflow

1. **Gather project info.** Collect site name and location, antenna frequency, survey grid and line spacing, target features, key results, and which figures and tables are available. Missing items are allowed and become `Yet to be developed`.
2. **Emit the dated manuscript skeleton.** Write the current date on line one, then the author block, then the canonical headings from `templates/master/MASTER_TEMPLATE.md` in order with `{{placeholders}}`.
3. **Populate each available section** by following its dedicated template in `templates/sections/NN_*.md` (see the map below). Match the tense and voice guidance in each file.
4. **Mark missing sections** `Yet to be developed`, verbatim, so gaps are visible and auditable.
5. **Run the humanization gate** in `templates/master/humanization_integration.md` on every drafted paragraph before accepting it.
6. **Insert figure, table, citation, and equation refs** per the conventions ("Figure N", author-date in-text, `$$...$$` display math with `\tag`).
7. **Run the review checklist** in `templates/master/global_rules_checklists.md` before returning the draft.

## Section order & template map

| Section | Template file | What to write |
|---|---|---|
| Title, Authors, Keywords | `templates/sections/00_title_authors_keywords.md` | Technique + key output + site in the title, paired authorship, 3 to 6 keywords general to novel |
| Abstract | `templates/sections/01_abstract.md` | One paragraph, 150 to 300 words, context, gap, method, one quantified result, validation |
| 1. Introduction | `templates/sections/02_introduction.md` | Historical context, narrow to site, state the gap, define feature vocabulary, roadmap sentence |
| 2. Study Area / Historical Context | `templates/sections/03_study_area_site.md` | Location, landform, cultural identity, dating, feature dimensions from historic sources |
| 3. Geological and Site Setting | `templates/sections/04_geological_site_setting.md` | Soils, moisture, near-surface conditions, each tied to radar penetration and contrast |
| 4. Materials and Methods (parent) | `templates/sections/05_materials_methods.md` | Overview of instrument, chain, and slice generation, plus what was not done |
| 4.1 Data Acquisition | `templates/sections/06_data_acquisition.md` | Instrument, antenna frequency, grid, line spacing, trace/sample rates, positioning |
| 4.2 Processing | `templates/sections/07_processing.md` | Ordered chain, time-zero, gain, filter, background removal, migration, gridding |
| 4.3 Slice + Depth Conversion | `templates/sections/07_processing.md` + `templates/sections/08_equations_math.md` | Slice generation, amplitude quantity, velocity model, time-to-depth conversion |
| Equations | `templates/sections/08_equations_math.md` | Depth relation, velocity from permittivity, depth-slice amplitude, in `$$...$$` |
| 5. Results | `templates/sections/09_results.md` | One block per site or anomaly mirroring Methods order, figure pointer, geometry, negatives |
| 6. Interpretation | `templates/sections/10_interpretation.md` | One reading per anomaly, each on exactly one tier with the matching hedge |
| 7. Discussion | `templates/sections/11_discussion.md` | Cross-site synthesis, verdict per technique with a scope caveat, prior-work comparison |
| 8. Conclusions | `templates/sections/12_conclusions.md` | Generalized contribution, feature counts by tier, next steps, broader significance |
| References | `templates/sections/13_references_citations.md` | Author-date, alphabetical, unnumbered, self-citation, grey literature on equal footing |
| Figure Captions | `templates/sections/14_figures_captions.md` | Self-sufficient interpretive captions each carrying one quantified value |
| Tables | `templates/sections/15_tables.md` | Optional survey-parameters and feature-inventory tables |
| Acknowledgements, Supplementary | `templates/sections/16_acknowledgements_supplementary.md` | Funding, permits, named contacts, software attribution, data availability |

## Interpretation rule

&nbsp;&nbsp;&nbsp;&nbsp;Place every archaeological claim on exactly one of five evidentiary tiers and write it in that tier's register. The hedging verb carries the tier, and the one failure this rule exists to prevent is claiming confirmation for a Tier 4 or Tier 5 anomaly.

| Tier | Standing | Hedging register |
|---|---|---|
| 1. Excavation-confirmed | Dug and physically recovered | State plainly. "was confirmed by excavation", "revealed", "were found" |
| 2. Strongly-supported | An independent line backs it | "agrees with the dimensions recorded by", "is consistent with", "as predicted by" |
| 3. Probable | Morphological or typological reasoning | "is believed to be", "most probably represents", "the geometry suggests a" |
| 4. Possible | Coherent anomaly, alternatives open | "may correspond to", "may be related to", "may indicate", "perhaps" |
| 5. Unconfirmed | Prospective target awaiting a dig | "tentatively", "indicate the presence of", "an area that would repay future excavation" |

&nbsp;&nbsp;&nbsp;&nbsp;A meaningful absence is its own interpretive move. The absence of deep reflections below a mound reads as "only a shallow surface burial is present", which is a real classification and not a discarded null.

## Humanization gate (quick)

- No em dashes anywhere. Rephrase into two sentences or use a comma.
- Avoid semicolons. Use a period, or join with "and" or "but". No mid-sentence ellipses. Limit parentheticals to one short aside per paragraph. Use colons sparingly.
- Indent the first line of every paragraph, except inside tables.
- Headings bold at top level "1. Introduction", subsection labels italic "2.1".
- Most sentences begin with "The", "Generally", "However", "So", "In this case", or "Throughout", varied so the pattern is not mechanical.
- Join clauses with connectors "which", "where", and "that's why" rather than stacking choppy sentences.
- No 1) 2) 3) numbered lists inside section prose. Carry enumeration in paragraph form with "The first", "A second", "and finally".
- Cut hedging filler ("it's worth noting", "arguably") and stock transitions ("furthermore", "in conclusion"). State it directly.
- Vary repeated terms (radargram, profile, section for the vertical image; anomaly, reflection, feature where each is accurate).
- Equations inline in `$...$` and displayed in `$$...$$`, never bare LaTeX delimiters.
- In-text references follow `(Author et al., 2023)`, `(Terrasse et al., 2015, 2017; Kumar et al., 2023)`, and `Following Ge et al. (2024)`.
- Document format Times New Roman, 12 pt, 1.5 line spacing.

## Reference files

- `templates/master/MASTER_TEMPLATE.md` - canonical section order, full manuscript skeleton, global writing rules, review checklist.
- `templates/master/humanization_integration.md` - the enforceable per-sentence gate with before/after examples.
- `templates/master/global_rules_checklists.md` - one-page quick reference, tense table, do/don't, final checklist.
- `templates/master/comparison_report.md` - the three-paper synthesis that this backbone is drawn from.
- `templates/sections/00_*.md` through `16_*.md` - the 17 per-section templates mapped above.
- `templates/skill/arch-paper.md` - the full skill specification with the copy-paste skeleton.
- `templates/skill/usage_guide.md` - how to invoke, with an example input and generated skeleton.
- `templates/skill/implementation_notes.md` - extraction pipeline, design decisions, and how to extend.

## Quality checklist

- [ ] Document begins with the current date line, then the default author block.
- [ ] Canonical section order followed, abstract present for a journal submission.
- [ ] Historical and archaeological context precedes the technique, feature vocabulary defined on first use.
- [ ] Methods is a headed section with acquisition, processing, and depth conversion, and the velocity value plus depth relation are stated.
- [ ] What was not done is named and justified.
- [ ] Results mirror the Methods order and report negatives plainly, every number cross-checked with a stated magnitude.
- [ ] Every archaeological claim sits on exactly one evidentiary tier with the matching hedge, and no Tier 4 or Tier 5 anomaly is claimed as confirmed.
- [ ] Missing sections read `Yet to be developed` verbatim.
- [ ] Discussion and Conclusions exist as explicit sections and the paper closes on the archaeological question.
- [ ] Equations in `$$...$$` with `\tag` numbering and defined symbols.
- [ ] References alphabetical, unnumbered, author-date, self-citation and grey literature included, every in-text cite resolves.
- [ ] Captions self-sufficient and interpretive, each carrying one quantified value.
- [ ] Humanization gate passed, no em dashes, semicolons avoided, no filler or stock transitions, openers varied, paragraphs indented.
- [ ] Document set to Times New Roman, 12 pt, 1.5 spacing.
