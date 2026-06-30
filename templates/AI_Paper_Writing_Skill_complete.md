---
name: ai-paper
title: AI-Paper — Complete Self-Contained Writing Skill (Ge-Style DL Papers)
description: Use when writing, drafting, or completing a deep-learning / GPR / geophysics / computer-vision / remote-sensing research paper or any of its sections (abstract, introduction, methodology, experiments, ablation, generalization, application, conclusion), or when a manuscript is partially done and needs the remaining sections developed in a consistent journal style.
version: 1.0
provenance: Extracted by a 9 + 16 agent analyst team from J. Ge et al., "Wavelet-GAN," IEEE TGRS vol. 62, Art. 5918214, 2024.
---

# 🤖 AI-Paper — Complete Writing Skill (Single-File Edition)

> **One self-contained document** packaging the entire AI-Paper writing skill: the operating workflow,
> the global writing rules, and the full per-section "Ge-style" templates (Introduction → Conclusion).
> Reverse-engineered move-by-move from **J. Ge *et al.*, “Wavelet-GAN: A GPR Noise and Clutter Removal
> Method Based on Small Real Datasets,” *IEEE TGRS*, vol. 62, Art. 5918214, 2024.**
>
> This file is the portable/Word-export edition. The split sources live alongside it in
> `Q_TEMPLATE_for_Claude/Paper/` (`MASTER_PAPER_template.md` + `sections/*.md`); the invocable runtime
> skill is `~/.claude/skills/ai-paper/SKILL.md`.

---

## 📑 Table of Contents

1. **Purpose & When to Use**
2. **Operating Workflow**
3. **Global Writing Rules** (US English, tense, equations, figures, citations, units, headings)
4. **Full Paper Skeleton** + structural invariants
5. **Unfinished-Section Policy** ("Yet to be developed")
6. **Section Template — I. Introduction**
7. **Section Template — II. Methodology** (A · B · C-1/2/3 · D)
8. **Section Template — III. Experiments** (A · B · C-1/2/3 · D)
9. **Section Template — IV. Generalization / Fine-Tuning**
10. **Section Template — V. Downstream Application**
11. **Section Template — VI. Conclusion**
12. **Abstract + Index Terms mini-template**
13. **Master Quality Checklist**

---

## 1. Purpose & When to Use

Write, in Ge-style, any of: the **whole paper**, an **individual section**, or the **remaining sections of a
partially-finished manuscript** — keeping consistent structure, voice, and journal formatting.

**Triggers:** drafting/completing a methods paper or any section; a manuscript skeleton needing its pending
sections developed; turning research results into IEEE-ready prose.

**Core principle:** the move-structure and global rules are **fixed**; only the domain content is filled in.
**Never fabricate results** — unfinished work gets an explicit "Yet to be developed" placeholder.

## 2. Operating Workflow

1. Read **§3 Global Rules** and **§4 Skeleton**.
2. Scope the request — whole paper vs sections; inventory done vs pending.
3. **Emit the full skeleton first** (every I–VI heading + subsections, correct IEEE numbering), even for pending parts.
4. For each section, use its template (§6–§11) and fill the slots with the project's content.
5. Apply **every** global rule (§3).
6. Mark pending work with the placeholder (§5) — never invent numbers/figures/tables.
7. Verify against the **Master Checklist** (§13) + each section's checklist.


---

## 3–5 · 13. Global Rules, Skeleton, Unfinished-Section Policy & Master Checklist

> *(from MASTER_PAPER_template.md)*

> A GPR Noise and Clutter Removal Method Based on Small Real Datasets,” *IEEE TGRS*, vol. 62, Art. 5918214, 2024.
>
> **Use with** the per-section templates in `./sections/`:
> `INTRODUCTION_template.md` · `METHODOLOGY_template.md` · `EXPERIMENTS_template.md` ·
> `GENERALIZATION_FINETUNING_template.md` · `APPLICATION_DOWNSTREAM_template.md` · `CONCLUSION_template.md`.
> Each section file holds the move-level fill-in templates; THIS file holds the **global rules** + the
> **assembled skeleton** + the **"unfinished-section" policy**.

---

## 1. 🌐 Global Writing Rules (apply to EVERY section)

### 1.1 Language & spelling
- **US English** throughout (e.g., *normalize, behavior, modeling, fiber, analyze, center, generalization*).
  Never mix in British spellings (*normalise, behaviour, modelling, fibre, centre*).
- Oxford/serial comma **on** ("clutter, noise, and interference").
- One space after periods; no double spaces; straight quotes in code, typographic quotes in prose if the
  converter supports them.

### 1.2 Scientific tone & voice
- Formal, objective, evidence-led. **First-person plural** ("we propose", "we use", "we set") for authorial
  choices; **passive** acceptable for mechanisms/measurements ("the data are normalized", "training was performed").
- Claims are **bounded and falsifiable**; hedge only where honesty requires ("may", "we believe", "preliminarily").
  Reserve hedging for genuine uncertainty — never for the central thesis.
- No marketing language, no exclamation, no rhetorical questions.

### 1.3 Tense convention
| Context | Tense |
|---|---|
| Established facts / definitions / the method's design | present ("GPR is…", "the network consists of…") |
| What the authors did (experiments run) | past ("training was performed", "we collected") |
| Fixed design choices/settings | present ("the Adam optimizer is used") |
| Results being reported | present or past, **consistent** within a paragraph |
| Conclusion recap | present / present-perfect ("is proposed", "the results show") |

### 1.4 Abbreviations & terminology
- Define on first use: **full name (ACRONYM)** — e.g., "ground-penetrating radar (GPR)"; acronym alone thereafter.
- Define once per paper (the Abstract may re-define since it is read standalone).
- **Terminology consistency:** pick one term per concept and use it verbatim everywhere (e.g., always
  "clutter removal", not alternating with "declutter"/"denoising"). Symbol notation fixed once (Methods) and reused.

### 1.5 Equations (md→PDF safe — MANDATORY)
- Inline math `$ … $`; display math `$$ … $$` on its own lines with a blank line above/below.
- Equation numbers as `\tag{n}` **inside** the `$$` block. **Never** `\(…\)`, `\[…\]`, or bare
  `\begin{equation}…\end{equation}` (md→PDF converters mis-parse these and eat subscript underscores).
- **Every** symbol appears inside `$…$` even in prose (protects `_` subscripts). Define all symbols in a
  "where $x$ represents …" sentence **immediately after** the equation.
- Composite losses = explicit weighted sum with named coefficients + their numeric values in a follow-up sentence.

### 1.6 Figures & tables
- Number in order of appearance: **Fig. 1, Fig. 2, …** and **Table I, Table II, …** (tables in Roman numerals, IEEE style).
- **Every** figure/table is referenced in the text **before** it appears ("as shown in Fig. 3", "Table I reports…").
- Reference sub-panels explicitly (Fig. 4(a), Fig. 11(a5)).
- Captions are self-contained: a reader should understand the figure from the caption alone. Result figures put
  raw/input first and the proposed method **last/rightmost**; comparison figures align competitors as columns.
- Co-cite figure + metric table in the same sentence for results ("shown in Fig. X and Table Y").
- State metric direction once (↑ better / ↓ better); **bold** the best value per metric in tables.

### 1.7 Citations
- IEEE numeric style: bracketed `[n]`, numbered by order of first appearance; multiple as `[a], [b]` or `[a]–[c]`.
- Cite the **origin of every borrowed** method/block/loss/metric/dataset at first mention.
- Prior-art review (Introduction §2, Related work) is citation-dense; **thesis, contributions, conclusion are
  citation-free** (the author's own claims).
- Do not cite inside the Methodology overview or the contributions list.

### 1.8 Units, numbers, notation
- SI units with a space before the unit ("256 × 256 pixels", "100 MHz", "2813 s", "6 m"). Use × (not x) for dimensions.
- Numerals for measured/【countable quantities; spell out integers < 10 only in non-technical prose.
- Decimal point (US), not comma; thousands optional comma ("48 000" or "48,000" — pick one and be consistent).
- Ranges with en-dash ("200–900 MHz").

### 1.9 Heading hierarchy (IEEE)
```
TITLE (title case)
Authors · Affiliations · Abstract · Index Terms
I.  SECTION (Roman, small-caps style)         ← top level
    A. Subsection (letter, italic)            ← second level
       1) Sub-subsection (number-paren)       ← third level
```
In markdown source use `#` (title), `##` (I., II., …), `###` (A., B., …), `####` (1), 2), …). Keep the Roman/letter/number
labels in the heading text so md→PDF preserves IEEE numbering.

### 1.10 Reproducibility & archival
- State hardware, optimizer, all hyperparameters, data scale, normalization range, and runtime in the setup subsection.
- Filenames for provenance carry version·date·time where applicable.

---

## 2. 🧱 Assembled Paper Skeleton (full structure)

> Order, with the controlling per-section template named. Fill each via its `sections/*.md` file.

```
TITLE — "[METHOD NAME]: A [DOMAIN] [TASK] Method [Distinguishing Qualifier]"

Authors, Affiliations, corresponding author, funding/grant footnote

ABSTRACT  (≈150–250 words; standalone; see §3 below)
INDEX TERMS  (4–8 alphabetical keywords)

I.   INTRODUCTION                         → sections/INTRODUCTION_template.md
        (M1a field+problem · M1b taxonomy · M2a classical · M2b learning ·
         M3 gap · M4 thesis · M5 contributions · M6 roadmap)

II.  METHODOLOGY                          → sections/METHODOLOGY_template.md
     A. Dataset Preparation
     B. [Enabling Transform / Theory]
     C. [Proposed Model]
        1) Overall Structure
        2) Generator / [Core Module]
        3) Discrimination Network / [Auxiliary Module]
     D. Loss and Evaluation Methods

III. EXPERIMENTS                          → sections/EXPERIMENTS_template.md
     A. Training and Testing
     B. Experiment Results and Comparison
     C. Ablation Study
        1) [Factor 1: e.g. Dataset Composition]
        2) [Factor 2: e.g. Loss Mechanisms]
        3) [Factor 3: e.g. Network Components]
     D. Experiments on [External / Field] Data

IV.  GENERALIZATION EXPERIMENTS …         → sections/GENERALIZATION_FINETUNING_template.md
V.   APPLICATION OF [METHOD] IN [DOWNSTREAM TASK]  → sections/APPLICATION_DOWNSTREAM_template.md
VI.  CONCLUSION                           → sections/CONCLUSION_template.md

REFERENCES   (IEEE style)
AUTHOR BIOGRAPHIES  (optional)
```

