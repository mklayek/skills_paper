# ✍️ Writer brief: one teaching paragraph per slide

Paste this whole brief into every writer's prompt, then add the writer's slide numbers, the mathematics runs among
them, the input paths and the output file.

## The job

The lecturer reads each paragraph in class, word for word. **Reading it explains the slide completely**:
every point on the slide (its text, figure, table and equations), the physical picture behind it, the findings and
key numbers, and what each important point means. Read the slide **image** (`temp/extract/slides/slide_NN.png`) as
well as the text dump (`temp/extract/slides_text.md`), because figures and tables carry content. Use richer source
notes if the user names them (for example the Markdown of derivation figures).

**Never mention that the text is read aloud, spoken or a script.** It is simply the teaching note for the slide.

## Output file contract

For every assigned slide, in slide order:

```markdown
## Slide NN · <slide title as printed, bullet glyphs such as ◆ ■ ● dropped, "(continued)" kept>

<exactly one paragraph>

**Insight:** <optional second paragraph, see "Insight paragraph" below>
```

- `NN` is the slide number. One blank line between heading and paragraph, and one blank line between the
  paragraph and its Insight paragraph. Nothing else in the file.
- A slide with no printed title (only a small tag such as "ICA") gets a short descriptive title written from its content.

## Paragraph contract

A paragraph is a sequence of short sentences, each of one of these four kinds, mixed naturally:

| Kind | Shape | Example |
|---|---|---|
| Statement | a plain fact, definition or finding from the slide | "Chargeability is measured in milliseconds." |
| Statement + consequence | fact, then what follows from it, only where the slide or source gives that consequence | "The Sun rises in the east, and for this we have life on earth." / "Clay surfaces carry negative charge, so positive ions crowd the pore water near them." |
| Equation reading | one sentence per equation saying how the quantities move together, checked against the formula | "We can get an idea from this equation that a larger area under the decay curve gives a larger $M$." |
| **Significance (dark red)** | after an important point, one sentence on what it means, why it matters or the contrast it creates | `\textcolor[HTML]{8B0000}{PCA separates uncorrelated components, whereas ICA separates statistically independent components, providing stronger signal separation.}` |

Rules that complete the contract:
1. **Cover every point.** Every bullet and sub-point, every table row, the key numbers, names and units, and what
   each figure shows, in the slide's order. Nothing on the slide is left out.
2. **Length:** the `words` range in `docs/notes_config.json` (default 45 to 240), display equations not counted. Use
   only as many words as full coverage needs.
3. **Significance sentences:** written exactly as `\textcolor[HTML]{8B0000}{<one sentence>}` inside the paragraph.
   Only after **important** points: usually 2 to 4 on a text-heavy slide, 1 or 2 on a figure slide, none on trivial
   points. Inside the braces: plain text and `$...$` only (no `**`, no `*`, no line break, because pandoc passes the
   command through as raw LaTeX). Each one must follow from the slide or the sources.
4. **Voice:** first-person lecturer speaking to students. The paragraph is only what is said, so it holds no stage
   directions ("Look at", "point to", "draw", "ask the class") and no questions.
5. **Openings:** start with the slide's subject ("Chargeability $M$ is ..."), never with "Here", "This slide", "Let us", "So".
6. **Links:** vary them (", and for this", ", so", ". Because of this,", ", which means"). Use "and for this" at most twice.
7. **Figures:** name what a figure shows in words ("the upper diagram shows ..."). No figure numbers, no "Figure 9.2".
8. **Abbreviations:** write each in full the first time in every paragraph: Induced Polarization (IP).
9. **Math:** inline `$...$`. At most one display equation, `$$...$$` on its own line **inside** the paragraph with no blank
   line before or after it. A display must fit a narrow column (about 45 characters of rendered math), so break a long
   chain as `$$\begin{aligned}a &= b\\ &= c\end{aligned}$$`. Use `\mathrm{rms}`, never `{\rm rms}`: the old font
   commands `\rm`, `\bf`, `\it` stop the KOMA build.
10. **Spelling and punctuation:** US English (meter, color, behavior, analyze, ohm-meter). No em dashes. No semicolons
   outside math.
11. **Faithful:** keep the slide's numbers, names and units. Invent nothing. When a slide statement looks wrong
   (a reversed inequality, a wrong unit), write the physically correct statement in the paragraph and report the slide
   number and the issue in your reply, so the lead can tell the user.

## Mathematics slides: one summary block per run

A run of derivation slides ("<topic>: the mathematics and the algorithm" plus its "(continued)" slides, listed by the
lead from `math_runs` in the config) gets **one block only**, headed with the first slide, the title ending with the span:

```markdown
## Slide 40 · ICA: the mathematics and whitening (slides 40 and 41)
## Slide 73 · f-k filtering: the mathematics, the masks and the algorithm (slides 73 to 76)
```

- The other slides of the run get no block.
- The paragraph **summarizes** the derivation, it does not walk through it. It says what quantity is calculated, how
  (the chain of main steps in plain words) and its significance (what it does to the data and why it matters).
- **7 to 8 printed lines at most** (`math_max_lines`). That is about 45 to 53 words at 13 pt, or 55 to 68 at 11 pt
  (`math_words`).
- No display equation, no Insight paragraph, no dark-red sentence, at most two or three short inline symbols
  ($k$, $\lambda$, $L+S$).

## Insight paragraph (second paragraph, where applicable)

After the main paragraph, add a **second paragraph** that starts with the bold label `**Insight:**` followed by
1 or 2 sentences (15 to 45 words, the `insight_words` range). It gives what a student gains beyond the slide:

- an intuition or physical picture,
- a practical field or processing tip,
- a common pitfall and how to spot it in the data,
- a link to another step or concept of the lecture,
- why the result matters for interpretation.

Add it on most slides (aim for 80 % or more) and skip it only where it would repeat the paragraph or a dark-red
sentence. Never on a mathematics summary block. It follows the same rules as the paragraph (voice, US English, no em
dash, no semicolon outside math, no questions), must be physically correct, invents no data or citations, and never
repeats an insight from another slide. It does not count toward the paragraph's `words` range. One Insight paragraph
per slide at most, always after the main paragraph.

## Editing the file

Write and edit the section file **only with the Write or Edit tool** (or a Python file). A bash heredoc, `printf`,
`echo` or `sed` turns `\b`, `\t`, `\r` into control characters: `\bar` became a backspace and `\textcolor` lost its
`\t` in earlier runs. After writing, check the file has no bytes below 0x20 other than newline, and that every
`\textcolor[HTML]{8B0000}{` has its closing `}`.

## Before you reply

- Count words per paragraph, search for `—`, for `;` outside math and for "Look at", "Here", "?".
- Reply with: file written, number of blocks, word range, dark-red sentences per slide, insights added (and slides
  skipped), any slide points you could not fit, and any slide issues found (rule 11).
