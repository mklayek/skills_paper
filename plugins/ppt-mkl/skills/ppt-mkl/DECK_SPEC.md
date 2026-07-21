# Deck-source mini-language (STRICT) — `build_styled_slides.py`

Every line starts with one of the prefixes below. **No other line types are allowed.**
Blank lines are ignored. Never use plain markdown headings, tables, HTML, or fenced code.

| Prefix | Meaning |
|---|---|
| `# <Section title>` | section divider slide (use sparingly, one per major part) |
| `== <Title>` | **starts a new slide**; the title line |
| `- <text>` | level-0 bullet, rendered with a green ☑ box |
| `-- <text>` | level-1 sub-bullet, rendered with a red ✪ |
| `--- <text>` | level-2 sub-bullet, rendered with a small • |
| `$$ <latex> $$ (N)` | display equation, ONE line, numbered `(N)` at the right |
| `$$ <latex> $$` | display equation, unnumbered |
| `!key: <text>` | bold black "takeaway" line (the one-sentence conclusion) |
| `!so: <text>` | purple handwriting "Therefore, …" line (the intuition) |
| `!fig: <abs path> <NN%>` | figure, centred at the bottom of the slide |
| `!note: <text>` | speaker note (one line; repeatable, lines are joined) |

## Inline formatting inside any text line
- `$ … $` — inline LaTeX math (becomes a native editable PowerPoint equation).
- `**term**` — maroon bold key term.
- `==term==` — yellow-highlighted bold red term (use ≤1 per slide, for THE key phrase).
- Use ` — ` (em dash) freely. Do not use other markdown (no `*italic*`, no backticks, no links).

## Title rules (IMPORTANT)
- Format: `== <PREFIX> : <topic>` where `<PREFIX>` is one of `CCT`, `DCT`, `LCCF`, `Frame`,
  `Why`, `Recap`. Example: `== CCT : Frequency-domain construction and admissibility`
- The title must be a **topic**, NEVER an equation name. Forbidden: "Equation (7)",
  "Eq. 12 — tightness", "The partition of unity equation".
- Wrap the single most important word/phrase of the topic in `**…**` → renders red.
- Keep titles ≤ 8 words after the prefix.

## Slide budget rules
- ≤ 6 level-0 bullets, ≤ 2 display equations, ≤ 1 figure per slide.
- A slide with a figure gets ≤ 3 bullets and ≤ 1 equation.
- If a source block needs more, SPLIT into two slides with `(1/2)` / `(2/2)` NOT in the title —
  instead give each half its own distinct topical title.
- Bullet text ≤ ~22 words. Symbol-definition bullets are short: `$ symbol $ — meaning.`

## Equation pretext (MANDATORY)

**Every `$$ … $$` MUST be immediately preceded by a `-` bullet saying what the equation
establishes, ending in a PLAIN connecting phrase and a colon.** The emphasis goes on the
substance, never on the connector: bold the phrase naming what the equation makes explicit,
defines, estimates or bounds. That bold phrase renders dark brown.

```
- Writing the atom directly in the frequency plane at integer scale $j$, in polar coordinates $(r,\vartheta)$, makes the **discrete construction explicit**, given by:
$$ \tilde U_{j,\ell}(\omega)=\tilde W_j(\omega)\,\tilde V_{j,\ell}(\omega) $$ (18)
```

- ✅ `…makes the **discrete construction explicit**, given by:`
- ❌ `…makes the discrete construction explicit, **given by:**` — connector bolded, substance left plain
- ❌ `**Given by:**` — no description of what the equation does

Connectors — always **plain**, always ending in `:`, varied so the deck does not read
mechanically, and chosen to fit the sentence grammatically:

`given by:` · `expressed as below:` · `formulated as below:` · `described as:` ·
`written as:` · `stated as below:` · `defined as below:`

- Exactly **one** bold phrase per lead-in, 2-5 words — e.g. **term count**,
  **exact reconstruction**, **anisotropic dilation matrix**, **tight-frame property**.
- Never let an equation follow a bullet that ends in a full stop.
- Never open a slide with an equation that has no lead-in bullet.
- `==yellow highlight==` is a different marker — never use it for the pretext.
- The builder warns on: no lead-in · no connector · bolded connector · no bold phrase.
  A clean build has zero warnings.

## Content pattern to follow per equation (this is the deck's rhythm)
1. one `-` lead-in bullet stating what the equation establishes, with that substance in
   bold and a PLAIN connector + colon at the end (see "Equation pretext" — mandatory);
2. the `$$ … $$ (N)` line — **the number N must be exactly the `\tag{N}` from the source**;
3. `-` or `--` bullets defining each symbol (from the source's "Symbols in (N)" list, shortened);
4. `!key:` the one-sentence result;
5. `!so:` the plain-language "in simple terms" takeaway, starting with "Therefore," / "So,";
6. `!note:` the source's "Discussion." paragraph, condensed to 1–3 sentences.

Not every equation needs all six; short/auxiliary equations may share a slide.

## Example (renders exactly like the reference deck)

```
== CCT : Frequency-domain construction and **admissibility**
- For the family to tile frequency without gaps or overlaps in energy, $ W $ and $ V $ must satisfy **admissibility** conditions — unit total energy under the scale-invariant (Haar) measures:
$$ \int_{0}^{\infty} W(r)^2\,\frac{dr}{r}\ =\ 1, \qquad\qquad \int_{-\infty}^{\infty} V(t)^2\,dt\ =\ 1 $$ (7)
- $ W(r)^2 $ or $ V(t)^2 $ — energy density.
- $ t=(\theta_\xi-\theta)/\sqrt{a} $ — the scaled-angle variable.
- Equation (7) directly yields the ==partition of unity== underlying the tight-frame property:
$$ \sum_{\text{scales}}\ \sum_{\text{orientations}} \big|\,W(a|\xi|)\,V(\cdot)\,\big|^{2}\ =\ 1 \qquad\text{for a.e. }\xi\neq 0 $$ (8)
-- $ \sum_{\text{scales}}\sum_{\text{orientations}} $ — the double sum over every ring and every wedge.
-- $ |W(a|\xi|)\,V(\cdot)|^{2} $ — the squared magnitude of each ring × wedge window product.
!key: The sum of the squared weights of all overlapping tiles is exactly 1.
!so: Therefore, the curvelet tiles neither increase the energy by overlap nor lose information by leaving gaps.
!note: The product of two partitions of unity (radial and angular) is itself a partition of unity, which is exactly (8): at any frequency, the squared weights of all overlapping tiles add to one. The ring-times-wedge tiles neither pile up energy nor leave holes.
```