**Structural invariants (the load-bearing patterns):**
- **Gap ↔ Contribution 1:1** — the open problems in Intro M3 map exactly onto the contributions in Intro M5,
  and onto the dedicated sections IV/V that demonstrate them.
- **Funnel** — Introduction narrows from field → thesis; Conclusion re-expands by mirroring contributions.
- **Clean hand-offs** — each (sub)section ends by naming the artifact the next consumes.
- **Qualitative-then-quantitative-then-mechanism** — every results claim: show it, measure it, attribute it.
- **Concede-then-fix** — external-validation and capability sections always state one honest limitation + remedy.

---

## 3. ✍️ Abstract + Index Terms (mini-template)

**Abstract** (one paragraph, no citations, no equations, standalone — may redefine acronyms):
> "In **[DOMAIN]** data, **[PROBLEM]** is commonly observed, which **[NEGATIVE EFFECT]**. In this article, we
> propose **[METHOD NAME]**, a **[paradigm]** that **[core mechanism]**. **[METHOD]** can **[capability 1]** and
> **[capability 2]**; additionally, we solve **[secondary problem]** through **[mechanism]**. Our method
> **[high-level how]**. **[METHOD]** uses **[key differentiator, e.g. a small-scale dataset]**, which enables
> **[practical benefit]**. We compare our method with **[baseline classes]** and demonstrate that **[METHOD]**
> performs better in **[setting]**. Finally, we apply this method to **[downstream task]** and test its feasibility."

**Index Terms** (alphabetical, 4–8): `[term], [term], [term], [term].`

---

## 4. 🧩 Unfinished-Section Policy ("Yet to be developed")

When generating a manuscript for work **in progress**, the writer (human or the **AI-Paper** skill) must:

1. **Preserve the full skeleton** — emit every section/subsection heading from §2 with correct IEEE numbering,
   even if its content does not exist yet.
2. **Mark incomplete content explicitly** — under any heading whose work is not done, insert a clearly fenced
   placeholder, never fabricated results:
   ```
   > 🚧 **Yet to be developed.**
   > Planned content: [one-line description of what will go here].
   > Depends on: [data / experiment / result still pending].
   ```
3. **Fully develop everything that *can* be written now** — Introduction, Methodology design, related work,
   loss/metric definitions, and any completed experiments are written in full Ge-style; only genuinely missing
   results/sections get the placeholder.
4. **Never invent numbers, figures, or table values.** A results subsection without data gets the placeholder,
   not a plausible-looking fake table. Figure callouts may be written as `Fig. [N — pending]`.
5. **Keep gap↔contribution alignment** — if a contribution's demonstrating section is "Yet to be developed",
   keep the contribution in the Introduction but flag it as a planned claim in a comment, so the structure stays auditable.

---

## 5. ✅ Master Checklist (whole paper)

- [ ] US English everywhere; terminology consistent; acronyms defined on first use.
- [ ] Tense convention followed per §1.3; tense consistent within each paragraph.
- [ ] All equations `$…$`/`$$…$$` + `\tag{}`; every symbol in math delimiters + glossed.
- [ ] Figures/tables numbered in order, referenced before appearance, captions self-contained, best metric bolded.
- [ ] Citations IEEE-numeric; prior-art dense; thesis/contributions/conclusion citation-free.
- [ ] Units SI with spaces; ranges en-dashed; numbers consistent.
- [ ] Heading hierarchy = IEEE Roman/letter/number, preserved in markdown.
- [ ] Gap↔Contribution 1:1 holds across Intro M3 ↔ M5 ↔ Sections IV/V.
- [ ] Every results claim is qualitative→quantitative→mechanism; fairness caveat present in comparison.
- [ ] External-validation + capability sections each concede one honest limitation + remedy.
- [ ] Incomplete work uses the "Yet to be developed" placeholder; **no fabricated results**.
- [ ] Abstract is standalone, citation/equation-free, ≤250 words; 4–8 alphabetical index terms.

---

### 📎 Provenance
Compiled by a team-lead AI agent from 9 (Introduction) + 16 (Methodology/Experiments/IV/V/VI) parallel
paragraph-analyst agents over the Wavelet-GAN exemplar. Domain-agnostic by construction. Paired with the
**AI-Paper** skill (`AI-Paper.md`) which operationalizes this master template for automated drafting.


---

## 6. SECTION TEMPLATE — I. INTRODUCTION


> **Purpose:** A domain-agnostic, fill-in-the-blank scaffold for writing a strong technical-paper
> Introduction, **reverse-engineered paragraph-by-paragraph** from a high-quality IEEE TGRS exemplar.
> Drop in your own `[PLACEHOLDERS]` and the rhetorical arc, citation discipline, and gap↔contribution
> alignment come for free.
>
> **Source exemplar:** J. Ge *et al.*, “Wavelet-GAN: A GPR Noise and Clutter Removal Method Based on
> Small Real Datasets,” *IEEE Trans. Geosci. Remote Sens.*, vol. 62, Art. 5918214, 2024.
> **Method:** team of 9 paragraph-analysts (one per Introduction paragraph) → team-lead compilation.
> **Author:** Mrinal Kanti Layek — Geophysics & AI Lab, Chonnam National University.

---

## 0. 🧭 The Introduction Arc at a Glance

A complete Introduction is a **funnel**: widest at the top (the field), narrowing to a point (your
thesis), then re-expanding into contributions and a roadmap. The exemplar realizes this in **6 moves
across 9 paragraphs**:

| # | Move | Paras | One-line job |
|---|------|-------|--------------|
| **1a** | Establish topic & importance | P1 | Define the field, how it works, why it matters, name the problem |
| **1b** | Decompose the problem (taxonomy) | P2–P3 | Partition the problem into named categories + physical causes |
| **2a** | Review classical prior art | P4 | Family-by-family: strength → limiting assumption → failure mode |
| **2b** | Review recent (learning) prior art | P5 | Credit the new paradigm, then surface its baked-in weakness |
| **3** | Crystallize the gap | P6 | Enumerate the *specific* open problems (1:1 with contributions) |
| **4** | Announce the solution (thesis) | P7 | One compact sentence: method + headline claims |
| **5** | Enumerate contributions | P8 | Numbered list; each item closes one gap (CLAIM→MECHANISM→BENEFIT) |
| **6** | Paper organization (roadmap) | P9 | Section-by-section preview with ordinal connectives |

**🔑 The single most important design principle:** **Gap ↔ Contribution 1:1 alignment.**
The open problems you list in Move 3 must map *exactly* onto the contributions in Move 5, and each
headline claim in the Move 4 thesis must silently rebut one previously stated limitation. Write Move 3
and Move 5 *together* so the reader can audit that every gap is answered.

```
WIDE   ┌─ M1a  field + problem ────────────────────────┐
       │  M1b  problem taxonomy                          │   "establishing a territory"
       │  M2a  classical prior art + limits              │
       │  M2b  learning prior art + limits               │   "establishing a niche"
NARROW │  M3   THE GAP  (g1, g2, g3) ───────────────┐    │
POINT  │  M4   THESIS  (we propose …) ──────────────┤    │   "occupying the niche"
       │  M5   CONTRIBUTIONS (c1↔g1, c2↔g2, c3↔g3)  │    │
WIDE   └─ M6   roadmap (Sec I…IV) ──────────────────┴────┘
```

---

## 1. 🟦 Move 1a — Establish Topic & Real-World Importance  *(≈ P1)*

**Function:** Orient any reader to the field — define the technology, state its operating principle,
assert its practical value, then pivot in the last 1–2 sentences to the central problem. Widest band
of the funnel; textbook-level, accessible to non-specialists.

**Component slots:** `[DOMAIN DEFINITION]` · `[HOW IT WORKS]` · `[CAPABILITY + 3 APPLICATIONS]` ·
`[THE PROBLEM + CAUSE + CONSEQUENCE]` · `[FIGURE POINTER to problem causes]`

**Fill-in template:**
> "[FIELD/SYSTEM ACRONYM] ([FULL NAME]) is a [SYSTEM CATEGORY] used for [PRIMARY PURPOSE]. It operates
> by [INPUT ACTION] and [MEASUREMENT/RECORDING ACTION]. [ACRONYM] can obtain [TYPE OF OUTPUT/INFO] and
> is commonly employed in [APPLICATION 1], [APPLICATION 2], and [APPLICATION 3] [CIT]. The presence of
> [DEGRADING PHENOMENON] in [DATA TYPE], caused by [GENERAL CAUSE], can introduce significant [NEGATIVE
> EFFECT] and hence limit the [DESIRED QUALITY, e.g. interpretability/accuracy] of the [DATA TYPE] [CIT].
> The different causes of [DEGRADING PHENOMENON] are shown in [FIGURE POINTER]."

**Citation pattern:** Sparse. Cite the **broad-domain/applications** claim and the **problem** claim;
leave definition + mechanism uncited. **Length & tone:** ~5 sentences, simple present, neutral
expository; mechanism/problem sentences lean passive. **Transition out:** the figure pointer + the
named problem hand off to the taxonomy.

---

## 2. 🟦 Move 1b — Decompose the Problem / Taxonomy  *(≈ P2–P3)*

**Function:** Partition the problem named in M1a into a small set of **named categories**, then drill
into each with physical/causal mechanisms so the taxonomy reads as principled, not arbitrary. Establishes
the per-branch scaffold the method will later address one piece at a time + demonstrates domain authority.
Usually **two paragraphs**: one per category (or one for category A, one for category B + its intractability).

