# ✍️ Writer brief: one read-aloud paragraph per slide

Paste this whole brief into every writer's prompt, then add the writer's slide numbers, the input paths and the output file.

## The job

The lecturer reads each paragraph aloud in class, word for word. **Reading it explains the slide completely**:
every point on the slide (its text, figure, table and equations), the physical picture behind it, the findings and
key numbers, and what it means. Read the slide **image** (`temp/extract/slides/slide_NN.png`) as well as the text dump
(`temp/extract/slides_text.md`), because figures and tables carry content. Use richer source notes if the user names them.

## Output file contract

For every assigned slide, in slide order:

```markdown
## Slide NN · <slide title as printed, bullet glyphs such as ◆ ■ ● dropped, "(continued)" kept>

<exactly one paragraph>
```

- `NN` is the two-digit slide number. One blank line between heading and paragraph. Nothing else in the file.

## Paragraph contract

A paragraph is a sequence of short sentences, each of one of these three kinds, mixed naturally:

| Kind | Shape | Example |
|---|---|---|
| Statement | a plain fact, definition or finding from the slide | "Chargeability is measured in milliseconds." |
| Statement + consequence | fact, then what follows from it, only where the slide or source gives that consequence | "The Sun rises in the east, and for this we have life on earth." / "Clay surfaces carry negative charge, so positive ions crowd the pore water near them." |
| Equation reading | one sentence per equation saying how the quantities move together, checked against the formula | "We can get an idea from this equation that a larger area under the decay curve gives a larger $M$." |

Rules that complete the contract:
1. **Length:** the `words` range in `docs/notes_config.json` (default 85 to 140), display equations not counted.
2. **Voice:** first-person lecturer speaking to students. The paragraph is only what is said, so it holds no stage
   directions ("Look at", "point to", "draw", "ask the class") and no questions.
3. **Openings:** start with the slide's subject ("Chargeability $M$ is ..."), never with "Here", "This slide", "Let us", "So".
4. **Links:** vary them (", and for this", ", so", ". Because of this,", ", which means"). Use "and for this" at most twice.
5. **Figures:** name what a figure shows in words ("the upper diagram shows ..."). No figure numbers, no "Figure 9.2".
6. **Abbreviations:** write each in full the first time in every paragraph: Induced Polarization (IP).
7. **Math:** inline `$...$`. At most one display equation, `$$...$$` on its own line **inside** the paragraph with no blank
   line before or after it. A display must fit a narrow column (about 45 characters of rendered math), so break a long
   chain as `$$\begin{aligned}a &= b\\ &= c\end{aligned}$$`.
8. **Spelling and punctuation:** US English (meter, color, behavior, analyze, ohm-meter). No em dashes. No semicolons
   outside math.
9. **Faithful:** keep the slide's numbers, names and units. Invent nothing. When a slide statement looks wrong
   (a reversed inequality, a wrong unit), write the physically correct statement in the paragraph and report the slide
   number and the issue in your reply, so the lead can tell the user.

## Before you reply

- Count words per paragraph, search for `—`, for `;` outside math and for "Look at", "Here", "?".
- Reply with: file written, number of blocks, word range, and any slide issues found (rule 9).
