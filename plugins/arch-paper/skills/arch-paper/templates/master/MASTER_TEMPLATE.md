_Master template date: 2026-07-09_

# Master Archaeological GPR Paper Template

&nbsp;&nbsp;&nbsp;&nbsp;This is the comprehensive master template for writing an archaeological ground-penetrating-radar (GPR) paper. It synthesizes three source papers (Goodman et al. 1995, Dalan et al. 2011, Goodman et al. 2014) into one reusable, journal-style IMRaD backbone adapted for archaeological GPR. The template gives the canonical section order, a ready-to-fill manuscript skeleton, the global writing rules, the interpretation workflow, and a review checklist. For the per-section detail, each entry points to its dedicated file in `templates/sections/`.

&nbsp;&nbsp;&nbsp;&nbsp;The governing principle is single source of truth. Ground the reader in the archaeological and historical stakes first, describe the technique second, fuse interpretation with results, hedge every claim to its evidentiary tier, and close by returning to the archaeological question. GPR is instrumental to an archaeological end, never an end in itself.

---

## Default author block (embed at the top of every generated manuscript)

&nbsp;&nbsp;&nbsp;&nbsp;Every generated manuscript starts with this block unless the user overrides it.

```
Author: Mrinal Kanti Layek
Affiliation: Geophysics & AI Lab, Department of Energy & Resources Engineering,
Chonnam National University, Gwangju, Republic of Korea [61186]
지구물리 및 인공지능 연구실, 에너지자원공학과, 전남대학교, 광주광역시, 대한민국 [61186]
Email: layek.mk@gmail.com
```

---

## 1. Canonical full section order

&nbsp;&nbsp;&nbsp;&nbsp;This is the full journal-style order. Sections marked optional collapse or drop for short chapters and proceedings. Each entry gives a short "what to write" plus a pointer to the detailed section template.

**Title, Authors, Affiliation, Keywords.**
Technique plus key output plus site or region in the title. Pair the geophysics lead with local site-authority and institutional archaeology co-authors. Give 3 to 6 keywords ordered general to novel. See `templates/sections/00_title_authors_keywords.md`.

**Abstract.**
One paragraph, roughly 150 to 300 words, mandatory for journals. Cover context, the archaeological gap, method and key parameters, at least one quantified headline result, and a validation statement. Omit only when an edited-volume venue explicitly waives it. See `templates/sections/01_abstract.md`.

**1. Introduction.**
Open on historical and cultural context, narrow to the site, state the loss or knowledge gap that justifies the survey, define recurring feature vocabulary in context, and end with an explicit roadmap paragraph. See `templates/sections/02_introduction.md`.

**2. Study Area and Archaeological / Historical Context.**
Give precise location and landform, the cultural-historical identity and dating, quantified feature dimensions from historic sources, and the land-use history that frames what GPR must find. See `templates/sections/03_study_area_site.md`.

**3. Geological and Site Setting.**
Describe soils, stratigraphy, moisture, and near-surface conditions that control radar penetration and contrast. Tie each ground property to its effect on the survey. See `templates/sections/04_geological_site_setting.md`.

**4. Materials and Methods.**
Instrument make, model, and geometry, ground conditions and penetration, the processing chain, and slice or depth generation. State plainly what was not done and why. Three subsections follow.

&nbsp;&nbsp;&nbsp;&nbsp;*4.1 Data Acquisition.* Instrument, antenna frequency, survey grid and line spacing, trace and sample rates, positioning, and field conditions. See `templates/sections/06_data_acquisition.md` (parent overview in `templates/sections/05_materials_methods.md`).

&nbsp;&nbsp;&nbsp;&nbsp;*4.2 Processing.* The ordered processing chain from raw traces to a clean volume: time-zero, gain, filtering, background removal, migration, and gridding. See `templates/sections/07_processing.md`.

&nbsp;&nbsp;&nbsp;&nbsp;*4.3 Time-slice / Depth-slice and Depth Conversion.* Slice generation, the amplitude quantity mapped, the velocity model, and travel-time-to-depth conversion. Equations go here. See `templates/sections/07_processing.md` and `templates/sections/08_equations_math.md`.

**5. Results.**
Repeat one block per site, anomaly, or technique, mirroring the Methods order. Open each with a direct figure pointer and stated parameters, describe geometry and dimensions, and report negative results plainly. See `templates/sections/09_results.md`.

**6. Interpretation.**
Turn each observation into an archaeological reading on a leash. Place every claim on exactly one of the five evidentiary tiers and match the hedging verb to the tier. See `templates/sections/10_interpretation.md`.