**Component slots:** `[TAXONOMY STATEMENT — N named types]` · `[CATEGORY A + DEFINING PROPERTY]` ·
`[SUB-PHENOMENA + PHYSICAL CAUSE each]` · `[SECONDARY CAUSE]` · `[CATEGORY B + SOURCES]` ·
`[ENUMERATED EXAMPLES + catch-all]` · `[WHY UNAVOIDABLE / INTRINSIC]` · `[AGGRAVATING CONDITION]`

**Fill-in template:**
> "We classify the [PROBLEM/PHENOMENON] of [DOMAIN] into [N] types: [CATEGORY A] and [CATEGORY B].
> [CATEGORY A] includes [SUB-PHENOMENON 1] and [SUB-PHENOMENON 2], which typically exhibits [OBSERVABLE
> PROPERTY]. [SUB-PHENOMENON 1] arises when [TRIGGERING CONDITION] [CIT]. [SUB-PHENOMENON 2] typically
> arises from [ROOT MECHANISM] between [COMPONENTS] [CIT]. Another cause of [SUB-PHENOMENON] is
> [SECONDARY MECHANISM] [CIT].
>
> The [CATEGORY B] mainly comes from [HIGH-LEVEL ORIGIN 1] and [ORIGIN 2]. This [CATEGORY B] is highly
> [intricate/complex] and may stem from [MECHANISM] in [ENVIRONMENT], such as [EXAMPLE 1], [EXAMPLE 2],
> [EXAMPLE 3], …, and other unknown sources [CIT]. [CATEGORY B] is unavoidable due to the [INTRINSIC
> PROPERTY] of [SYSTEM] [CIT]. Moreover, when [OPERATING PARAMETER] increases, the proportion of
> [CATEGORY B] also increases [CIT]."

**Citation pattern:** One cite per **mechanism/causal claim**; cluster cites (`[8], [9]`) on the
“intrinsic/unavoidable” assertion. Taxonomy statement itself uncited. **Length & tone:** present tense,
active for the “We classify…” act, passive for mechanisms; concrete enumeration adds vividness.
**Transition out:** framing category B as intrinsic/worsening creates pressure for a remedy → pivots to
the prior-art review.

---

## 3. 🟦 Move 2a — Review Classical (Non-Learning) Prior Art  *(≈ P4)*

**Function:** Survey established solutions grouped into **method-families**, ordered by increasing
sophistication. For each family: name it + representative techniques, credit its genuine strength, then
expose its limiting assumption and failure mode. Builds a cumulative case that *no* classical family
fully solves the problem — fairly, without dismissiveness.

**Component slots (recurring unit, repeat per family):**
`[FAMILY NAME + EXAMPLES]` → `[WHAT IT DOES / STRENGTH]` → `[CORE ASSUMPTION]` → `[FAILURE CONDITION]`.
The load-bearing connective is **“However / based on the assumption that … so …”**.

**Fill-in template:**
> "Many [DOMAIN] [TASK] methods have been developed to solve [PROBLEM].
> [FAMILY 1] approaches, such as [METHOD A] and [METHOD B], are commonly used for [STRENGTH]. However,
> these are only effective when [ASSUMPTION], so performance is not ideal when [FAILURE CONDITION] [CIT].
> Methods based on [FAMILY 2], such as [METHOD C] [CIT] and [METHOD D] [CIT], are very effective at
> [STRENGTH]. [FAMILY 2] is based on the assumption that [ASSUMPTION], so its performance is poor when
> [FAILURE CONDITION].
> Techniques founded on [FAMILY 3], such as [METHOD E] [CIT] and [METHOD F] [CIT], utilize [EXPLOITED
> PROPERTY] to [ACHIEVE GOAL]. However, when [ADVERSE CONDITION], performance is adversely affected, and
> [SECONDARY DRAWBACK, e.g. hyperparameter selection] is also an issue [CIT]."

**Citation pattern:** Dense — cite each **named technique at first mention** *and* cite the
**limitation** claims separately. **Length & tone:** ~8–10 sentences, one dense paragraph; evaluative
but fair, hedged degradation language (“not ideal”, “poor”, “adversely affected”) — bound each method,
never reject it. **Transition out:** end on the residual weakness of the most advanced classical family →
sets up the learning-based pivot.

---

## 4. 🟦 Move 2b — Review Recent (Learning-Based) Prior Art + Emerging Gap  *(≈ P5)*

**Function:** Survey the newest, most credible paradigm (e.g. deep learning) to show the field has
advanced; grant it real strengths so the coming critique is fair; then pivot to a **paradigm-wide**
limitation (here: over-reliance on training-data quality + a baked-in structural assumption) that the
rest of the intro will exploit. The hinge between “state of the art” and “what it still can’t do.”

**Component slots:** `[RECENT-PARADIGM FRAMING]` · `[ENUMERATE APPROACHES + CITES each]` ·
`[ADJACENT HYBRID TREND + CITES]` · `[WHAT THE PARADIGM CAN DO]` · `[GENERAL WEAKNESS — data/quality
dependence]` · `[FAILURE-MODE CONSEQUENCE]` · `[SPECIFIC ASSUMPTION baked into training data]`

**Fill-in template:**
> "In recent years, [PARADIGM]-based methods have garnered considerable attention. [APPROACH A] [CIT],
> [APPROACH B] [CIT], and [APPROACH C] [CIT] have been tried for [TASK]. [ADJACENT TECHNIQUE] has also
> been widely combined with [PARADIGM] methods [CIT]. The method based on [PARADIGM] can [CORE CAPABILITY]
> by [MECHANISM]. These [PARADIGM]-based methods are usually based on [TYPICAL FEATURE/ASSUMPTION], so one
> disadvantage is that they highly rely on the quality and features of the [DATASET]. If the actual [DATA]
> deviate from the [TRAINING DATA], the accuracy of the [MODELS] may suffer. Typically, the models are
> trained using data that exhibit [SPECIFIC PATTERN], commonly associated with [CANONICAL SCENARIO]."

**Citation pattern:** Technique-anchored — each named approach carries its own cite; hybrid trend gets a
paired group. The **weakness/assumption sentences carry no citation** (your own critique → signals the
gap transition). **Length & tone:** ~7 sentences; tone shifts mid-paragraph from even-handed to
critical, hedged with “may / usually / typically / some of the disadvantages.” **Transition out:** end
on the *specific* baked-in assumption (deliberately mid-thought) → launches the explicit gap paragraph.

---

## 5. 🟥 Move 3 — Crystallize the Research Gap (Enumerated Open Problems)  *(≈ P6)*

**Function:** Convert diffuse “needs improvement” tension into a tight, numbered set of **specific,
solvable** problems. Engineer the enumeration to map **1:1 onto the later contributions** (Move 5), so
each gap pre-justifies a method component. Funnel from general → one domain-specific mechanism-level
deficiency, priming “In this article, we propose…”.

**Component slots:** `[GAP 1 — GENERALIZATION / OOD]` · `[GAP 2 — DATA HUNGER (+ partial existing
remedy)]` · `[GAP 3 — DOMAIN-SPECIFIC CONFLICT (+ concrete example)]`. Connectives:
**“When … is limited”, “Another issue is …”, “In addition …”, “For example …”.**

**Fill-in template:**
> "Because [DOMAIN] conditions can be intricate, [SIGNAL/OBSERVATION] does not always follow the expected
> [CANONICAL PATTERN] due to [VARIED CAUSES]. When the [PROCESSED/TEST DATA] differ significantly from the
> [TRAINING DATA], the generalization ability of [METHOD CLASS] is limited [CIT]. Another issue is that,
> to achieve ideal results, [METHOD CLASS] typically requires a large number of [TRAINING DATA] [CIT], and
> [PARTIAL REMEDY] is used to address this problem [CIT]. In addition, different [MECHANISMS] focus on
> different [DIMENSION], leading to [CONFLICT NAME] [CIT]. For example, [METHOD A with SETTING] tends to
> [CAPTURE PROPERTY 1], while [METHOD B] tends to [CAPTURE PROPERTY 2]."

**Citation pattern:** Every named open problem anchored to 1–2 prior works; remedy + conflict get single
cites. No uncited problem claims. **Length & tone:** ~5 sentences, compact, declarative; critical-but-
constructive — each gap is a tractable target. **Transition out:** the general→specific funnel leaves an
obvious unmet need a single method must reconcile → the thesis sentence.

---

## 6. 🟥 Move 4 — Announce the Proposed Solution (Thesis Sentence)  *(≈ P7)*

**Function:** Pivot from problem-space to solution-space in **one compact sentence**: name the method,
then load it with headline claims that each silently close a gap. Generality claims rebut “prior methods
are narrow”; the key differentiator (e.g. “no hyperparameters”) rebuts the usability/reproducibility
limitation. Brevity signals this is the paper’s central claim.

**Component slots:** `[SIGNPOST "In this article, we propose"]` · `[METHOD ONE-LINER = paradigm + task]`
· `[SCOPE/GENERALITY CLAIMS — enumerated robustness axes, each ↔ a gap]` · `[KEY DIFFERENTIATOR]`

**Fill-in template:**
> "In this article, we propose a [PARADIGM]-based [TASK] method that is applicable to almost all types of
> [AXIS 1], [AXIS 2], [AXIS 3], and [AXIS 4], and does not require [BURDENSOME REQUIREMENT OF PRIOR WORK]."

*Variant:* "In this article, we propose [METHOD NAME], a [METHOD ONE-LINER] that generalizes across
[SCOPE CLAIMS] while eliminating the need for [KEY DIFFERENTIATOR]."

**Citation pattern:** **None** — this is your own contribution claim. **Length & tone:** deliberately one
assertive sentence; only calibrated hedge is “almost all.” **Transition out:** unpacks into the numbered
contributions.

---

## 7. 🟥 Move 5 — Enumerate Contributions (Gap-Aligned)  *(≈ P8)*

