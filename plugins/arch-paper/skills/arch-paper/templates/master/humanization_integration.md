_date: 2026-07-09_

# Humanization Integration — enforceable rules for every generated sentence

&nbsp;&nbsp;&nbsp;&nbsp;This file operationalizes the humanization rules so the skill applies them to every sentence it writes. The rules make generated prose read as if a careful human wrote it, not a model. Treat the checklist below as a hard gate. The skill runs each drafted paragraph past it before the paragraph is accepted. The default document format is Times New Roman, 12 pt, 1.5 line spacing.

---

## Enforceable checklist (apply to every sentence)

**Language and spelling.**
- [ ] US English throughout ("analyze", "modeling", "meter" only where a unit convention allows, otherwise US spelling).

**Punctuation.**
- [ ] No em dashes anywhere. Rephrase into two sentences or use a comma. If a dash feels needed, the sentence needs splitting.
- [ ] Avoid semicolons. Use a period, or join with "and" or "but".
- [ ] No mid-sentence ellipses.
- [ ] Limit parentheticals. Keep at most one short parenthetical per paragraph, and prefer folding the aside into the sentence.
- [ ] Use colons sparingly. Reserve them for a genuine list lead-in or a ratio, not for dramatic effect.

**Headings.**
- [ ] Top-level headings read "1. Introduction" and are bold.
- [ ] Subsection labels read "2.1" and are italics.

**Paragraphs.**
- [ ] The first line of every paragraph is indented, except inside tables.
- [ ] No 1) 2) 3) numbered lists inside section prose. Carry enumerated content in paragraph form using "The first", "A second", "and finally".

**Sentence openers.**
- [ ] Most sentences begin with one of "The", "Generally", "However", "So", "In this case", or "Throughout". Vary across the paragraph so the pattern is not mechanical.
- [ ] Use the connectors "which", "where", and "that's why" to join clauses instead of stacking short choppy sentences.

**Directness.**
- [ ] Replace hedging filler ("it's worth noting", "it should be mentioned", "arguably") with the direct statement.
- [ ] Replace stock transitions ("furthermore", "moreover", "in conclusion", "additionally") with a direct continuation or a concrete connector.

**Variety.**
- [ ] Vary repeated terms. Do not open three consecutive sentences the same way, and swap a repeated noun for a precise synonym where the meaning holds (radargram, profile, section for the vertical image; anomaly, reflection, feature where each is accurate).

**Math and citations.**
- [ ] Equations in `$...$` inline and `$$...$$` displayed, never bare LaTeX delimiters.
- [ ] In-text references follow `(Kumar et al., 2023)`, `(Terrasse et al., 2015, 2017; Kumar et al., 2023)`, and `Following Ge et al. (2024)`.

---

## Rule rationale in one line each

- No em dashes, because they are a strong model tell and a period or comma reads more naturally.
- Avoid semicolons, because human technical prose in this genre rarely uses them and a period is cleaner.
- No mid-sentence ellipses, because they read as trailing off rather than as finished thought.
- Limit parentheticals, because stacked asides fragment the argument.
- Indent paragraph first lines, because that is the manuscript convention the source papers follow.
- Vary openers and terms, because uniform sentence shape is the clearest signature of machine text.
- No inline numbered lists, because section prose in this genre carries enumeration inside sentences.

---

## Three before / after rewrite examples

**Example 1 — em dash, semicolon, and stock transition.**

Before:
> The 400 MHz antenna gave the best resolution — furthermore, it penetrated to about 3 m; this was sufficient for the chambers.

After:
> &nbsp;&nbsp;&nbsp;&nbsp;The 400 MHz antenna gave the best resolution and penetrated to about 3 m. This depth was sufficient to reach the chambers.

Why: the em dash and semicolon are gone, "furthermore" is dropped, the clauses are split into two clean sentences, and the first line is indented.

**Example 2 — hedging filler, parenthetical overload, and mechanical opener.**

Before:
> It's worth noting that the anomaly (which was roughly 4 by 3 m, and quite bright) may (possibly) be a hut floor.

After:
> &nbsp;&nbsp;&nbsp;&nbsp;The bright anomaly, roughly 4 by 3 m, may correspond to a hut floor.

Why: the hedging filler "it's worth noting" is cut, the nested parentheticals collapse into one clean modifier, and "may correspond to" is the correct Tier 4 hedge stated directly.

**Example 3 — inline numbered list and repeated opener.**

Before:
> The processing chain had three steps: 1) time-zero correction, 2) background removal, 3) migration. The processing then produced slices. The processing used a nominal velocity.

After:
> &nbsp;&nbsp;&nbsp;&nbsp;The processing chain ran in three stages. The first applied a time-zero correction, the second removed background, and the third migrated the data with Kirchhoff migration. So the migrated volume was then sliced at a nominal velocity of 0.1 m/ns.

Why: the 1) 2) 3) list becomes paragraph prose, the repeated "The processing" opener is varied, and the connector "so" carries the result.

---

## Default document format

- Font: Times New Roman.
- Size: 12 pt.
- Line spacing: 1.5.
- Paragraph first line indented, except inside tables.
- Headings bold at top level ("1. Introduction"), subsection labels italic ("2.1").