**7. Discussion.**
Synthesize across sites or techniques, give a verdict per technique with a scope-limiting caveat, explain agreements and disagreements mechanistically, and state candidly where success owed something to site conditions. Compare to prior work. See `templates/sections/11_discussion.md`.

**8. Conclusions.**
Restate the core contribution generalized beyond the specific sites, list confirmed versus probable versus unconfirmed feature counts, propose next steps, and close on broader significance. See `templates/sections/12_conclusions.md`.

**Acknowledgements.**
Credit funding, permits and access, named field and local contacts by role, and an explicit software or tool attribution. See `templates/sections/16_acknowledgements_supplementary.md`.

**References.**
Author-date, alphabetical, unnumbered. Include self-citation for method continuity, a classic geophysics text for any named-but-unelaborated technique, and grey literature on equal footing. See `templates/sections/13_references_citations.md`.

**Figure Captions.**
Self-sufficient and interpretive. Each caption states what the figure means and carries at least one quantified value, so figures plus captions reconstruct the paper. See `templates/sections/14_figures_captions.md`.

**Tables.**
Optional in this genre. Use a survey-parameters table and a feature-inventory table for a full journal article. The source papers use none. See `templates/sections/15_tables.md`.

**Supplementary.**
Data availability, extended figure sets, raw survey grids, and processing scripts. See `templates/sections/16_acknowledgements_supplementary.md`.

---

## 2. Full manuscript skeleton (copy and populate)

&nbsp;&nbsp;&nbsp;&nbsp;Copy the block below into a new manuscript and fill the `{{placeholders}}`. Any part not yet available reads "Yet to be developed". Keep first lines of paragraphs indented and follow the humanization rules in `humanization_integration.md`.

```
Author: Mrinal Kanti Layek
Affiliation: Geophysics & AI Lab, Department of Energy & Resources Engineering,
Chonnam National University, Gwangju, Republic of Korea [61186]
지구물리 및 인공지능 연구실, 에너지자원공학과, 전남대학교, 광주광역시, 대한민국 [61186]
Email: layek.mk@gmail.com

# {{Title: technique + key output + site/region}}
Prompt: name the method, the headline output, and the place. Neutral noun phrase for a geophysics journal.

**Authors:** {{Author list with affiliation superscripts}}
**Keywords:** {{3 to 6 terms, general to novel}}

## Abstract
{{One paragraph, 150 to 300 words}}
Prompt: context, gap, method and key parameters, one quantified result, validation statement.

## 1. Introduction
{{Historical and cultural context, narrowing to the site}}
Prompt: why the site matters, the knowledge gap, feature vocabulary defined in context, and a roadmap sentence.

## 2. Study Area and Archaeological / Historical Context
{{Location, landform, cultural identity, dating, feature dimensions from historic sources}}
Prompt: precise relative location plus a figure pointer in the first sentence.

## 3. Geological and Site Setting
{{Soils, stratigraphy, moisture, near-surface conditions}}
Prompt: tie each ground property to its effect on radar penetration and contrast.

## 4. Materials and Methods
### 4.1 Data Acquisition
{{Instrument, antenna frequency, grid, line spacing, trace/sample rates, positioning}}
Prompt: state field conditions and what limited coverage.

### 4.2 Processing
{{Ordered processing chain: time-zero, gain, filter, background removal, migration, gridding}}
Prompt: state what was not done and why.

### 4.3 Time-slice / Depth-slice and Depth Conversion
{{Slice generation, amplitude quantity, velocity model, time-to-depth conversion}}
Prompt: present the velocity, its origin, and the depth relation as $d = v t / 2$.

## 5. Results
{{Repeat one block per site / anomaly / technique, mirroring the Methods order}}
Prompt: open with a figure pointer and parameters, describe geometry and dimensions, report negatives plainly.

## 6. Interpretation
{{One reading per anomaly, each on exactly one evidentiary tier}}
Prompt: match the hedging verb to the tier, add mechanistic support, state confounds, close on the archaeological so-what.

## 7. Discussion
{{Cross-site / cross-technique synthesis, verdict per technique with a scope caveat}}
Prompt: explain agreements mechanistically, state where site conditions helped, compare to prior work.

## 8. Conclusions
{{Core contribution generalized, feature counts by tier, next steps, broader significance}}
Prompt: restate what was learned beyond this site.

## Acknowledgements
{{Funding, permits, named contacts, software attribution}}

## References
{{Author-date, alphabetical, unnumbered}}
Prompt: include self-citation for method continuity and grey literature on equal footing.

## Figure Captions
Figure 1. {{Self-sufficient interpretive caption carrying one quantified value}}
...

## Tables
{{Survey-parameters table and feature-inventory table, if used}}

## Supplementary
{{Data availability, extended figures, processing scripts}}
```

