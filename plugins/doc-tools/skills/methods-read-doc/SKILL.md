---
name: methods-read-doc
description: Use when asked to produce a detailed, beginner-accessible "read" or explainer version of a technical or mathematical section (methods, equations, transforms, derivations) — with per-symbol glossaries, boxed key-term definitions, plain-language explanations, schematics, and matching PDF/DOCX output. Triggers include "explain every symbol", "read doc", "dumb down the math", "term definitions in a box", "make a detailed methods explainer".
---

# Methods Read-Doc

## Overview
A **methods read-doc** is a self-contained, beginner-accessible companion to a technical/math section. It keeps every original equation verbatim and wraps it in layered explanation, so a non-specialist can follow the whole derivation while an expert still sees the exact math. Output is one Markdown file plus a matching PDF and DOCX. Filenames use the convention `[Methods_read<NN>]_<YYYYMMDD>_<topic>.{md,pdf,docx}`.

**Core principle:** preserve the math exactly, explain everything around it in layers, and render key-term definitions as visually distinct boxes.

## When to use
- The user wants a section's math "explained", "dumbed down but detailed", every symbol/term glossed, or a "read"/explainer version.
- The user asks for term definitions in boxes, schematics for concepts, or a beginner walkthrough of equations.
- **Not for:** the terse manuscript itself (that is the source), one-line answers, or non-math prose.

## Per-equation anatomy (the required layers)
For EVERY equation, in this order:
1. The equation verbatim in `$$…$$` with its original `\tag{n}` — never renumber or alter it.
2. `**Symbols in (N):**` — a **bulleted list** defining EVERY symbol, operator, subscript, superscript, and constant in that equation, one bullet each, plain language. This includes **notation constructs, not just letters**: function signatures ($g:A\to B$ means "$g$ takes an input in the set $A$ and returns an output in the set $B$", where the colon introduces the domain and codomain and the arrow $\to$ reads "into"), set symbols ($\mathbb{R}$ reals, $\mathbb{R}^2$ the plane, $\mathbb{R}_+$ positive reals, $\mathbb{R}_{\ge0}$ non-negative reals, $\mathbb{S}^1$ the circle of directions, $\mathbb{Z}$ integers, $\mathbb{C}$ complex numbers), and relations ($\in$ "is a member of", $\mapsto$ "maps to", $\forall$ "for all", $\le,\ge,\sim,\approx$). Every glyph and construct is explained the **first time** it appears.
3. `**Discussion.**` — a short paragraph on what the equation says and why it matters.
4. `**In simple terms:**` — an expanded plain-language walkthrough (≈8–12 sentences) that stands alone, folding in the glossary and discussion detail.
5. `**Physical significance (<domain>):**` — ties it to the real problem (e.g. GPR hyperbolic diffraction).

## Per-subsection anatomy
- `##### N. Title` subsections.
- End each subsection with a **Key terms box**: a Markdown blockquote led by `> **Key terms.**`, defining the subsection's *concepts* (not per-symbol) as short paragraphs with inline math and a "why it matters" clause. Each term appears in `***bold italic***` at first mention. The blockquote renders as a **rectangular bordered box** (see build.md).
- Add a **schematic** for hard-to-picture concepts: author TikZ, compile to PNG+PDF, embed with a `**Fig. N.**` caption. Keep figures in a `figures_*` subfolder next to the doc.
- **Ray / physics diagrams (do this whenever a concept has a physical origin).** For domain concepts that come from a real measurement (in GPR: the acquisition geometry, why the signature is a hyperbola, the polarity/phase of a reflection, wave paths, impedance contrasts), add a **ray diagram** alongside the abstract/frequency-domain schematic. Draw it in TikZ: source/receiver positions, rays to and from the buried target, the resulting traveltime curve, and the reflection sign that sets polarity. A ray diagram grounds an equation in the physics a reader already pictures, so pair it with the math (e.g. a single-sided-wedge equation gets both a frequency-plane wedge schematic **and** a ray diagram showing the polarity flip it recovers). Same build path (TikZ → PDF → PNG at ~200 dpi), same `**Fig. N.**` caption convention, same `figs_<shortname>/` folder.
- **Figure captions: full, self-contained, 3 pt smaller than body, hanging-indent, via ONE command.** Every embedded figure gets a `**Fig. N.**` caption paragraph that *fully explains the figure on its own* — walk through each panel `(a)/(b)/…`, name every symbol shown, and state the takeaway in plain language. Captions may be **long** (several sentences, whatever it takes to simplify); do not truncate to a one-liner. **Style: 3 pt smaller than the body font** (a 10 pt `article` ⇒ **7 pt**) with a **hanging indent** (label + first line flush left, wrapped lines indented). **Define the style once in the preamble and call it for every caption** (the "best" pattern — not the same inline code repeated 11×):
  ```latex
  % preamble, ONCE (this single \fontsize is the one knob for size + leading):
  \newcommand{\figcaption}[1]{%
    {\fontsize{7}{8.4}\selectfont\hangindent=2em\hangafter=1\noindent#1\par}}
  % each figure caption:
  \figcaption{\textbf{Fig. N.} … full explanation …}
  ```
  In the TeX-patch step: **(1)** inject the `\newcommand{\figcaption}` right before `\begin{document}`; **(2)** wrap each `\textbf{Fig. …}` caption paragraph with it, `t = re.sub(r'(\\textbf\{Fig\.\s.*?)\n\n', r'\\figcaption{\1}\n\n', t, flags=re.S)` (runs after the `\includegraphics` fix). The `\figcaption` macro adds the `\par`, so the captured group must not include one. Change `\fontsize{7}{8.4}` in the single definition to restyle every caption at once. (`build_read_doc.py --caption-size N` exposes this knob.)