**Function:** A numbered ledger asserting **1:1 closure** of each gap from Move 3 (c1↔g1, c2↔g2, c3↔g3).
Each bullet doubles as a forward map to a methods/experiments section. Positions the paper as complete
and self-justifying.

**Per-contribution sub-structure:** `[HEADLINE CLAIM]` → `[MECHANISM — how achieved]` →
`[BENEFIT or VALIDATION]`.

**Fill-in template:**
> "The main contributions of this study are as follows.
> 1. [HEADLINE CLAIM — named method/capability] is proposed to [core task / close gap #1]. It [MECHANISM
>    — combines technique A and technique B] to [effect], effectively solving [gap #1]. This [BENEFIT —
>    improves/preserves ___].
> 2. [HEADLINE CLAIM — capability] is achieved. We [MECHANISM — adopt technique C and technique D]. This
>    [BENEFIT — reduces/saves ___], closing [gap #2].
> 3. We [verb: preliminarily solve] [problem of gap #3], even when [hard condition]. By [MECHANISM —
>    e.g. fine-tuning / transfer learning], we [outcome], verified through [VALIDATION — experiment on ___]."

*Generic repeatable bullet:* "N) [CLAIM]. By [MECHANISM], we [BENEFIT]. [VALIDATION]."

**Citation pattern:** **Self-referential / none** — points only to your own method, components, and
experiments (those components were cited earlier). **Length & tone:** numbered list, 3–4 sentences/item,
assertive (“is proposed”, “is achieved”); reserve hedging (“preliminarily”) for the riskiest claim.
**Transition out:** seeds the roadmap (or hands directly into Methodology).

---

## 8. 🟦 Move 6 — Paper Organization / Roadmap  *(≈ P9)*

**Function:** Section-by-section preview — a navigational contract so readers locate methodology,
validation, extension, and application without searching. Signals completeness of scope and closes the
Introduction.

**Component slots:** `[SIGNPOST]` · `[SECTION N → content]` ×K, carried by ordinal connectives
**first → then → also → finally**.

**Fill-in template:**
> "In this article, we first introduce the [methodology] that [METHOD NAME] relies on in Section [N],
> including [component 1], [component 2], and [component 3]. Then, [experiments] are conducted on both
> [data A] and [data B] to verify its effectiveness in Section [N]; we compare the proposed method with
> [baselines]. We also present a [experiment type] to test [capability] in Section [N]. Finally, we
> conduct [extension/application] with [downstream task] in Section [N]."

*Generic one-liner:* "Section [N] [introduces / presents / evaluates / extends / applies] [content]."

**Citation pattern:** **None** (self-referential to your own sections). **Length & tone:** ~4–6
sentences, declarative, first-person plural, ordinal rhythm. **Transition out:** terminates the
Introduction → body sections.

---

## 9. ✅ Author Checklist (verify before moving on)

- [ ] **M1a** opens at field level (a non-specialist could follow sentence 1) and names the problem by the end.
- [ ] **M1b** taxonomy uses *named* categories, each grounded in a physical/causal mechanism (not assertion).
- [ ] **M2a** every classical family follows *strength → assumption → failure*; each method cited at first mention.
- [ ] **M2b** the new paradigm is *credited* before it is *critiqued*; weakness sentences are uncited (your voice).
- [ ] **M3** gaps are **enumerated** and **specific**, each cited, funnelling general → specific.
- [ ] **🔑 Gap↔Contribution 1:1**: count(gaps in M3) == count(contributions in M5), and they correspond in order.
- [ ] **M4** thesis is **one sentence**, uncited, every headline claim rebuts a prior limitation.
- [ ] **M5** each contribution = CLAIM → MECHANISM → BENEFIT/VALIDATION; hedge only the riskiest item.
- [ ] **M6** roadmap covers *every* body section with ordinal connectives.
- [ ] Citation discipline: dense in prior-art (M2), anchored on claims in M1b/M3, **absent** in M4/M5/M6.
- [ ] Funnel shape holds: each paragraph is narrower in scope than the one before, up to the thesis.

---

## 10. 🧱 Blank Skeleton (copy-paste & fill)

```text
[P1 / M1a]  <field def> · <how it works> · <capability + 3 apps [cit]> · <the problem + cause + effect [cit]> · <Fig pointer>
[P2 / M1b]  We classify <problem> into N types: <A> and <B>. <A includes …, mechanisms [cit]> …
[P3 / M1b]  <B comes from …, enumerated examples [cit]> · <why unavoidable [cit]> · <aggravating condition [cit]>
[P4 / M2a]  Many <task> methods exist. <Family1 + ex + strength + However + failure [cit]> <Family2 …> <Family3 …>
[P5 / M2b]  In recent years, <paradigm> … <approach A [cit], B [cit], C [cit]> … <can do X> … <BUT relies on data; assumption …>
[P6 / M3]   <gap1 generalization [cit]> · <gap2 data hunger + partial remedy [cit]> · <gap3 domain conflict + example [cit]>
[P7 / M4]   In this article, we propose <method> applicable to <axis1..4> and not requiring <burden>.
[P8 / M5]   The main contributions are: 1) <claim→mech→benefit> 2) <…> 3) <…>
[P9 / M6]   first Section I <method>; then Section II <validation+compare>; also Section III <extension>; finally Section IV <application>.
```

---

### 📎 Provenance
Compiled by team-lead from 9 parallel paragraph-analyst agents (one per Introduction paragraph of the
Wavelet-GAN exemplar). Generic/domain-agnostic by construction — reuse for any signal-processing,
remote-sensing, or deep-learning methods paper. Math (if added) must use `$…$` / `$$…$$` delimiters so
md→PDF renders correctly.


---

## 7. SECTION TEMPLATE — II. METHODOLOGY


> Domain-agnostic scaffold for the Methods section of a deep-learning methods paper, reverse-engineered
> paragraph-by-paragraph from J. Ge *et al.*, “Wavelet-GAN…,” *IEEE TGRS*, vol. 62, Art. 5918214, 2024 (§II).
> Built by a 7-agent analyst team (overview · A · B · C-1 · C-2 · C-3 · D) → team-lead compilation.
> **Math rule (mandatory):** all equations use `$…$` / `$$…$$` with `\tag{n}` **inside** the block —
> never `\(…\)`, `\[…\]`, or bare `\begin{equation}` (md→PDF converters break those).

---

## 0. 🧭 Methodology Sub-Architecture

| Sub | Move | Job |
|-----|------|-----|
| **II (open)** | Roadmap | Preview the A/B/C/D pillars in the order they appear |
| **II.A** Dataset Preparation | Data construction | Recast problem as a data model `D=A+B+C`; synthesize paired data + augmentation |
| **II.B** Transform / Theory | Math foundation | Formalize the enabling transform; prove it separates signal components |
| **II.C.1** Overall Structure | Architecture overview | End-to-end data flow, module inventory, anchored to master figure |
| **II.C.2** Generator | Component deep-dive | Design-rationale-first, then per-subnet block specs |
| **II.C.3** Discrimination Net | Adversarial deep-dive | Discriminator structure + alternating training + loss objectives |
| **II.D** Loss & Evaluation | Objective + metrics | Per-branch losses → weighted composite → synthetic vs real metrics |

**Ordering rule:** the comma-separated pillars listed in the II opening paragraph must appear in the
**same order** as the lettered subsections — the preview doubles as a forward index.

---

## 1. Methodology Overview *(II opening, ≈3 sentences)*

**Role:** roadmap of the proposed approach. **Function:** in one breath state *what* the section delivers
and *how* the method achieves its goal, compressed into named pillars = a mental table of contents.

**Slots:** `[SECTION SCOPE]` · `[TASK/GOAL]` · `[CONSTRAINT/SETTING]` · `[PILLAR_1…N]` · `[HEADLINE OUTCOME]`

**Fill-in:**
> "In this section, we introduce the **[SECTION SCOPE]** used for **[TASK/GOAL]**, and describe the
> **[secondary artefacts — dataset and loss]** employed in this work. We achieve **[TASK/GOAL]** under
> **[CONSTRAINT/SETTING]** through **[PILLAR_1]**, **[PILLAR_2]**, **[PILLAR_3]**, and **[PILLAR_N]**.
> By using **[approach]**, we solve the problem of **[HEADLINE OUTCOME]**."

**Citations:** none. **Figures/eqns:** none (no forward refs in the preview). **Tone:** ~3 sentences,
present tense, first-person plural, abstract — no symbols/numbers. **Transition:** the lettered heading
`A.` *is* the transition; first pillar named = title of subsection A.

---

## 2. II.A — Dataset Preparation

**Role:** first subsection; establish the data model + synthetic-dataset generation pipeline before any
architecture. **Function:** reframe the application problem as a decomposition of the observed signal,
justify why labels must be *synthesized*, and present each augmentation as a defense against poor generalization.

**Paragraph flow:** (1) problem-as-data-model → (2) why naive/end-to-end is hard (input vs label) →
(3) compromise strategy (real component + simulated target; simulation-reality gap) → (4) label & background
sourcing with counts → (5) augmentation enumeration → (6) synthesis recipe + pipeline figure.

**Slots:** `[DATA DECOMPOSITION MODEL]` · `[TASK REFRAMING]` · `[LEARNING-PARADIGM CONTRAST]` ·
`[SIM-REALITY GAP]` · `[LABEL SOURCING +counts]` · `[BACKGROUND SOURCING]` · `[AUGMENTATION OPS]` ·
`[SYNTHESIS RECIPE]` · `[PIPELINE FIGURE]`

**Fill-in:**
> "From a mathematical perspective, **[OBSERVED DATA]** consists of **[COMPONENT A]**, **[COMPONENT B]**,
> and **[COMPONENT C]**: $D = A + B + C$. The **[TASK]** can be seen as extracting **[TARGET]** from real
> **[OBSERVED DATA]**; the function $T = F(D)$ represents the process of **[RECOVERING TARGET]** [CIT].
> When training, we treat the raw **[OBSERVED DATA]** as input and the expected **[CLEAN RESULT]** as the
> label. While this can also be solved using **[SIMULATION]**, factors such as **[REAL-WORLD FACTORS]**
> cannot be fully reproduced, so the differences between simulated and real data are inevitable [CIT].
> Based on $D=A+B+C$, we adopt a compromise of adding **[TARGET]** to real **[BACKGROUND]** data [CIT].
> For labels, **[N₁]** real and **[N₂]** simulated **[TARGET]** data are used; simulation is generated by
> **[TOOL]** [CIT]. Simply combining target and background one-to-one yields limited variability, so we
> propose a data-augmentation method: **First**, the **[TARGET]** is extracted by **[METHOD]**. **Second**,
> we randomly transform the **[SCALE/GEOMETRY]**… **Third**, we apply random **[STYLE]** changes
> (**[PARAMS]**), add **[NOISE]** with **[STAT]**, **[FILTER]** over a random **[RANGE]**, and adjust
> **[ENERGY]** by a random **[COEFFICIENT]**. Finally, the transformed **[TARGET]** is randomly matched
> with real measured **[BACKGROUND]** to produce the final paired dataset."

**Equations:** inline `$D=A+B+C$`, `$T=F(D)$`. **Figure:** introduce the pipeline once
("The preparation process is shown in Fig. [N]."), then narrate stages in order. **Citations:** one per
claim (problem formulation, borrowed compromise, simulator/augmentation library). **Tone:** ~5–7 paragraphs,
justificatory ("due to… in order to… therefore…"), first-person plural, explicit numbers/params.
**Transition:** close on the completed dataset → next subsection consumes it.

---

## 3. II.B — Transform / Mathematical Foundation

**Role:** formalize the enabling transform/theory and tie it to the problem — the analytical bridge between
"here is the problem" and "here is the model that exploits this math." **Function:** establish the architecture
is principled (citeable transform properties), fix notation reused downstream, and *earn the right* to use the
transform as preprocessing by showing it separates target from nuisance components.

**Paragraph flow:** (1) define transform + cite origin → (2) governing equations → (3) multi-level
decomposition + structure figure → (4) empirical/analytic justification (controlled synthetic model →
which subbands hold nuisance vs target) + figure.

**Slots:** `[TRANSFORM DEFINITION]` · `[GOVERNING EQUATIONS w/ tag]` · `[DECOMPOSITION STRUCTURE + FIGURE]` ·
`[SYMBOL GLOSSARY]` · `[WHY-IT-HELPS ANALYSIS + FIGURE]`

**Fill-in:**
> "In this section, we analyze the **[response/structure]** characteristics of **[problem data]** using
> **[TRANSFORM]** [CIT]. The **[base algorithm]** [CIT] of **[d]-D [TRANSFORM]** can be expressed as"
>
> $$ \text{COMP}_{j+1}(m,n) = \sum_{l\in z}\sum_{k\in z} f_{l-2m}\, f_{k-2n}\, X_j(l,k) \tag{1} $$
>
> "where $m, n, l, k$ represent the calculation indices, $j$ represents the decomposition level, and
> $f_{\cdot}$ represent the low-/high-pass filters. After **[N]**-order decomposition, an input of size
> $H \times W$ yields **[K]** subbands at **[J]** scales (see Fig. [N]). To analyze how **[TRANSFORM]**
> separates **[components]**, we use **[tool]** [CIT] to build a controlled model containing
> **[structures]**; the result is shown in Fig. [N]. **[Nuisance X]** is observed in **[subband(s)]** but
> almost eliminated elsewhere; owing to the **[property]** of **[TRANSFORM]**, **[X]** can be effectively
> separated. Therefore, the preprocessing of **[TRANSFORM]** is helpful for the **[downstream method]**."

**Equations:** numbered display (`$$…$$` + `\tag{}`), symbol glossary immediately after, inline symbols in
`$…$`. **Figures:** structural figure (decomposition tree, mapped to equations) + justification figure
(synthetic model → corrupted → transformed, interpreted subband-by-subband). **Citations:** transform
lineage + analysis tool. **Tone:** 3–5 paragraphs, formal/declarative; mild hedge only on the concluding
claim ("we believe… is helpful"). **Transition:** name the artifacts (subbands/coefficients) the model consumes.

---

## 4. II.C.1 — Overall Structure (Architecture Overview)

**Role:** present the complete network as a system before per-component deep-dives. **Function:** answer
"what are the parts, in what order does data move, why is each there" in one pass anchored to the master figure;
stay at system altitude, defer mechanics.

**Paragraph flow:** (1) component inventory → (2) input decomposition into branches → (3) per-branch processor
+ its loss → (4) inter-branch coupling/guidance → (5) output reconstruction.

**Slots:** `[COMPONENT INVENTORY]` · `[INPUT DECOMPOSITION]` · `[PER-BRANCH PROCESSOR + LOSS]` ·
`[INTER-BRANCH COUPLING]` · `[OUTPUT RECONSTRUCTION]` · `[ARCHITECTURE FIGURE]`

**Fill-in:**
> "As shown in Fig. **[ARCH]**, the **[METHOD]** network consists of **[INPUT DECOMPOSITION]** and
> **[OUTPUT RECONSTRUCTION]** modules, **[PROCESSOR FAMILY]** generators, and **[N]** discriminators. The
> purpose of the **[generator]** is to map **[degraded input]** to **[clean target]**, while the
> **[discriminator]** determines whether its input is true (label) or false (generator). First, the input
> is decomposed into **[BRANCH-1]**, **[BRANCH-2]**, and **[BRANCH-3]** via **[INPUT DECOMPOSITION]**. The
> **[BRANCH-1]** data are processed by **[PROCESSOR-1]** under **[LOSS-1]**; the **[BRANCH-2]**/**[BRANCH-3]**
> data are processed by **[PROCESSOR-2]** under **[LOSS-2]**. The feature map from **[PROCESSOR-1]** is also
> fed to the higher-level processors to guide **[BRANCH-2/3]**. Finally, the reconstructed branches are
> synthesized as the output through **[OUTPUT RECONSTRUCTION]**."

**Figure:** one master architecture figure, cited in sentence 1; component sub-diagrams deferred to C.2/C.3.
**Equations:** mostly prose; inline `$\hat T = G_\theta(D)$` only if needed. **Citations:** cite each adopted
sub-module at first mention; the architecture itself uncited. **Tone:** 1–2 compact paragraphs, declarative,
present tense, role-before-mechanism. **Transition:** to the Generator deep-dive.

---

## 5. II.C.2 — Generator (Component Deep-Dive)

**Role:** justify and specify each generator sub-network — **design-rationale-first, mechanism-second.**
**Function:** convert the architecture choice into per-component engineering commitments traceable to a
purpose and a prior source.

**Paragraph flow:** (1) why-this-design (band split + supervision asymmetry + lower→higher guidance) →
(2) sub-net A spec (blocks + purpose + dual output) → (3) sub-net B spec + figure → (4) coupling/alignment.

**Slots:** `[DESIGN RATIONALE]` · `[SUB-NET A blocks]` · `[SUB-NET B blocks + FIGURE]` · `[COUPLING/ALIGNMENT]`

**Fill-in:**
> "Because **[branch X]** handles **[property]**, we recover it with a **[network-type]** under
> **[objective]**, whereas **[branch Y]** requires **[adversarial scheme]** to reconstruct **[property the
> objective cannot supervise]**. In the network, **[downstream component]** must be guided by **[upstream
> component]**, so **[alignment]** between **[scales/bands]** is required. We use **[SUB-NET A]** [CIT],
> composed of a **[base mechanism]** with **[auxiliary mechanism]** [CIT], to achieve **[purpose]**;
> specifically, it adopts **[block]** that uses **[mechanism]** to **[effect]**. The feature map it
> generates is also passed to **[downstream components]** to guide their generation. We use **[SUB-NET B]**
> [CIT] based on **[mechanism]** to achieve **[correspondence]**; as shown in Fig. **[N]**, it consists of
> **[block 1]**, **[block 2]**, and **[block 3]**, and aligns features by training **[the modulation
> parameters]**."

**Figure:** sub-block diagram for the non-obvious sub-net ("As shown in Fig. N, it consists of…").
**Equations:** qualitative; inline `$\gamma,\beta$` if needed. **Citations:** every borrowed sub-net/block
cited at first mention; "We use… based on…" signals reuse. **Tone:** 3–4 paragraphs, present tense,
constraint→consequence then block→purpose; effects are design *intentions*, not measured. **Transition:** to discriminator.

---

## 6. II.C.3 — Discrimination Network (Adversarial Deep-Dive)

**Role:** specify the discriminator + the alternating adversarial training + its loss objectives.
**Function:** turn "generator vs discriminator" into a concrete training loop anchored by a workflow figure,
then formalize it as paired objectives, preparing the consolidated loss in II.D.

**Paragraph flow:** (1) discriminator structure (count, shared, branch assignment) → (2) alternating training
+ figure → (3) discriminator objective + generator adversarial objective, each with glossary.

**Slots:** `[DISCRIMINATOR STRUCTURE]` · `[ADVERSARIAL PROCEDURE + FIGURE]` · `[DISCRIMINATOR OBJECTIVE]` ·
`[GENERATOR ADVERSARIAL OBJECTIVE]` · `[SYMBOL GLOSSARY]`

**Fill-in:**
> "We employ **[N]** discriminators with the same structure, each paired with the corresponding **[output
> subband]** of the generator. As shown in Fig. **[N]**, the generator and discriminator are trained in turn
> each epoch: first the discriminator is trained on both **[real]** and **[generated]** data to distinguish
> them; subsequently, only generated data are fed to the trained discriminator and the generator is trained
> so its output is authenticated as real. The difference between the two processes lies in the input data,
> the loss function, and the training section. The target loss of the **[n]**th discriminator is"
>
> $$ L_{D_n} = \mathbb{E}_{Y_n^{\text{high}}}\!\big[\mathrm{ReLU}(1 - D_n(Y_n^{\text{high}}))\big] + \mathbb{E}_{F(x)_n^{\text{high}}}\!\big[\mathrm{ReLU}(1 + D_n(F(x)_n^{\text{high}}))\big] \tag{2} $$
>
> "where $Y_n^{\text{high}}$ is the real high-frequency data, $D_n$ the $n$th discriminator, and
> $F(x)_n^{\text{high}}$ the data from the $n$th generator. The generator adversarial objective is"
>
> $$ L_{G} = -\sum_{n=1}^{N_w} \mathbb{E}_{F(x)_n^{\text{high}}}\!\big[D_n(F(x)_n^{\text{high}})\big] \tag{3} $$
>
> "where $N_w$ is the number of high-frequency subbands."

**Equations:** numbered loss eqns → "where `$symbol$` represents…" glossary; second glossary refers back to
first. **Figure:** GAN train workflow (two-phase loop). **Citations:** borrowed loss/activation only.
**Tone:** 3 short paragraphs + 2 eqns, procedural ("First…, Subsequently…"). **Transition:** to II.D ("we next
consolidate them with the reconstruction/feature/perceptual terms into the overall loss").

---

## 7. II.D — Loss & Evaluation Methods

**Role:** equation-dense optimization-and-metrics subsection closing the Methods section. **Function:** one
tailored loss per branch → linear weighted composite → separate train-time losses from eval-time metrics;
the synthetic-vs-real split is load-bearing (real data has no clean reference → relative metric).

**Paragraph flow:** (1) per-branch losses (4)(5)(6) → (2) composite weighted objective (7) + weights →
(3) synthetic metrics (8)(9)(10) → (4) real-data metric + rationale (11)(12).

**Slots:** `[PER-BRANCH LOSS eqns]` · `[COMPOSITE OBJECTIVE + WEIGHTS]` · `[SYNTHETIC METRICS]` ·
`[REAL-DATA METRIC + WHY]`

**Fill-in:**
> "We use **[loss]** in the **[low/coarse branch]**: $$ L_{\text{low}} = [\text{expr}] \tag{4} $$
> In the **[detail branches]** we use **[adversarial loss]** (2)–(3) and, to achieve feature
> correspondence, **[feature-matching loss]**: $$ L_{\text{FM}} = [\text{expr}] \tag{5} $$
> We also adopt **[perceptual loss]** based on a pretrained **[network]** [CIT]:
> $$ L_p = [\text{expr}] \tag{6} $$
> The overall objective linearly combines these with **[adjustment factors]**:
> $$ L = \min_{G}\max_{D}\big(\lambda_{\text{low}} L_{\text{low}} + L_{G} + \lambda_f L_{\text{FM}} + \lambda_p L_p\big) \tag{7} $$
> where we set $\lambda_{\text{low}}=[\,]$, $\lambda_f=[\,]$, $\lambda_p=[\,]$, respectively. For **[synthetic]**
> data we use **[PSNR]** [CIT] and **[SSIM]** [CIT] (eqns 8–10). For **[real]** data we cannot obtain the
> ideal clean reference, so reference-based metrics cannot be computed; we therefore use **[improvement
> factor]** [CIT]: $$ \mathrm{IF} = [\text{expr}] \tag{11} $$ with **[constituent ratio]** defined in (12)."

**Equations:** the canonical formatting exemplar — `$$…$$`+`\tag{}`, immediate `$…$` glossary, weighted-sum
composite with named λ + numeric values, paired metric eqns. **Citations:** origin of every borrowed loss/metric
(`full name (ACRONYM) [cit]` first use). **Tone:** 4–6 short paragraphs, formula-driven, declarative, present
tense; prose only names → introduces eqn → glosses symbols. **Transition:** to Experiments ("we conduct
experiments… and ablations that verify each component").

---

## 8. ✅ Methodology Checklist

- [ ] Opening previews pillars in the **same order** as the lettered subsections.
- [ ] II.A states the data model `$D=A+B+C$`, the input/label definition, and enumerates augmentations with params.
- [ ] II.B gives numbered equations + immediate symbol glossary, and a figure proving component separation.
- [ ] II.C.1 anchors one master architecture figure and walks data input→output before any deep-dive.
- [ ] II.C.2 is rationale-first; every borrowed block carries a citation.
- [ ] II.C.3 presents the alternating loop + the two numbered adversarial objectives with glossaries.
- [ ] II.D defines per-branch losses → weighted composite (with numeric λ) → synthetic metrics → real-data metric + why.
- [ ] **All equations** use `$…$`/`$$…$$` with `\tag{}` inside; no `\(…\)`/`\[…\]`/`\begin{equation}`.
- [ ] Borrowed components/losses/metrics cited at first mention; the contribution itself uncited.
- [ ] Each subsection ends by naming the artifact the next subsection consumes (clean hand-offs).


---

## 8. SECTION TEMPLATE — III. EXPERIMENTS


> Domain-agnostic scaffold for the Experiments section, reverse-engineered from J. Ge *et al.*,
> “Wavelet-GAN…,” *IEEE TGRS*, vol. 62, Art. 5918214, 2024 (§III). Built by a 6-agent analyst team
> (A · B · C-1 · C-2 · C-3 · D) → team-lead compilation.

---

## 0. 🧭 Experiments Sub-Architecture

| Sub | Move | Job |
|-----|------|-----|
| **III.A** Training & Testing | Setup + roadmap | Map the subsections; give reproducible hardware/hyperparams/data |
| **III.B** Results & Comparison | Benchmark | Beat classical then learned baselines; qualitative→quantitative→why |
| **III.C** Ablation Study | Decompose | 3 parallel units: dataset / loss / architecture, one shared micro-pattern |
| **III.D** Field/External Data | External validation | Robustness on independent, third-party real data |

---

## 1. III.A — Training and Testing (Setup + Roadmap)

**Role:** bridge that opens Experiments — section roadmap, then reproducible implementation block.
**Function:** establish credibility/reproducibility *before* any result; separate "how we ran it" from "what we got."

**Paragraph flow:** (1) section roadmap → (2) hardware → (3) optimizer+hyperparams → (4) data pipeline/normalization
→ (5) data scale + runtime → (6) process-illustration figure.

**Slots:** `[SECTION ROADMAP]` · `[HARDWARE]` · `[OPTIMIZER+HYPERPARAMS]` · `[DATA PREP/NORMALIZATION]` ·
`[DATA SCALE + RUNTIME]` · `[PROCESS FIGURE]`

**Fill-in:**
> "In this section, we conduct experiments to test the performance of **[METHOD]**. Section **[X-A]**
> introduces the implementation details; Section **[X-B]** presents the results and compares with
> **[traditional]** and **[deep-learning]** methods; Section **[X-C]** presents ablation experiments that
> verify the key parts of our network; Section **[X-D]** applies **[METHOD]** to **[external data]**.
> The training is performed on a **[OS]** server using **[CPU]** with **[N] [GPU]** GPUs. We set the batch
> size as **[B]** and the number of epochs to **[E]**. The **[OPTIMIZER]** optimizer is used with a learning
> rate of **[LR]**, which continuously decreases from the **[K]**th epoch. During training, each input is
> randomly matched with **[M]** transformed targets, so every dataset may differ across epochs; all samples
> are resized to **[H×W]** and normalized to **[LOW–HIGH]**. There are **[N]** combined data trained, and the
> training took **[T]** s. The data extracted at different steps are shown in Fig. **[N]** (from the **[K]**th
> epoch): **[stage-1]** is the input synthesized from **[components]**; **[METHOD]** first **[step]** and then
> **[final step]**."

**Figure:** one process-illustration figure (columns = pipeline stages, rows = examples); walk left→right.
**Citations:** mostly none; cite only a named external dataset flagged for later use. **Tone:** roadmap = 1
paragraph; setup = 1–2 dense paragraphs; **past tense** for actions, present for fixed choices; every constant
stated. **Transition:** to results/comparison.

---

## 2. III.B — Experiment Results and Comparison

**Role:** experimental-evidence + head-to-head benchmarking. **Function:** two-channel argument — qualitative
figure read (*what* it preserves/removes) + quantitative table read (*how much* it wins) — closed by attributing
the win to a **mechanism**, insulated by a fairness caveat.

**Paragraph flow:** (1) set up baseline tier(s) + fig/table → (2) qualitative figure reading → (3) quantitative
table reading → (4) superiority claim + reason → (5) fairness caveat.

**Slots:** `[BASELINE SET A + fig + table]` · `[BASELINE SET B + fig + table]` · `[QUALITATIVE OBSERVATION]` ·
`[QUANTITATIVE COMPARISON]` · `[WHY-WE-WIN]` · `[FAIRNESS NOTE]`

**Fill-in:**
> "The processing results of **[BASELINE_SET]** and our method on **[DATA]** are shown in Fig. **[X]** and
> Table **[Y]**, together with the **[METRIC LIST]**. It can be observed that **[COMPETITOR]** **[leaves /
> distorts / cannot remove]** **[ARTIFACT/DETAIL]**, while our method **[preserves / reconstructs]**
> **[TARGET FEATURE]** with the most comprehensive depiction of detail. Compared with **[COMPETITOR_1]**,
> **[COMPETITOR_2]**, …, our method achieves the best **[METRIC]** (**[value]**). This advantage is
> attributed to **[MECHANISM]**, which **[preserves/aligns/enhances]** **[FEATURE]** that competitors discard.
> It should be emphasized that, to ensure fairness, all **[METHOD CATEGORY]** use **[the same dataset /
> identical noise / equal epochs / identical inputs]**."

**Figures & tables:** co-cite in the same sentence (figure = qualitative, table = quantitative); each tier gets
its own fig+table pair; read table per-metric (state ↑/↓ once, name the best cell). **Interpretation:**
qualitative→quantitative→attribute-to-mechanism (numbers confirm the eye; mechanism explains both).
**Citations:** each baseline named with inline ref + one-clause identity. **Tone:** 2–4 paragraphs, assertive
but bounded — every win backed by figure callout + table value + mechanism. **Transition:** to ablation.

---

## 3. III.C — Ablation Study (3 Parallel Units, ONE Shared Micro-Template)

**Shared micro-template** (instantiate 3×): **remove/swap one factor → name the variant + model ID → cite its
figure panel-pair `(aᵢ)`/`(bᵢ)` and table row → interpret degradation → state necessity.** Only three things
change per unit: the **factor type** (data ↔ loss term ↔ architecture block), the **removal operation**
(substitute data / zero a loss weight / replace a block with a trivial op), and the **model IDs + panel-pairs +
table rows**. Reserve the climactic **"plays a crucial role"** superlative for the **final** unit only.

**Generic ablation-unit fill-in:**
> "To investigate the effect of **[ABLATED FACTOR]**, in Model **[N]** we **[toggle/remove/replace the
> factor]**. The results of Model **[N]** are shown in **[(aᵢ)]** and **[(bᵢ)]** of Fig. **[X]** and Table
> **[Y]**. It is observed that **[the variant lacking the factor]** **[is limited / degrades / approximates
> the full model but…]**, as its results **[symptom]**, while the full model performs better. *(Caveat where
> relevant:)* It is worth mentioning that **[CONFOUND, e.g. reduced data volume]**, which may also contribute."

**Figure & table convention (all units):** cite panels by exact label, pairing synthetic row `(aᵢ)` with real
row `(bᵢ)` for the same model; co-cite the table in the same sentence; refer to variants by stable model IDs
that map 1:1 to table columns. **Citations:** internal cross-refs only (the design space is the authors' own).

### 3.1 III.C.1 — Dataset Composition
**Factor:** training-data source. **Variants:** Model I = real-target-only; Model II = simulation-target-only;
full = mixed. **Interpretation:** real-only is *limited* (fixates on strong-signal features), simulation-only is
*good*, mixed is *best*; caveat = ablated sets also have reduced volume. **Transition:** parallel opener to loss unit.

### 3.2 III.C.2 — Loss Mechanisms
**Factor:** a loss term (removal = set its weight to 0). **Variants:** Model III = perceptual/VGG weight 0 →
chaotic global reconstruction (term enforces global perception); Model IV = fidelity/L1 weight 0 → tracks full
model but redundant/over-detailed artifacts (term anchors fidelity). **Strategy:** removal-reveals-function.
**Transition:** parallel opener to network-component unit.

### 3.3 III.C.3 — Network Components *(climax of the triad)*
**Factor:** an architectural block. **Variants:** Model V = remove feature-alignment block (replace by trivial
addition) → approximates full model **but** loses weak detail (green box) / misses target reflection (yellow box);
Model VI = remove adversarial branch (weight 0) → serious distortion, info lost → **"plays a crucial role."**
**Strategy:** concede-then-rebuttal ("performs well … however …"); order so the **most damaging** removal is last
and stamped with the necessity superlative. **Transition:** closes triad → to field/external data.

---

## 4. III.D — Experiments on Geophysical / External Data (External Validation)

**Role:** closing subsection; move off the authors' own data onto a public benchmark acquired by others, under
untrained conditions. **Function:** answer "would it survive in the wild?" by running the **already-trained** model
on **open, independently collected** data spanning multiple devices/settings, **no retraining** — honestly,
including the one weak regime + its fix.

**Paragraph flow:** (1) motivate + introduce external dataset + site figure → (2) enumerate diversity axes
(device/setting, explicitly out-of-distribution) → (3) cross-axis-1 results + figure → (4) cross-axis-2 results +
figure → (5) honest limitation + remedy + verdict.

**Slots:** `[EXTERNAL DATASET + SITE FIGURE]` · `[DIVERSITY AXES]` · `[CROSS-AXIS-1 RESULTS + fig]` ·
`[CROSS-AXIS-2 RESULTS + fig]` · `[LIMITATION + REMEDY]`

**Fill-in:**
> "To further test **[METHOD]** on real data, we conduct tests on open-source **[DOMAIN]** data from
> **[INDEPENDENT SOURCE]**. The data are from the **[DATASET]** dataset [CIT]; the layout of the **[SITE]** is
> shown in Fig. **[N]** (a **[MEDIUM]** where **[TARGET TYPES]** are present). There are **[K]** brands of
> **[INSTRUMENT]** (**[VENDORS]**), with data across **[low]–[high] [UNIT]**. The results across different
> **[AXIS-1]** are shown in Fig. **[N(b)]**: **[METHOD]** has good generalization for different **[AXIS-1]**.
> The results across different **[AXIS-2]** are shown in Fig. **[N(d)]**: the raw data have clearly different
> styles, yet after **[METHOD]** the clutter is removed and targets preserved. For **[EXTREME SETTING]**, the
> **[signal]** decays rapidly, so some weak signals are lost; this can be solved by adjusting **[energy/gain]**.
> Overall, **[METHOD]** has good generalization across devices and settings."

**Figures:** annotated site-layout figure (credit source if modified) + multi-panel raw-vs-processed grouped by
axis; reference sub-panels individually. **Interpretation:** lead with the positive per-axis claim, then
concede-then-fix. **Citations:** the open dataset (does double duty — provenance + independence). **Tone:** 3–5
compact paragraphs, qualitative/visual (no metric tables here). **Transition:** to Section IV (new target types via fine-tuning).

---

## 5. ✅ Experiments Checklist

- [ ] III.A opens with a roadmap mapping every subsection, then states **every** reproducibility constant (hardware, batch, epochs, optimizer, LR schedule, resize, normalization, sample count, runtime).
- [ ] III.B co-cites figure+table per claim, reads tables per-metric, and **attributes the win to a mechanism**, not just numbers.
- [ ] III.B includes an explicit **fairness caveat** (shared dataset/epochs/noise).
- [ ] All three ablation units follow the shared micro-template (toggle → panel-pair+row → interpret → necessity).
- [ ] Panel-pairs cite synthetic `(aᵢ)` + real `(bᵢ)` together with the table row.
- [ ] The **"crucial role" superlative** appears only in the final ablation unit; honest caveats included.
- [ ] III.D uses **open/third-party** data with **no retraining**, claims per-axis generalization, and **concedes one weak regime + remedy**.
- [ ] Setup is past-tense; result claims are figure/table-anchored; external section is qualitative.


---

## 9. SECTION TEMPLATE — IV. GENERALIZATION / FINE-TUNING


> Domain-agnostic scaffold for a *capability-demonstration* top-level section, reverse-engineered from
> J. Ge *et al.*, “Wavelet-GAN…,” *IEEE TGRS*, vol. 62, Art. 5918214, 2024 (§IV, “Generalization
> Experiments Based on Fine-Tuning Datasets”).

---

## 1. Role & Function

**Role:** a dedicated top-level section whose **sole job is to prove ONE headline contribution** promised in
the Introduction but not covered by the main benchmark (here: *generalizes to new target types from tiny data*).
**Function:** isolate the claim → design a minimal experiment that can only succeed if the claim is true →
report the outcome **with its cost and honest boundaries**. Persuasive weight comes from a capability competitors
structurally lack, not from beating a metric.

## 2. Paragraph Flow

1. **Restate the gap/motivation** — re-open the Introduction's limitation (why existing methods fail on the new condition); name the specific scenario.
2. **Experiment design** — baseline regime (small/standard training set) + the new out-of-distribution target/condition + data/field layout.
3. **Minimal-data intervention** — the smallest possible augmentation (a single added sample); stress its parameters differ entirely from the test data.
4. **Before/after results** — un-augmented vs augmented model on the new condition, paired figures.
5. **Quantify cost** — epochs · wall-clock · #samples · hardware (prove it's cheap).
6. **Honest limitation** — where the un-tuned baseline visibly fails (residual distortion / un-removed artifact), bounding the claim.

## 3. Component Slots

`[MOTIVATION RESTATE]` · `[EXPERIMENT DESIGN]` · `[MINIMAL-DATA INTERVENTION + figure]` ·
`[BEFORE/AFTER RESULTS + figure]` · `[COST/EFFICIENCY METRICS]` · `[HONEST LIMITATION]`

## 4. Fill-in Template

> "A known drawback of **[method class]** is that performance degrades when the **[characteristics]** of the
> processed data differ from the training set [CIT]. Because real **[domain]** data are not always
> **[the canonical case]**, we organize a **[capability]** experiment to test **[METHOD]**'s ability to handle
> **[the new condition]**. At the start of training we use only **[N]** **[canonical-type]** samples; for the
> **[new target type]**, whose characteristics differ significantly, we use the data from Fig. **[X]** for
> analysis. We first apply the model trained entirely on **[canonical]** data to the **[new-type]** data: as
> shown in Fig. **[Y]**, although the **[new-type responses]** are extracted, their **[distortion]** is high.
> We then add a **single** **[new-type]** response to the original **[N]**-sample dataset for fine-tuning;
> the parameters of this added sample (**[size, frequency, medium]**) are completely different from the test
> data, to avoid any similarity (Fig. **[Z]**). Applying the rapidly tuned model, for both strong and weak
> cases the fine-tuned model effectively performs the task while preserving the genuine signal — adding one
> **[new-type]** response yields good generalization without large retraining datasets. Training of the new
> dataset is on the same **[hardware]**, and the transfer training of **[E]** epochs takes **[T]** s. When not
> fine-tuned, the method **[shows residual distortion / fails to remove artifact X]**, indicating that relying
> on a limited dataset of **[the new condition]** has limitations."

## 5. Figures · Interpretation · Citations · Tone

- **Figures:** layout figure (field geometry of new target) · intervention figure (single added sample +
  fine-tuning schematic: original dataset + single response → new dataset) · before/after figure (raw / before
  / after, paired panels).
- **Interpretation:** lead with the positive demonstration (the decisive advantage over methods needing large
  retraining), then **bound it** with the un-tuned failure mode in the same breath. Tie cheap cost figures back
  to the practical claim.
- **Citations:** sparse — cite the prior-work limitation once at motivation; cite external data/model source
  when reused; the experiment itself is uncited.
- **Tone:** ~5–7 short paragraphs (~0.75–1 page); confident but candid; present tense for behavior, past for
  what was run; numbers plain (N, E, T). **The honest-limitation sentence is mandatory and load-bearing.**

## 6. Transition Out → Section V

> "The fast transfer training and low data requirement mean we can perform timely **[task]** on data with
> atypical new **[responses]**. In the following section, we apply **[METHOD]** to **[downstream application]**
> and test whether it is effective for **[that application]**."

## 7. ✅ Checklist

- [ ] Opens by restating a specific Introduction gap, then names the exact new scenario.
- [ ] Shows the **un-tuned baseline first** (it partially fails), then the minimal intervention.
- [ ] Intervention is genuinely minimal (one sample) and its parameters differ from test data (stated explicitly).
- [ ] Before/after contrast is figure-anchored.
- [ ] Cost (epochs/time/#samples/hardware) reported to prove efficiency.
- [ ] **Honest limitation** sentence present.
- [ ] Closes by generalizing the capability + pivoting to the application section.


---

## 10. SECTION TEMPLATE — V. DOWNSTREAM APPLICATION


> Domain-agnostic scaffold for a *downstream-application* top-level section, reverse-engineered from
> J. Ge *et al.*, “Wavelet-GAN…,” *IEEE TGRS*, vol. 62, Art. 5918214, 2024 (§V, “Application of Wavelet-GAN
> in Inversion”).

---

## 1. Role & Function

**Role:** demonstrate the method's value as a **preprocessing step inside a larger pipeline** — show that better
cleaning yields a better end-to-end result on a separate, established task. **Function:** elevate the contribution
from "we remove the artifact well" to "removing it our way measurably improves what people actually do next."
Plug the method's output into a **fixed, third-party downstream model** and contrast against the field-standard
preprocessing baseline; pre-empts the "so what?" objection.

## 2. Paragraph Flow

1. **Why the downstream task suffers** — name the downstream task; explain how the artifact corrupts its results.
2. **Conventional preprocessing's flaw** — the field-standard step everyone uses + the specific information it destroys.
3. **Experiment setup** — feed *our output* vs *baseline-preprocessing output* into the **same pretrained downstream model**; give data source + acquisition details.
4. **Result contrast + figure** — baseline-preprocessed → wrong/degraded downstream result; our-preprocessed → result close to ground truth; **diagnose why** the baseline failed.
5. **Reliability conclusion** — better preprocessing of our kind improves downstream reliability.

## 3. Component Slots

`[DOWNSTREAM TASK + WHY ARTIFACT HURTS IT]` · `[CONVENTIONAL PREPROCESSING FLAW]` ·
`[EXPERIMENT SETUP + acquisition details]` · `[RESULT CONTRAST OURS vs BASELINE + figure]` ·
`[RELIABILITY CONCLUSION]`

## 4. Fill-in Template

> "The presence of **[ARTIFACT]** can seriously affect the results of **[DOWNSTREAM TASK]** [CIT].
> **[DOWNSTREAM-MODEL FAMILY]** methods are typically trained on **[idealized/simulated data]**, which does not
> account for **[ARTIFACT]**. In practice, the data are usually preprocessed by **[CONVENTIONAL METHOD]** to
> remove **[ARTIFACT]** before being fed into **[DOWNSTREAM MODEL]**. However, this causes **[SIGNAL OF
> INTEREST]** to lose **[KEY INFORMATION]**, resulting in **[INACCURATE DOWNSTREAM RESULT]** [CIT]. In this
> section, we test the effectiveness of **[OUR METHOD]** within **[DOWNSTREAM TASK]**. We collected real
> **[DATA TYPE]** from a known **[TARGET]** and processed it with **[OUR METHOD]** and **[BASELINE]**,
> respectively, then input each into the pretrained **[DOWNSTREAM MODEL]** [CIT]. The data were acquired with
> **[INSTRUMENT]**, **[KEY PARAMETERS]**; the target was **[DESCRIPTION/GEOMETRY]**, and **[MEDIUM PROPERTY]**
> was **[VALUE]**. As shown in Fig. **[N(panel)]**, with **[BASELINE]**-processed input the downstream model
> produced a result far from the truth, because residual **[ARTIFACT]** was erroneously interpreted as
> **[SIGNAL OF INTEREST]**. In contrast, panels **[N(panels)]** show that **[OUR METHOD]** removes **[ARTIFACT]**
> and the resulting **[DOWNSTREAM OUTPUT]** is much closer to the true **[GROUND TRUTH]**. Therefore,
> **[OUR METHOD]** can be used for **[DOWNSTREAM-TASK]** preprocessing to improve the reliability of
> **[DOWNSTREAM RESULT]**."

## 5. Figures · Interpretation · Citations · Tone

- **Figure:** one multi-panel application figure; standard layout — (a) acquisition/survey schematic; (b) ground
  truth; (c) baseline-preprocessed input; (d) downstream result from baseline; (e) our-preprocessed input;
  (f) downstream result from ours. Cite panels inline in flow order; pair them ("compare (d) and (f) against (b)").
- **Interpretation:** hold the downstream model **fixed**, vary only the preprocessing → any difference is
  attributable to the cleaning method. Read each result **against ground truth**. Always supply a **mechanism**
  for the baseline's failure (e.g., "residual artifact mistaken for true signal"), not just a verdict.
- **Citations:** downstream task importance + artifact sensitivity [refs]; conventional-preprocessing weakness
  [ref]; the third-party downstream model by name with its primary ref at first mention. Reference-light overall.
- **Tone:** 4–6 compact paragraphs / one column; applied, evidence-first; first-person plural for the experiment;
  hedged on causal diagnosis ("we suspect/believe") but firm on the observed outcome + recommendation.

## 6. Transition Out → Conclusion

End on the reliability claim phrased as a forward-looking recommendation ("…can be used for **[task]**
preprocessing to improve reliability"), which the Conclusion restates as a headline contribution.

## 7. ✅ Checklist

- [ ] Names a concrete downstream task and explains the artifact's specific failure mode there.
- [ ] Identifies the conventional preprocessing baseline and the information it destroys.
- [ ] Holds the downstream model **fixed**; varies **only** the preprocessing.
- [ ] Reads all results against **ground truth**; gives a **mechanism** for the baseline failure.
- [ ] Multi-panel figure cited panel-by-panel in flow order.
- [ ] Closes with a reliability recommendation that the Conclusion can echo.


---

## 11. SECTION TEMPLATE — VI. CONCLUSION


> Domain-agnostic scaffold for the Conclusion, reverse-engineered from J. Ge *et al.*, “Wavelet-GAN…,”
> *IEEE TGRS*, vol. 62, Art. 5918214, 2024 (§VI).

---

## 1. Role & Function

**Role:** closing recap / contribution-mirror. **Function:** concisely restate what was proposed and demonstrated,
consolidating the Introduction's promises as **now-substantiated** results — **no new** method, data, or experiment.
A reader who reads only this section should grasp the full takeaway. Forward-pointing only at the very end (optional outlook).

## 2. Paragraph Flow

1. **Method recap** — one line naming the method, its task, and its paradigm combination + core mechanism.
2. **What-was-done summary** — recap dataset construction → comparison/evaluation → generalization test → downstream
   application, **mirroring the contributions in original order**, each phrased as accomplished.
3. **Headline advantages** — the substantiated selling points stated as established facts (robustness/independence
   from equipment & hyperparameters, small-data + fast transfer, new-case handling via minimal input).
4. **Future work / outlook** *(optional)* — broader applicability or the remaining problem now made tractable.

## 3. Component Slots

`[METHOD RECAP]` · `[WHAT-WAS-DONE SUMMARY mirroring contributions]` · `[HEADLINE ADVANTAGES]` ·
`[FUTURE WORK / OUTLOOK (optional)]`

## 4. Fill-in Template

> "A new **[TASK]** method based on **[PARADIGM]** is proposed. The **[METHOD]** combines **[COMPONENT A]**,
> **[COMPONENT B]**, and **[COMPONENT C]**, and can effectively **[SOLVE PROBLEM]** by **[MECHANISM]**. To train
> the network, we construct **[DATASET]** based on **[REAL/SOURCE INPUT]**; a **[augmentation]** method using
> **[techniques]** is designed to achieve **[GOAL]** with **[constraint, e.g. small datasets]**. We compare this
> method with other **[BASELINE-CLASS]** methods; the results show it can effectively **[PERFORM TASK]** and
> demonstrate superiority in **[KEY QUALITY]**. Generalization experiments are also carried out to test its
> ability on **[NEW/UNSEEN CASES]** completely different from training. Finally, we apply **[METHOD]** to
> **[DOWNSTREAM TASK]** and test whether it is effective for **[DOWNSTREAM GOAL]**. The research shows that
> **[METHOD]** can effectively **[CORE OUTCOME]**; its effectiveness is not affected by **[confounding factor,
> e.g. equipment/hyperparameters]**. The small-data demand and fast transfer enable **[PRACTICAL BENEFIT]**
> rather than **[costly alternative]**. The problem of **[NEW-CASE HANDLING]** can be solved by **[MINIMAL
> ADDITIONAL INPUT]**."

## 5. Citations · Tone · Transition

- **Citations:** typically **none** — no new references; reuse method names already cited without re-citing.
- **Tone:** short (~1–4 compact paragraphs); summary register; present and present-perfect ("is proposed",
  "the results show", "can effectively"); **no new claims, no new numbers/metrics, no equations**.
- **Transition:** none — ends the paper body; leads directly into References (and author biographies).

## 6. ✅ Checklist

- [ ] One-line method recap names paradigm + components + mechanism.
- [ ] Summary **mirrors the contributions** in the same order as the Introduction's contribution list.
- [ ] Advantages stated as **established facts**, not aspirations.
- [ ] **No new** method, data, experiment, number, or equation introduced.
- [ ] Citation-free; present / present-perfect tense throughout.
- [ ] Optional outlook sentence is genuinely forward-looking, not a new result.


---

### 📎 End of consolidated AI-Paper writing skill — convert to .docx on request (LibreOffice available).
