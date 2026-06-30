# 📘 MASTER PAPER TEMPLATE — "Ge-Style" Deep-Learning Methods Paper

> A single, journal-ready master scaffold for writing a complete deep-learning / GPR / geophysics /
> computer-vision / remote-sensing methods paper in the scientific style of J. Ge *et al.*, “Wavelet-GAN:
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
