# 📝 Reusable Template — Paper **INTRODUCTION** Section

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
