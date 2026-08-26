# LaTeX authoring rules for teaching-notes fragments

These rules produce a tight, black-and-white, information-dense teaching document.
They apply whether you write the whole `main.tex` yourself or dispatch one subagent
per section (Mode A). When dispatching agents, hand them THIS file plus their source
line-range, and tell them to write a `\input`-able fragment (no preamble, no
`\begin{document}`) to a named file.

## The preamble already provides (never redefine)
- Packages: amsmath, amssymb, graphicx, booktabs, array, tabularx, longtable,
  enumitem, xcolor, tcolorbox, tikz, caption, float, hyperref, cleveref.
- `\figpath` → figures directory. Use `\includegraphics[...]{\figpath/NAME.png}`.
- Bounded, unbreakable teaching boxes (each wraps body text):
  - `keynote`   — KEY POINT / important takeaway or "in one line".
  - `notebox`   — a derivation NOTE / side aid ("arc ≈ bθ", small-angle rule, etc.).
  - `resultbox` — a final RESULT & MEANING (heavier frame).
  - `defbox`    — a boxed DEFINITION.
  - `oneline`   — a one-line "in a nutshell" strip (no title).

## Content fidelity
- Retain ALL source text, equations, tables, lists. Nothing is dropped. You may fix
  obvious OCR artefacts (`\*\*`, stray `\ `, broken `\[\boxed{...}]`, doubled words),
  drop bare URL-citation link dumps, and drop emoji (or replace with a word).
- Reorganise into a logical teaching flow (topic → section → subsection → explanation
  → figure/table/equation → key takeaway). Do NOT convert page-by-page.

## Hard formatting rules
- **No raw Unicode.** Convert every Greek/symbol to LaTeX math: θ→`$\theta$`, α→`$\alpha$`,
  δ→`$\delta$`, μ→`$\mu$`, ρ→`$\rho$`, φ→`$\phi$`, π→`$\pi$`, Δ→`$\Delta$`, ×→`$\times$`,
  →→`$\rightarrow$`, ⇒→`$\Rightarrow$`, ≈→`$\approx$`, ≤→`$\le$`, ²→`$^2$`, °→`$^\circ$`,
  μGal→`$\mu$Gal`, Σ→`$\sum$`, ∝→`$\propto$`. Never leave emoji in output.
- Reuse the source's display equations VERBATIM as LaTeX inside `\[ ... \]` or `equation`
  (add `\tag{N}` if the source numbers it). Do not paraphrase equations.
- **Lists:** any point-wise / numbered content becomes `itemize`/`enumerate` — never a
  run-on paragraph. Bold the defined term on first use; `\emph{}` for emphasis.
- **Emphasis:** `\textbf{}` for key terms, definitions and warnings; `\emph{}` for stress.

## Tables — tight, wrapping, no white gaps
- Text-heavy comparison tables: `tabularx` at `\linewidth`, with **raggedright wrapping X
  columns** so cells wrap and fill the width evenly:
  `\begin{tabularx}{\linewidth}{@{}>{\bfseries\raggedright\arraybackslash}p{2.5cm} >{\raggedright\arraybackslash}X >{\raggedright\arraybackslash}X@{}}`
  Use `\footnotesize`, `booktabs` rules (`\toprule/\midrule/\bottomrule`), a `\caption{}`.
- A large table must NOT float onto its own page (it gets vertically centred, leaving big
  top/bottom white bands). Put it **in-flow** with `\begin{table}[H]`.
- Wide **numeric** tables: `longtable` at `\footnotesize`, tight column glue
  (`{@{}c@{\hspace{6pt}}*{N}{c}@{}}`), repeating header via `\endfirsthead/\endhead` and a
  `\bottomrule\endfoot`. Reset with `\normalsize` after `\end{longtable}`.
- Split genuinely long tables across pages with `longtable` (that is expected and fine).

## Figures — near the text, no float-page gaps
- Place a figure right after the text that discusses it. For anything sizeable, use
  `[H]` (in-flow) rather than `[htbp]` — a floated figure often drifts onto a sparse page
  with large empty bands above/below. Example:
  `\begin{figure}[H]\centering\includegraphics[width=9cm]{\figpath/NAME.png}\caption{...}\label{fig:key}\end{figure}`
- Give every figure a `\caption{}` (start captions `Figure N.` when the source numbers them).
- Pick a width that fits inline (7–12 cm typical; full-width plots up to 15 cm). If two
  figures + their captions + text can't share a page, that's fine — `[H]` still avoids the
  sparse float page.

## Boxes — when to use which
- "Note:", small geometric/algebraic aids, "where each factor comes from" → `notebox`.
- Final results / "Result & meaning" / the key sensitivity formula → `resultbox`.
- "In one line", "one-line memory aid", "in simple terms" → `keynote` (or `oneline`).
- Boxed definitions / boxed identities → `defbox`.

## Style contract (the "regular tex-to-pdf" look the user wants)
- **Black and white** — no coloured headings or coloured box fills. (Content figures may
  keep their own colours; the document *typography* is B&W.)
- **Tight** — no `\vspace` padding, no decorative blank lines, compact section spacing.
- **Page numbers** on every page (the preamble's fancyhdr footer handles this).
