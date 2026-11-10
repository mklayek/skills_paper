---
name: aloud-notes-ppt
description: Use when the user wants read-aloud, speaking or lecture notes made from a PowerPoint deck (.pptx), one spoken paragraph per slide, "what I have to read out" for each slide, or a printable PDF script to explain the slides and their findings in class.
---

# 🎙️ aloud-notes-ppt: one spoken paragraph per slide, as a two-column PDF

## Overview
The lecturer reads each paragraph aloud and has then explained the slide: its points, figure, equations, findings and
meaning. The paragraph is built from **plain statements, statements with their consequence, and one reading per
equation**, never from stage directions or questions. The output is a compact two-column Latin Modern PDF.

Model sentence from the user: *"The Sun rises in the east, and for this we have life on earth."* Not every sentence
needs a consequence: *"The Sun rises in the east."* is a full sentence too, and so is *"We can get an idea from this
equation that if x rises, y falls."*

## 🎨 Page style (v1.1, the user's teaching-note layout)

| Element | Style | Config key (default) |
|---|---|---|
| Title block | two tight bold navy lines: title, then subtitle, crisp and small, then author, affiliation, year in small type | `title_pt` (15) |
| Body text | Latin Modern, two columns, KOMA class `scrartcl` so any size works | `fontsize` (13) |
| Margins | 1 cm on all four sides | `margin_cm` (1.0) |
| Writing gap under each slide heading | blank space for the lecturer's handwritten notes | `write_space_cm` (1.2) |
| Gap after each slide block | blank space after the Insight paragraph, before the next slide heading | `after_space_cm` (1.0) |
| Page number | alone in the bottom-right corner, no header or footer text | always |
| Slide range | notes for part of a deck, e.g. slides 46 to 85 | `range` ([1, last]) |
| Paragraph length | crisp | `words` ([60, 115]) |

The user's words in the chat override these defaults. Keep a project rules file (`docs/NOTES_STYLE_AND_RULES.md`) when
the user asks for one, listing their requests and the config values used.

**Not for:** detailed teaching notes with several labeled paragraphs per slide (what to say, how to explain, findings),
making slides (use the PPT skills) or equation-explainer notes from a book passage (`tex-notes-mkl`).

## Quick reference

| Step | Command / action | Result |
|---|---|---|
| 1. Folder | user's task folder, or a new `<NN>_<Topic>_Read_Aloud_Notes` beside the deck work | `sections/ figs/ docs/ temp/ archive/` |
| 2. Extract | `python scripts/extract_deck.py <deck.pptx> <task_folder>` | slide PNGs, `slides.json`, `slides_text.md`, config template |
| 3. Configure | edit `docs/notes_config.json` | title, author, skip list, parts, limits |
| 4. Write | writer agents with `reference/WRITER_BRIEF.md` | `sections/NN_slides_x.md` |
| 5. Build | `python scripts/build_notes.py <task_folder>` | PDF at the top, master MD in `docs/`, ALL CHECKS PASSED |
| 6. Look | render 2 pages, view them | layout confirmed |

## Workflow

1. **Archive first.** If the task folder already has a PDF or sections, copy them to `archive/<date>_v<N>/`.
2. **Never write into the deck's folder when it is protected** (for example `PPT_class_kr\PPT\`). `extract_deck.py`
   copies the deck and opens only the copy. It never calls PowerPoint `Quit`.
3. **Configure** `docs/notes_config.json`:
   - `range`: the slides the user asked for (default all). Only slides inside it get a block.
   - `skip`: slides with no paragraph. The script proposes candidates with almost no text. Confirm them against the
     images (title slide, section dividers, closing "Thank you" slide).
   - `parts`: `{"<first slide of the part>": "<divider title>"}`, taken from the divider slides.
   - `title`, `subtitle`, `author`, `affiliation`, `year`: ask the user only if the deck and chat do not give them.
   - layout keys from the page-style table above (`fontsize` 13, `title_pt` 15, `write_space_cm` 1.2,
     `after_space_cm` 1.0, `margin_cm` 1.0), plus `words` (default `[60, 115]`), `insight_words` (default `[15, 45]`),
     `max_pages`, `slides_per_page`.
