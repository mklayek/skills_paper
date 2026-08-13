# Formatting spec (seismo-report)

## Body
- Font Times New Roman, 12 pt. Korean runs use Malgun Gothic (East-Asian font) so 한글 renders.
- Line spacing 1.15 (multiple).
- First line of every paragraph indented 0.5 in. No indent inside tables.
- Justified alignment.

## Heading hierarchy (matches the reference image: emphasis descends by level)
| Level | Markdown | Word style | LaTeX | Size | Weight |
|---|---|---|---|---|---|
| Section | `#` | Heading 1 | `\section` | 16 pt | bold |
| Sub-section | `##` | Heading 2 | `\subsection` | 14 pt | bold |
| Sub-sub-section | `###` | Heading 3 | `\subsubsection` | 13 pt | bold |
| Paragraph | `####` | Heading 4 | `\paragraph` | 12 pt | regular (not bold) |
| Sub-paragraph | `#####` | Heading 5 | `\subparagraph` | 12 pt | italic |

Author headings as ATX Markdown (`#` through `#####`), never as bold pseudo-headings (`**1. X**`): pandoc maps `#` to Heading 1 through `#####` to Heading 5 on DOCX and `\section` through `\subparagraph` on LaTeX/PDF, and `--number-sections` numbers them automatically, so no manual "1." prefix is written in the heading text. Section titles are one to two points bolder and bigger than the body. Each deeper level has a visibly different format, ending in a regular-weight paragraph head and an italic sub-paragraph head.

## Numbering
- Sections auto-numbered on export (`--number-sections`).
- Figures numbered "Figure N" in order of first in-text mention; tables "Table N"; equations "(N)". Captions sit under figures and above tables.

## Export mapping
- DOCX: pandoc `--reference-doc=reference_seismo.docx` (built by `scripts/make_reference_docx.py`). The reference doc encodes every rule above.
- PDF: xelatex via pandoc `-H scripts/preamble_seismo.tex -V mainfont="Times New Roman" --toc --number-sections`.
- HTML: pandoc `--standalone --embed-resources -c scripts/seismo.css`.
