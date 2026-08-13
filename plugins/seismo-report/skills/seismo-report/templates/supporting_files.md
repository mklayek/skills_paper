# Supporting files (seismo-report)

&nbsp;&nbsp;&nbsp;&nbsp;The skill maintains a small set of supporting files alongside the report, each with a minimal header block that the skill fills in as the report develops. Every file below carries its own one-line purpose.

## REPORT.md
&nbsp;&nbsp;&nbsp;&nbsp;The master editable report, the same Markdown that `scripts/build_report.py` converts to HTML, LaTeX/PDF, and optionally DOCX/PPTX.
```
<!-- REPORT.md — master editable report -->
{{YYYY-MM-DD}}
```

## HANDOUT.md
&nbsp;&nbsp;&nbsp;&nbsp;Continuation memory across sessions, so a later run of the skill picks up where the last one left off.
```
<!-- HANDOUT.md — continuation memory -->
Status: {{in progress / draft complete / approved}}
```

## figure_inventory.md
&nbsp;&nbsp;&nbsp;&nbsp;The numbered figure list with source paths and captions, kept in sync with `figures_and_captions.md`.
```
<!-- figure_inventory.md — numbered figure list -->
| Figure | Source path | Caption |
|---|---|---|
```

## bibliography.md
&nbsp;&nbsp;&nbsp;&nbsp;Author-date entries, real works only, matching the in-text citations used across the report.
```
<!-- bibliography.md — author-date reference list -->
```

## glossary.md
&nbsp;&nbsp;&nbsp;&nbsp;Defined terms used throughout the report, one entry per term.
```
<!-- glossary.md — defined terms -->
```

## abbreviations.md
&nbsp;&nbsp;&nbsp;&nbsp;Expansions of every abbreviation used in the report, matching the first-use definitions in the body.
```
<!-- abbreviations.md — abbreviation expansions -->
```

## equation_index.md
&nbsp;&nbsp;&nbsp;&nbsp;Numbered equations with their page or section, so any equation can be located quickly.
```
<!-- equation_index.md — numbered equation index -->
| Equation | Section | Description |
|---|---|---|
```

## processing_log.md
&nbsp;&nbsp;&nbsp;&nbsp;A dated log of build actions, which are Markdown edits, HTML/PDF/DOCX builds, and approval checkpoints.
```
<!-- processing_log.md — dated build actions -->
| Date | Action |
|---|---|
```
