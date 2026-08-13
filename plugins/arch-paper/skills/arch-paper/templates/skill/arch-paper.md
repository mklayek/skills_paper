_date: 2026-07-09_

# arch-paper — full skill specification

## Overview

&nbsp;&nbsp;&nbsp;&nbsp;This is the long-form specification for the `arch-paper` skill. The skill drafts and structures archaeological ground-penetrating-radar (GPR) manuscripts on a single governing principle. The reader is grounded in the archaeological and historical stakes first, the technique is described second, results are fused with interpretation, every claim is hedged to its evidentiary tier, and the paper closes by returning to the archaeological question. GPR stays instrumental to an archaeological end and never becomes an end in itself. The backbone is synthesized from three Goodman-lineage source papers into one reusable IMRaD structure with a canonical section order, a copy-paste manuscript skeleton, a five-tier interpretation discipline, and a humanization gate that runs on every sentence.

## When to use

&nbsp;&nbsp;&nbsp;&nbsp;Reach for this skill when the user wants to write, draft, outline, or structure an archaeological GPR paper, chapter, or proceedings piece. The core triggers are time-slice or depth-slice survey reporting, buried-feature or anomaly interpretation, radargram-to-archaeology inference, Goodman-style archaeological-geophysics prose, and generating a full manuscript skeleton from raw project info. A single section request in the same house style also qualifies. Do not use the skill for a non-archaeological geophysics paper with no buried-feature interpretation, a pure signal-processing or hardware study, a GPR modeling paper with no site, or a standalone literature review that is not a primary survey report.

## Mandatory rules (ALWAYS)

&nbsp;&nbsp;&nbsp;&nbsp;Every generated document begins with the current date on the very first line in `YYYY-MM-DD` form. The default author block is embedded at the top of every manuscript, immediately after the date line, unless the user supplies an override. Any section without supplied content is written verbatim as `Yet to be developed`, and the skill never invents site data, results, or citations to fill a gap. The humanization gate applies to every sentence, with no exemption for captions, abstracts, or list items. The default document format is Times New Roman, 12 pt, 1.5 line spacing, with the first line of every paragraph indented except inside tables.

The default author block is:

```
Author: Mrinal Kanti Layek
Affiliation: Geophysics & AI Lab, Department of Energy & Resources Engineering,
Chonnam National University, Gwangju, Republic of Korea [61186]
(Korean: 지구물리 및 인공지능 연구실, 에너지자원공학과, 전남대학교, 광주광역시, 대한민국 [61186])
Email: layek.mk@gmail.com
```

## Workflow

&nbsp;&nbsp;&nbsp;&nbsp;The skill runs in seven steps. The first gathers project info, which covers the site name and location, the antenna frequency, the survey grid and line spacing, the target features, the key results, and the list of available figures and tables. Missing items are allowed and each becomes a `Yet to be developed` placeholder. The second emits the dated manuscript skeleton, writing the current date on line one, then the author block, then the canonical headings from `templates/master/MASTER_TEMPLATE.md` in order with `{{placeholders}}`. The third populates each available section by following its dedicated template in `templates/sections/NN_*.md`, matching the tense and voice guidance in each file. The fourth marks every missing section `Yet to be developed`, verbatim, so gaps stay visible and auditable. The fifth runs the humanization gate in `templates/master/humanization_integration.md` on every drafted paragraph before it is accepted. The sixth inserts figure, table, citation, and equation references per the conventions, which means "Figure N" in body text, author-date in-text citations, and `$$...$$` display math with `\tag` numbering. So the seventh and final step runs the review checklist in `templates/master/global_rules_checklists.md` before the draft is returned.

## Generation logic (expanded)

&nbsp;&nbsp;&nbsp;&nbsp;The generator maps supplied project info onto placeholders and leaves unmapped placeholders as `Yet to be developed`. The title takes the pattern technique plus key output plus site, so a 400 MHz survey of a buried moat at a given site yields a neutral noun phrase for a geophysics journal or an evocative "Search for" phrasing for a broad-audience volume. The abstract is generated only when the user supplies at least one quantified result and a validation statement, because an abstract without a headline number and a validation clause fails the review checklist. Where the venue is an edited-volume chapter that waives the abstract, the first Introduction paragraph stands in.

&nbsp;&nbsp;&nbsp;&nbsp;The Methods block is always a headed section and never buried in the Introduction, which is one of the pitfalls the source-paper comparison flags. The generator states the antenna frequency, the grid and line spacing, the trace and sample rates, and the positioning method, then names explicitly what was not done and why. The depth-conversion subsection always presents the velocity value, its origin, and the depth relation $d = v t / 2$, because a Methods section that hides the velocity fails the checklist.