---

## 3. Global writing rules

&nbsp;&nbsp;&nbsp;&nbsp;These rules apply to every generated manuscript. The humanization rules in `humanization_integration.md` are enforced on top of them.

- Use US English throughout.
- Write named, unnumbered section titles in the source-paper tradition, or decimal-numbered headings ("1. Introduction", "4.1 Data Acquisition") when the target journal requires them. Bold the top-level heading, italicize the "2.1" subsection label.
- Passive voice dominates the methods. Reserve first person for explicit interpretive judgment, and avoid it entirely for a neutral journal.
- Ground archaeological and historical context before the technique. Define recurring feature vocabulary (moat, chamber, keyhole tomb, earth lodge) by use in context, up front.
- Fuse results and interpretation. Gloss each anomaly archaeologically in the same breath it is described, but keep the evidentiary discipline of Section 6 so a light gloss never hardens into a confirmed claim.
- Close every paper by returning to the archaeological question.
- Cross-check every quantitative claim against an independent source and state the magnitude of agreement or disagreement. Never write "consistent" without the number.
- Report negative results plainly. A method that failed to detect an expected feature is a finding.
- Keep terminology consistent (see the table below). Define every abbreviation on first use, for example ground-penetrating radar (GPR), two-way travel time (TWTT).

### Recommended tense usage per section

| Section | Default tense | Note |
|---|---|---|
| Abstract | Present for scope and general claims | Past for what was done in the study |
| Introduction | Present for standing facts | Past for historical narrative |
| Study Area / Context | Past for history | Present for what exists now |
| Geological Setting | Present | Standing physical description |
| Methods (Acquisition, Processing) | Past passive | "A 400 MHz antenna was used" |
| Equations | Present for the relation | Past for the study-specific value |
| Results | Present for what the figure shows | Past for the survey action |
| Interpretation | Present for standing readings | Past for validating actions ("were found") |
| Discussion | Present-perfect for cumulative claims | Present for verdicts |
| Conclusions | Present | Past where summarizing what was done |

### Voice

Impersonal passive for procedure. Active "we" only at an explicit interpretive judgment, and omitted entirely for a strict geophysics journal. Let the site or the feature be the grammatical subject in interpretation.

### Abbreviation rules

Define on first use, abbreviation in parentheses after the spelled-out term, then use the abbreviation consistently. Common cases: ground-penetrating radar (GPR), two-way travel time (TWTT), relative dielectric permittivity, ground-truth.

### Terminology-consistency table

| Preferred term | Do not mix with | Note |
|---|---|---|
| ground-penetrating radar (GPR) | ground penetrating radar, georadar | Hyphenate, define once |
| radargram | radar profile, B-scan (informal) | The vertical section image |
| time slice | timeslice, depth slice (unless truly depth) | Horizontal amplitude map at a time window |
| depth slice | depth-slice | Reserve for slices after depth conversion |
| two-way travel time (TWTT) | travel time, TWT | Define once, then TWTT |
| dielectric permittivity | dielectric constant | Use "relative dielectric permittivity" for $\varepsilon_r$ |
| amplitude map | amplitude image | The mapped average squared amplitude |
| hyperbola | diffraction curve | The point-source diffraction signature |
| migration | focusing | Kirchhoff migration collapses hyperbolae |
| velocity | speed | Radar wave velocity in the ground |

### Figure and table conventions

Refer to figures as "Figure N" spelled out in body text. Captions are self-sufficient and interpretive and carry at least one quantified value. Place figures inline near first citation for modern journals, or batched at the end only for camera-ready proceedings. Tables are optional in this genre. Use a survey-parameters table and a feature-inventory table for a full journal article.

### Equation formatting

Display equations on their own line in `$$...$$` with a blank line above and below, and number with `\tag` inside the block. Define every symbol immediately after, in order of appearance. Inline symbols use `$...$`. For a full journal Methods section present at least the depth relation, the velocity-from-permittivity relation, and the depth-slice amplitude definition.

$$ d = \frac{v\,t}{2} \tag{1} $$

where $d$ is reflector depth, $v$ is radar wave velocity in the ground, and $t$ is the two-way travel time. See `templates/sections/08_equations_math.md` for the full equation set.

### Citation placement rules

