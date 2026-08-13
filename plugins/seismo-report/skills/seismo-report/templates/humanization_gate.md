# Humanization gate (seismo-report)

Apply to every sentence, including captions, the executive summary, and table notes. These rules come from `reference/AI_humanization_writing_instructions.md`.

## Punctuation
- No em dashes. Rephrase or use a period.
- Avoid semicolons; use a period or "and"/"but".
- No mid-sentence ellipses. Few commas.
- Colons only to introduce an equation with a lead-in like "described as:" or "formulated as below:".

## Language
- US English throughout.
- Default document format when unspecified: Times New Roman, 12 pt, 1.15 line spacing.
- Author every chapter and section as an ATX Markdown heading: `#` for a section, `##` for a sub-section, `###` for a sub-sub-section, `####` for a paragraph head, `#####` for a sub-paragraph head. Do not use bold-text pseudo-headings (never `**1. Introduction**`). The export applies the styled hierarchy from `formatting_spec.md` and numbers sections automatically.
- First line of every paragraph is indented, never inside a table.
- Most sentences open with "The", varied with "Generally", "However", "So", "In this case", "Throughout".
- Join clauses with "which", "where", "that's why".
- No `1) 2) 3)` numbered lists inside section prose; carry the enumeration in paragraph form.
- Replace hedging ("it's worth noting") with direct statements. Avoid stock transitions ("furthermore", "in conclusion") unless truly needed.
- Vary repeated terms. Prefer simple words ("use" over "utilize").
- Equations in LaTeX `$...$`. Refer as "Equation (11)" or "Equations (11-12)". Refer to tables as "Table 1".
- In-text references in real author-date form, e.g. "(Kumar et al., 2023)", "(Terrasse et al., 2015, 2017; Kumar et al., 2023)", "Following Ge et al. (2024), ...".

## Seismology-specific
- Define every abbreviation and symbol on first use, e.g. "peak ground acceleration (PGA)", "the shear-wave velocity $V_s$".
- Interpret, do not describe. Each observation is followed by its physical reasoning and its significance for the source, path, or site.
- State assumptions and give the physical meaning of each equation term the first time it appears.

## Example
Before: "The spectra—though preliminary—show a peak; however, it's worth noting the noise."
After: "The preliminary spectra show a clear peak near 2 Hz, which the ambient noise does not explain."