&nbsp;&nbsp;&nbsp;&nbsp;Results are generated one block per site or anomaly, mirroring the Methods order so a reader can flip between a technique's method entry and its result entry. Each block opens with a direct figure pointer and the stated parameters, describes the geometry and dimensions in the same units as the site section, cross-checks against the historic or excavation record with a stated magnitude, and reports negative results plainly. Interpretation is fused into Results as a light gloss, then disciplined in Section 6 so a gloss never hardens into a confirmed claim.

&nbsp;&nbsp;&nbsp;&nbsp;The interpretation generator is the heart of the skill. Every archaeological reading is placed on exactly one evidentiary tier, and the hedging verb is drawn from that tier's register. The generator refuses to attach Tier 1 language ("was confirmed by excavation") to an anomaly that has only spatial coherence, which would be a Tier 4 or Tier 5 claim. Meaningful absences are written as classifications, not discarded nulls.

## Section order and template map

| Section | Template file | What to write |
|---|---|---|
| Title, Authors, Keywords | `templates/sections/00_title_authors_keywords.md` | Technique + key output + site, paired authorship, 3 to 6 keywords general to novel |
| Abstract | `templates/sections/01_abstract.md` | One paragraph, 150 to 300 words, context, gap, method, one quantified result, validation |
| 1. Introduction | `templates/sections/02_introduction.md` | Historical context to site, the gap, feature vocabulary, roadmap sentence |
| 2. Study Area / Historical Context | `templates/sections/03_study_area_site.md` | Location, landform, cultural identity, dating, feature dimensions from historic sources |
| 3. Geological and Site Setting | `templates/sections/04_geological_site_setting.md` | Soils, moisture, near-surface conditions tied to radar penetration and contrast |
| 4. Materials and Methods (parent) | `templates/sections/05_materials_methods.md` | Instrument, chain, slice generation overview, plus what was not done |
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

## Interpretation rule (5-tier evidentiary hierarchy)

| Tier | Standing | Hedging register |
|---|---|---|
| 1. Excavation-confirmed | Dug and physically recovered | State plainly. "was confirmed by excavation", "revealed", "were found" |
| 2. Strongly-supported | An independent line backs it | "agrees with the dimensions recorded by", "is consistent with", "as predicted by" |
| 3. Probable | Morphological or typological reasoning | "is believed to be", "most probably represents", "the geometry suggests a" |
| 4. Possible | Coherent anomaly, alternatives open | "may correspond to", "may be related to", "may indicate", "perhaps" |
| 5. Unconfirmed | Prospective target awaiting a dig | "tentatively", "indicate the presence of", "an area that would repay future excavation" |

&nbsp;&nbsp;&nbsp;&nbsp;The per-anomaly interpretation chain restates the observed anomaly and quantifies its diagnostic property, gives the first-order reading hedged to its tier, adds any nested sub-feature, brings the independent supporting evidence that sets the tier, states the confounds or dependencies, reads meaningful absences as classifications, and closes on the archaeological so-what.

## Humanization gate

&nbsp;&nbsp;&nbsp;&nbsp;The gate has no em dashes anywhere, which means a dash is rephrased into two sentences or replaced with a comma. Semicolons are avoided in favor of a period or a join with "and" or "but", and mid-sentence ellipses are dropped. Parentheticals are limited to one short aside per paragraph, and colons are used sparingly. The first line of every paragraph is indented except inside tables. Top-level headings are bold and read "1. Introduction", where subsection labels are italic and read "2.1". Most sentences begin with "The", "Generally", "However", "So", "In this case", or "Throughout", varied across the paragraph, and clauses join with the connectors "which", "where", and "that's why". There are no 1) 2) 3) numbered lists inside section prose, so enumeration is carried in paragraph form with "The first", "A second", and "and finally". Hedging filler and stock transitions are cut for the direct statement. Repeated terms are varied, equations use `$...$` and `$$...$$`, and in-text references follow `(Author et al., 2023)`, `(Terrasse et al., 2015, 2017; Kumar et al., 2023)`, and `Following Ge et al. (2024)`. The default format is Times New Roman, 12 pt, 1.5 line spacing.

## Full manuscript skeleton (copy and populate)

&nbsp;&nbsp;&nbsp;&nbsp;Copy the block below into a new manuscript and fill the `{{placeholders}}`. Every part not yet available reads `Yet to be developed`. Keep first lines of paragraphs indented and follow the humanization rules.