Use author-date in-text form. Place a citation at the exact point a claim needs backing, cluster citations in the theory background, and drop citation density in Results in favor of ground-truth cross-checks. Cite to underwrite the physics of an inference, not the archaeology itself, which is supported by excavation, maps, and photographs. Self-cite for method continuity. Treat grey literature as first-class. Forms: `(Kumar et al., 2023)`, `(Terrasse et al., 2015, 2017; Kumar et al., 2023)`, and `Following Ge et al. (2024)`. See `templates/sections/13_references_citations.md`.

---

## 4. Interpretation workflow (5-tier evidentiary-validation hierarchy)

&nbsp;&nbsp;&nbsp;&nbsp;This is the interpretive spine of the whole template. Place every archaeological claim on exactly one tier and write it in that tier's register. The hierarchy runs strongest to weakest, and the hedging verb carries the tier. Full detail is in `templates/sections/10_interpretation.md`.

| Tier | Standing | Evidence | Hedging verbs |
|---|---|---|---|
| **1. Excavation-confirmed** | The feature was dug and physically recovered | Excavation artifacts, recovered structure | "was confirmed by excavation", "revealed", "were found and corroborated by" |
| **2. Strongly-supported** | No dig on this feature, but an independent line backs it | Matching historic-map dimension, documented construction method, published mechanism | "agrees with the dimensions recorded by", "is consistent with", "as predicted by" |
| **3. Probable** | Morphological or typological reasoning from geometry alone | Regional archaeological typology, geometry | "is believed to be", "most probably represents", "the geometry suggests a" |
| **4. Possible** | A coherent anomaly that reads plausibly, alternatives left open | Spatial coherence only | "may correspond to", "may be related to", "perhaps", "several interpretations suggest" |
| **5. Unconfirmed** | A prospective target awaiting excavation | Anomaly present, no validation | "indicate the presence of", "an area that would repay future excavation" |

&nbsp;&nbsp;&nbsp;&nbsp;The one failure this workflow exists to prevent is claiming confirmation for a Tier 4 or Tier 5 anomaly. A meaningful absence is its own interpretive move, so absence of deep reflections below a mound reads as "only a shallow surface burial is present", which is a real classification and not a discarded null.

**The per-anomaly interpretation chain.** Restate the observed anomaly and quantify its diagnostic property. Give the first-order reading hedged to its tier. Add any nested sub-feature. Bring the independent supporting evidence, which sets the tier. State the confounds or dependencies. Interpret meaningful absences as classifications. Close on the archaeological so-what.

---

## 5. Manuscript review checklist

**Structure.**
- [ ] Canonical section order followed, with the abstract present for a journal submission.
- [ ] Methods is a headed section, not buried in the Introduction.
- [ ] Discussion and Conclusions exist as explicit sections for a full manuscript.
- [ ] Results order mirrors the Methods order.
- [ ] The paper closes by returning to the archaeological question.

**Content.**
- [ ] Historical and archaeological context precedes the technique.
- [ ] Feature vocabulary is defined in context on first use.
- [ ] Every quantitative claim is cross-checked against an independent source with a stated magnitude.
- [ ] Negative results are reported plainly.
- [ ] The velocity value, its origin, and the depth relation are stated.
- [ ] What was not done is named and justified.

**Style.**
- [ ] US English, consistent terminology, abbreviations defined on first use.
- [ ] Correct tense per section, passive-voiced methods.
- [ ] Equations in `$$...$$` with `\tag` numbering and defined symbols.
- [ ] Citation placement and forms correct, self-citation used for method continuity.

**Humanization.**
- [ ] No em dashes, semicolons avoided, no mid-sentence ellipses, parentheticals limited.
- [ ] No hedging filler ("it's worth noting") and no stock transitions ("furthermore", "in conclusion").
- [ ] No 1) 2) 3) numbered lists inside section prose.
- [ ] Paragraph first lines indented, sentence openers varied. See `humanization_integration.md`.

**Figures.**
- [ ] Captions are self-sufficient and interpretive and carry at least one quantified value.
- [ ] The archetypal figure set is present: regional context map, composite validation figure, GIS-draped depth slice, method-demonstration figure, multi-panel slice progression.
- [ ] Figures referred to as "Figure N" and placed per venue convention.

**Citations.**
- [ ] Reference list alphabetical, unnumbered, author-date.
- [ ] A classic geophysics text backs any named-but-unelaborated technique.
- [ ] Grey literature included on equal footing.
- [ ] Every in-text citation resolves to a list entry and vice versa.

---

&nbsp;&nbsp;&nbsp;&nbsp;For humanization enforcement see `humanization_integration.md`. For the one-page quick reference see `global_rules_checklists.md`. For per-section depth see the 17 files in `templates/sections/`.
