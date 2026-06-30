# 🤖 AI-Paper — Reusable Skill Specification

> A permanent, self-contained specification for an AI writing skill that drafts complete or partial
> **deep-learning / GPR / geophysics / computer-vision / remote-sensing** research papers in the
> scientific style of J. Ge *et al.*, “Wavelet-GAN: A GPR Noise and Clutter Removal Method Based on Small
> Real Datasets,” *IEEE TGRS*, vol. 62, Art. 5918214, 2024.
>
> **Runtime skill:** `~/.claude/skills/ai-paper/SKILL.md` (invocable). **This file** is the standalone
> human/portable spec. Both operationalize the templates in `Q_TEMPLATE_for_Claude/Paper/`.

---

## 1. Purpose & Scope

Write, in Ge-style, any of: the **whole paper**, an **individual section**, or the **remaining sections of a
partially-finished manuscript** — while keeping consistent structure, voice, and journal formatting.

**Triggers (when to use):** drafting/completing a methods paper or any section (abstract, introduction,
methodology, experiments, ablation, generalization, application, conclusion); a manuscript skeleton that
needs its pending sections developed; converting research results into IEEE-ready prose.

**Core principle:** the move-structure and global rules are fixed; only domain content is filled in.
**Never fabricate results** — unfinished work gets an explicit "Yet to be developed" placeholder.

---

## 2. Template Library (authoritative inputs)

```
Q_TEMPLATE_for_Claude/Paper/
├── MASTER_PAPER_template.md            # global rules + full skeleton + unfinished-section policy
├── AI-Paper.md                         # THIS spec
└── sections/
    ├── INTRODUCTION_template.md
    ├── METHODOLOGY_template.md
    ├── EXPERIMENTS_template.md
    ├── GENERALIZATION_FINETUNING_template.md
    ├── APPLICATION_DOWNSTREAM_template.md
    └── CONCLUSION_template.md
```

Each section file defines: role · function · paragraph flow · component slots · domain-agnostic fill-in
sentences · citation/figure/equation conventions · length/tone · transition · checklist.

---

## 3. Operating Workflow

1. **Read `MASTER_PAPER_template.md`** (global rules + assembled skeleton).
2. **Scope the request** — whole paper vs sections; inventory what is *done* vs *pending*.
3. **Emit the full skeleton first** — every heading I–VI + subsections with correct IEEE numbering, regardless
   of completion state.
4. **Per section, read its `sections/*.md`** and fill slots with the project's content.
5. **Apply every global rule** (§4).
6. **Insert the placeholder** for pending work (§5); never invent numbers/figures/tables.
7. **Verify** against the Master Checklist + each section checklist.

---

## 4. Global Writing Rules (always enforced)

| Rule | Requirement |
|------|-------------|
| **Language** | US English only (normalize, behavior, modeling, analyze, fiber, center). Serial comma on. |
| **Voice/tone** | Formal, evidence-led; first-person plural for choices; passive for mechanisms; bounded claims, minimal hedging. |
| **Tense** | Present = design/facts; past = what was done; consistent within a paragraph; present-perfect in Conclusion. |
| **Abbreviations** | `full name (ACRONYM)` on first use; acronym thereafter; one term per concept everywhere. |
| **Equations** | `$…$` inline, `$$…$$` display with `\tag{n}` **inside**; every symbol in math delimiters + glossed right after. NEVER `\(…\)`, `\[…\]`, `\begin{equation}`. |
| **Figures/Tables** | Numbered in order (Tables = Roman numerals); cited **before** appearance; self-contained captions; proposed method last/rightmost; best metric **bolded**; state ↑/↓ once. |
| **Citations** | IEEE numeric `[n]`; cite origin of every borrowed method/block/loss/metric/dataset; prior-art dense; **thesis/contributions/conclusion citation-free**. |
| **Units/numbers** | SI with a space ("256 × 256 pixels", "100 MHz", "2813 s"); en-dash ranges ("200–900 MHz"); decimal point; consistent thousands style. |
| **Headings** | IEEE: `I.` (Roman) → `A.` (letter) → `1)` (number); preserve labels in markdown `##`/`###`/`####`. |
| **Reproducibility** | Setup states hardware, optimizer, all hyperparameters, data scale, normalization, runtime. |