4. **Write** with writer agents when the deck has more than about 12 content slides: split the content slides into
   groups of 7 to 9 and dispatch the groups in parallel. Each prompt is `reference/WRITER_BRIEF.md` pasted in full plus
   the slide numbers, the input paths and the output file `sections/<first slide>_slides_<letter>.md`. If the user gives
   richer source notes (detailed teaching notes, a book chapter), add their path as an input.
5. **Build** and fix until the script prints **ALL CHECKS PASSED**: one paragraph per content slide (plus at most one
   **Insight:** paragraph after it), word ranges, no em
   dash or semicolon, no leftover labels, 0 missing glyphs, 0 overfull lines, page and slides-per-page limits.
6. **Look** at two rendered pages (`pdftoppm -r 60 -f 1 -l 2`).
7. **Report**: path, pages, slides per page, any slide issues the writers flagged, choices made.

## 💡 Insight paragraph (default on)

Each slide block may end with a **second paragraph** starting with `**Insight:**`: 1 or 2 sentences (15 to 45 words)
with an intuition, a field or processing tip, a pitfall, a link to another step, or why the result matters. Writers
add it on most slides (`reference/WRITER_BRIEF.md`). It renders as its own paragraph with a bold label, is checked
against `insight_words`, and does not count toward `words`. Write it as a plain Markdown paragraph, never with raw
TeX such as `\par`. The build prints how many slides carry one. Insights add about 20 % to the page count.

```markdown
## Slide 20 · Chargeability M

Chargeability $M$ is the most common time-domain ... the classic pointer to disseminated sulfides.

**Insight:** Two surveys can only be compared when their integration windows match, so I always note the receiver
window next to every chargeability value.
```

## Fitting page limits

Slides per page and page count trade against font size and length. The build script prints both.

| Need | Change, in this order |
|---|---|
| fewer pages | `after_space_cm` and `write_space_cm` down (only if the user agrees, they are writing space), then `words` max down by 15, then `fontsize` down |
| last page nearly empty | same as above, a small cut is often enough |
| bigger type | each pt of `fontsize` adds about 15 % pages. 13 pt with the writing gaps gives about 4 slides per page |

Arithmetic first: 54 content slides cannot give 7 per page on 8 pages (that needs 56). When the user's limits conflict,
build the closest version and ask which limit wins (AskUserQuestion).

## Common mistakes

| Mistake | Fix |
|---|---|
| "Look at the figure on the right", "Why is ...?" | the paragraph is only spoken content: state what the figure shows |
| every sentence forced into "..., and for this ..." | plain statements are fine. Keep a consequence only where the source gives one |
| equation spelled out but never interpreted | one "We can get an idea from this equation that ..." sentence per equation, direction checked |
| copying a slide error as fact | write the correct physics, flag the slide number to the user |
| metres, colour, behaviour | US spelling: meters, color, behavior |
| 180 to 200 word paragraphs | stay in the `words` range, cut asides, never cut slide points |
| editing the build output by hand | edit `sections/*.md` or the config, then rebuild |
| heredoc or sed edits on LaTeX in Markdown | backslashes get eaten: edit with the Edit tool or a Python file |
| mapping ∫ ∂ Σ ∞ √ with `newunicodechar` | XeLaTeX hangs under unicode-math. The script maps only Greek and relation glyphs |
| `/d/...` paths from Git Bash to `extract_deck.py` | the output lands in `D:\d\...`. Pass Windows paths (`D:/...`) |
| notes for a slide range written for every slide | set `range`, and put only the dividers inside the range in `skip` |

## Files
- `scripts/extract_deck.py`: copy, export through PowerPoint, render, dump text, write the config template.
- `scripts/build_notes.py`: master MD, pandoc, XeLaTeX twice, all checks. The config keys are listed in its docstring.
- `reference/WRITER_BRIEF.md`: the paragraph contract given to each writer.
- `examples/sample_paragraphs.md`: two finished paragraphs (a mechanism slide and an equation slide).

Requirements: Windows with PowerPoint (export), Python with `python-pptx` and `pymupdf`, pandoc, XeLaTeX with Latin
Modern, KOMA-Script (`scrartcl`) and `eso-pic`.