```
2026-07-09

Author: Mrinal Kanti Layek
Affiliation: Geophysics & AI Lab, Department of Energy & Resources Engineering,
Chonnam National University, Gwangju, Republic of Korea [61186]
(Korean: 지구물리 및 인공지능 연구실, 에너지자원공학과, 전남대학교, 광주광역시, 대한민국 [61186])
Email: layek.mk@gmail.com

# {{Title: technique + key output + site/region}}

**Authors:** {{Author list with affiliation superscripts}}
**Keywords:** {{3 to 6 terms, general to novel}}

## Abstract
{{One paragraph, 150 to 300 words: context, gap, method and key parameters, one quantified result, validation statement}}
Yet to be developed

## 1. Introduction
{{Historical and cultural context narrowing to the site, the knowledge gap, feature vocabulary defined in context, a roadmap sentence}}
Yet to be developed

## 2. Study Area and Archaeological / Historical Context
{{Location, landform, cultural identity, dating, feature dimensions from historic sources, with a figure pointer in the first sentence}}
Yet to be developed

## 3. Geological and Site Setting
{{Soils, stratigraphy, moisture, near-surface conditions, each tied to radar penetration and contrast}}
Yet to be developed

## 4. Materials and Methods

### 4.1 Data Acquisition
{{Instrument, antenna frequency, grid, line spacing, trace/sample rates, positioning, field conditions and what limited coverage}}
Yet to be developed

### 4.2 Processing
{{Ordered chain: time-zero, gain, filter, background removal, migration, gridding, and what was not done and why}}
Yet to be developed

### 4.3 Time-slice / Depth-slice and Depth Conversion
{{Slice generation, amplitude quantity mapped, velocity model, time-to-depth conversion}}

$$ d = \frac{v\,t}{2} \tag{1} $$

where $d$ is reflector depth, $v$ is radar wave velocity in the ground, and $t$ is the two-way travel time.
Yet to be developed

## 5. Results
{{Repeat one block per site / anomaly / technique mirroring the Methods order, opening with a figure pointer and parameters, describing geometry and dimensions, reporting negatives plainly}}
Yet to be developed

## 6. Interpretation
{{One reading per anomaly, each placed on exactly one evidentiary tier with the matching hedge, mechanistic support, stated confounds, and the archaeological so-what}}
Yet to be developed

## 7. Discussion
{{Cross-site / cross-technique synthesis, a verdict per technique with a scope caveat, mechanistic explanation of agreements, prior-work comparison}}
Yet to be developed

## 8. Conclusions
{{Core contribution generalized beyond the sites, feature counts by tier, next steps, broader significance}}
Yet to be developed

## Acknowledgements
{{Funding, permits and access, named contacts by role, software attribution}}
Yet to be developed

## References
{{Author-date, alphabetical, unnumbered, self-citation for method continuity, grey literature on equal footing}}
Yet to be developed

## Figure Captions
Figure 1. {{Self-sufficient interpretive caption carrying one quantified value}}
Yet to be developed

## Tables
{{Survey-parameters table and feature-inventory table, if used}}
Yet to be developed

## Supplementary
{{Data availability, extended figures, processing scripts}}
Yet to be developed
```

## Worked notes

&nbsp;&nbsp;&nbsp;&nbsp;The date on line one is the generation date, so a manuscript emitted today carries `2026-07-09` and a manuscript regenerated later carries that later date. The author block wraps across two lines for the English affiliation and adds the parenthetical Korean line, which is preserved verbatim including the `[61186]` postal code. When the user overrides the author, the date line stays and only the block below it changes.

&nbsp;&nbsp;&nbsp;&nbsp;A common mistake the skill guards against is filling a gap with plausible-sounding invented data. Where the user gives an antenna frequency but no velocity, the depth-conversion subsection keeps the depth relation and marks the velocity value `Yet to be developed` rather than guessing a number. Where a result has spatial coherence but no dig, the interpretation stays on Tier 4 or Tier 5 and never borrows Tier 1 language. So the generated draft is always honest about what is known and what remains open, which is the interpretive discipline the whole template exists to enforce.

## Reference files

&nbsp;&nbsp;&nbsp;&nbsp;The bundled templates are `templates/master/MASTER_TEMPLATE.md` for the canonical order and skeleton, `templates/master/humanization_integration.md` for the per-sentence gate, `templates/master/global_rules_checklists.md` for the one-page reference and checklist, and `templates/master/comparison_report.md` for the three-paper synthesis. The 17 per-section templates live in `templates/sections/00_*.md` through `16_*.md`. The companion skill docs are `templates/skill/usage_guide.md` and `templates/skill/implementation_notes.md`.