**Structural invariants:** Gap↔Contribution 1:1 (Intro M3 ↔ M5 ↔ Sections IV/V) · funnel-shaped Introduction ·
contribution-mirroring Conclusion · clean artifact hand-offs between (sub)sections · every results claim
qualitative→quantitative→mechanism · concede-then-fix in external-validation/capability sections.

---

## 5. Unfinished-Section Policy ("Yet to be developed")

When the underlying work is incomplete:

1. **Preserve the full skeleton** — emit all headings with correct numbering.
2. **Mark incomplete content** with a fenced placeholder — never fabricated results:
   ```
   > 🚧 **Yet to be developed.**
   > Planned content: [one-line description].
   > Depends on: [data / experiment / result still pending].
   ```
3. **Fully develop everything writable now** — Introduction, Methodology design, related work, loss/metric
   definitions, completed experiments — in full Ge-style.
4. **Never invent** numbers, figures, or table values. A results subsection without data → placeholder; figure
   callouts → `Fig. [N — pending]`.
5. **Keep gap↔contribution auditable** — retain a planned contribution in the Introduction even if its
   demonstrating section is pending (flag it as planned).

---

## 6. Full Paper Skeleton (emit this shape)

```
TITLE · Authors · Affiliations · ABSTRACT · INDEX TERMS
I.   INTRODUCTION                              (field→problem→taxonomy→prior art→gap→thesis→contributions→roadmap)
II.  METHODOLOGY  → A Dataset · B Transform/Theory · C Model(1 Overall,2 Generator,3 Discriminator) · D Loss & Eval
III. EXPERIMENTS  → A Training&Testing · B Results&Comparison · C Ablation(1,2,3) · D External/Field Data
IV.  GENERALIZATION EXPERIMENTS …             (capability demonstration of one contribution)
V.   APPLICATION OF [METHOD] IN [DOWNSTREAM]  (value as preprocessing in a larger pipeline)
VI.  CONCLUSION                               (mirror substantiated contributions; no new claims)
REFERENCES · AUTHOR BIOGRAPHIES (optional)
```

---

## 7. Quality Gate (before declaring done)

- [ ] Full skeleton present with IEEE numbering, including pending sections.
- [ ] US English; consistent terminology; acronyms defined once.
- [ ] All equations `$…$`/`$$…$$` + `\tag{}`; symbols glossed; no bare LaTeX delimiters.
- [ ] Figures/tables numbered, pre-referenced, captioned, best value bolded.
- [ ] Citations IEEE-numeric; thesis/contributions/conclusion citation-free.
- [ ] Gap↔Contribution 1:1 holds.
- [ ] Results claims = qualitative→quantitative→mechanism; fairness caveat in comparisons.
- [ ] External-validation/capability sections concede one honest limitation + remedy.
- [ ] **No fabricated results**; pending work uses the placeholder.
- [ ] Abstract standalone (≤250 words, no citations/equations); 4–8 alphabetical index terms.

---

## 8. Testing Note (for skill maintainers)

Per the superpowers TDD-for-skills discipline, validate before relying on this skill: run **retrieval** tests
(can an agent find the right section template?) and **application** tests (does the produced section obey the
global rules and the section checklist?) against a no-guidance control. Add any new rationalization/failure
observed (e.g., fabricated tables, British spellings, bare `\[ \]`) as an explicit counter in §4–§5.

---

### 📎 Provenance
Templates and this spec were compiled by a team-lead AI agent from 9 (Introduction) + 16
(Methodology/Experiments/IV/V/VI) parallel paragraph-analyst agents over the Wavelet-GAN exemplar.
Domain-agnostic by construction; reusable as a permanent paper-writing system for future research projects.
