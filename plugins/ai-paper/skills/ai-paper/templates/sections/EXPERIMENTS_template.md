# 🧪 Reusable Template — **EXPERIMENTS** Section (III)

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