## Document skeleton
Title + `**Date:** YYYY-MM-DD` header → intro paragraph (paper voice, no meta about the writing process) → detailed **Notation** paragraph (define every recurring symbol for a beginner, and state the reading conventions once: what a function signature $g:A\to B$ means, and the set/relation symbols $\mathbb{R},\mathbb{R}^2,\mathbb{R}_+,\mathbb{R}_{\ge0},\mathbb{S}^1,\mathbb{Z},\mathbb{C},\in,\mapsto,\to,\forall$) → the numbered subsections → `### Equation index` → `### References` (author–year, "et al.").

## Writing style (MANDATORY — apply to every added paragraph)
**REQUIRED:** every sentence you write for the read-doc follows `references/AI_humanization_writing_instructions.md` (bundled, source of truth) in **formal register**. The concrete rules:
- **No em dashes** — use commas or rephrase. **No semicolons in prose** — use periods or "and"/"but".
- **Integrate parentheticals** into the sentence. Use **colons sparingly** (do not lead a list with "Key points:").
- **Vary sentence starts and length.** Start most sentences with "The", also "Generally", "However", "So", "In this case", "Throughout". Connect clauses with "which" / "where" / "that is why".
- **Replace hedging** ("it is worth noting", "however it should be said") with direct statements.
- **Prefer simple words** ("use" not "utilize", "find" not "ascertain"). **US English** throughout.
- **Formal register: no contractions, no sentence fragments.** (Do not adopt the file's casual-only rules.)
- **Citations:** author–year in text, e.g. "(Candès et al., 2006)" or "Following Ge et al. (2024), …".
- All math in `$…$`/`$$…$$` with `\tag{}` **inside** the block. Never `\(…\)`, `\[…\]`, or `\begin{equation}`.
- Keep any project framing conventions (e.g. name a target generally, not by a specific label) if the source project has one.

When splitting work across subagents, pass this rule set to each one so every part is written in the same voice.

## Build workflow — strict order: MD → TEX → PDF → DOCX
Always produce the artifacts in this exact sequence. Do not skip the `.tex` step; the PDF is compiled from the generated `.tex`, not straight from Markdown.

1. **Scale with subagents:** for a large section, split by part (one researcher subagent per part) with identical layer rules, then the lead stitches `preamble + parts + equation-index/references`. Verify tag count and no duplicate tags after stitching.
2. **① Markdown (`.md`) first** — write the whole doc to local scratch (e.g. `/DATA1/mkl/...`), verify it (all equations, glossaries, boxes, tags), then mirror the `.md` to the output/NAS folder.
3. **② TeX (`.tex`)** — `pandoc DOC.md -o DOC.tex --standalone --toc`, then inject the preamble (mdframed boxes, `\setstretch{1.15}`, `newunicodechar`, `graphicspath`, strip `alt=`) per **build.md**. The `.tex` is a real intermediate: keep it.
4. **③ PDF (`.pdf`)** — `pdflatex DOC.tex` twice (2nd pass for the TOC), from the patched `.tex` in step ②.
5. **④ DOCX (`.docx`)** — `pandoc DOC.md -o DOC.docx --reference-doc=refbox15.docx --mathml --toc` (build `refbox15.docx` once with `make_refbox.py`).
6. Mirror `.md/.tex/.pdf/.docx` to the output/NAS folder. **Optional red-mark** variant (word-level diff, changes in red) — see build.md.

**REQUIRED READ:** `build.md` has the copy-paste commands for steps ②–④; `make_refbox.py` builds the bordered, 1.15-spaced DOCX reference.

## Quick reference
| Element | Markup |
|---|---|
| Equation | `$$ … \tag{n} $$` |
| Symbol glossary | `**Symbols in (n):**` + `- $sym$ — definition.` |
| Concept box | `> **Key terms.**` blockquote, terms in `***bold italic***` |
| Discussion | `**Discussion.**` paragraph |
| Simple explanation | `**In simple terms:**` (8–12 sentences) |
| Figure | TikZ → PNG, `![alt](figures_x/name.png)` + `**Fig. n.**` caption |

## Common mistakes
- Renumbering or paraphrasing an equation. Keep it byte-for-byte with its tag.
- Leaving a symbol undefined. Every glyph in every equation gets a bullet.
- Rendering key-term boxes as plain indents. They must be rectangular bordered boxes (build.md).
- Em dashes / semicolons / contractions slipping into new prose.
- Forgetting the date in the header or the date-time prefix in the filename.
