_Template date: 2026-07-09_

# Tables — template

## Purpose & writing logic

    Tables consolidate the parametric and comparative facts that would otherwise clutter the prose. None of the three source papers actually used a formal numbered table: Goodman et al. (1995), Dalan et al. (2011), and Goodman et al. (2014) all conveyed survey parameters, calibration constants, and anomaly inventories in running prose or in figure annotations. That absence is itself the lesson. A short paper can be table-free, but a full journal manuscript benefits from lifting the flat prose list of acquisition and processing parameters into a Table 1, and from collecting per-anomaly findings into an anomaly-catalogue table. The Goodman et al. (2014) analysis explicitly recommends table-ifying its prose parameter list (200, 270, 500 MHz frequencies; 50 cm and 25 cm line spacing; the dewow, bandpass, Kirchhoff migration, Hilbert transform chain) into a survey-parameters table.

    The two table archetypes for this genre are the survey-parameters table (one row per site or antenna configuration, columns for frequency, spacing, sampling window, processing steps) and the anomaly-catalogue table (one row per detected anomaly, columns for identifier, location, depth, size, interpretation, and validation status). The anomaly catalogue makes the paper's five-tier validation hierarchy (from excavation-confirmed down to unconfirmed-prospective) auditable at a glance.

## When to write / what belongs here

    Write the survey-parameters table once the Methods section stabilizes, so its numbers are the single source of truth that the Methods prose then references rather than repeats. Write the anomaly-catalogue table alongside the Results, adding a row each time you interpret a new anomaly. What belongs in a table: repeated, structured, comparable values (frequencies, spacings, depths, dimensions, calibration constants) and per-item inventories (anomalies, boreholes, features). What does not belong: narrative interpretation, physical justification, or a single one-off number that reads fine in a sentence. If a value appears only once and needs a sentence of context, leave it in prose.

## Fill-in skeleton

Survey-parameters table:

```
Table {{N}}. GPR survey and processing parameters for the {{site name}} campaign.

| Site / target        | Antenna frequency | Line spacing | Sampling window        | Processing steps                                  |
|----------------------|-------------------|--------------|------------------------|---------------------------------------------------|
| {{site or grid}}     | {{e.g., 500 MHz}} | {{e.g., 50 cm}} | {{e.g., 30 cm depth}} | {{dewow, bandpass, migration, Hilbert transform}} |
| {{mound tops}}       | {{e.g., 270 MHz}} | {{e.g., 25 cm}} | {{...}}                | {{...}}                                           |
```

Anomaly-catalogue table:

```
Table {{N}}. Catalogue of GPR anomalies at {{site name}}, with interpretation and validation status.

| ID       | Location / grid  | Depth (m) | Size            | Interpretation            | Validation status            |
|----------|------------------|-----------|-----------------|---------------------------|------------------------------|
| {{A1}}   | {{x, y or grid}} | {{2.5}}   | {{22 m diam.}}  | {{buried moat}}           | {{excavation-confirmed}}     |
| {{A2}}   | {{...}}          | {{1.1-1.4}} | {{cluster}}   | {{chamber cluster}}       | {{unconfirmed / prospective}}|
```

    Inline instruction: give every table a numbered caption above the table (Table 1, Table 2, ...) written as a self-sufficient sentence, matching the figure-caption discipline. Keep column headers short and unit-bearing. State the unit in the header (Depth (m)) rather than repeating it in every cell. Cell text is terse and does not take a first-line indent. Reference each table in the body as "Table N".

## Expected content

    A survey-parameters table has one row per site, target zone, or antenna configuration, with columns covering frequency, line spacing, sampling or depth-slice window, and the ordered processing chain. An anomaly-catalogue table has one row per interpreted anomaly, with a stable identifier, its location, depth, size or dimension, the archaeological interpretation, and its validation status drawn from the five-tier hierarchy (excavation-confirmed, historically corroborated, typologically inferred, anecdotally supported, or unconfirmed-prospective). Every number in a table matches the corresponding number in the prose and captions. Tables are numbered in citation order and each is referenced at least once in the body.

## Style / format rules

- Caption goes above the table, numbered "Table N.", written as a self-sufficient sentence.
- Units live in the column header, not repeated in every cell.
- No first-line indent inside table cells. Cell content is terse, sentence-fragment style, not full indented paragraphs. This is the one place the paper's body first-line-indent rule does not apply.
- Column headers are short and consistent across tables.
- One row per site, configuration, or anomaly. Do not merge multiple items into one cell.
- Every table value agrees with the prose and caption values for the same quantity.
- Tables are numbered in order of first citation and each is cited as "Table N" in the body.
- Wide tables must be allowed to scroll or wrap rather than force the page to overflow.
- US English throughout. No em dashes in cells (use a comma, a range hyphen, or "to"). Avoid semicolons; separate list items in a cell with commas.

## Common phrases / real examples

- Prose that should become a survey-parameters table row: "GPR surveys employing varying frequencies from 200, 270 and 500 MHz have been expedited. ... Profiles for most sites were recorded at 50cm intervals, 25cm on the tops of burial portions. Radargram signal processes included dewowing, bandpass filtering, Kirchoff migration and Hilbert transform." (Goodman et al., 2014, prose that the analysis recommends table-ifying)
- Prose that should become an anomaly-catalogue row: "On the deepest slice, 40-48 ns, a large ring-like anomaly is imaged. The ring anomaly is approximately 22 m in diameter. This radar structure is believed to be a moat." (Goodman et al., 1995: ID, depth window, size, interpretation)
- A calibration constant belongs in a parameters table: "Multiplying values by 1.4 x 10^-5 yields SI susceptibilities; this calibration factor is suggested by Bartington Instruments for 24-mm holes." (Dalan et al., 2011)
- A validation-status entry: "One pit dwelling within the southern trench at (x = 1 m, y = 7 m) ... were found with radar and corroborated by the previous excavation." (Goodman et al., 1995: excavation-confirmed)
- A negative result still earns a catalogue row: "None of the methods appear to detect the northern pit." (Dalan et al., 2011)
- Caption style, self-sufficient: "Table 1. GPR survey and processing parameters for the Saitobaru campaign, by antenna frequency and target zone."

## Quality checklist

- [ ] Each table has a numbered caption above it, written as a self-sufficient sentence.
- [ ] Units appear in column headers, not repeated in every cell.
- [ ] No first-line indent inside table cells; cell text is terse.
- [ ] Every value in a table matches the same value in the prose and figure captions.
- [ ] The survey-parameters table has one row per site, configuration, or antenna, covering frequency, spacing, window, and processing steps.
- [ ] The anomaly-catalogue table has one row per anomaly with a stable ID, depth, size, interpretation, and validation status.
- [ ] Every table is cited as "Table N" at least once in the body, numbered in citation order.
- [ ] US English, no em dashes or stray semicolons inside cells.

## Short worked example

    Prose in Methods: "Surveys used a 500 MHz antenna over open ground and a 270 MHz antenna over the mound tops, on 50 cm and 25 cm lines respectively. All radargrams were dewowed, bandpass filtered, migrated (Kirchhoff), and Hilbert-transformed before slicing (Table 1)."

```
Table 1. GPR survey and processing parameters for the Mound 12 campaign.

| Target zone   | Antenna frequency | Line spacing | Depth-slice window | Processing chain                                  |
|---------------|-------------------|--------------|--------------------|---------------------------------------------------|
| Open ground   | 500 MHz           | 50 cm        | 30 cm              | dewow, bandpass, Kirchhoff migration, Hilbert     |
| Mound tops    | 270 MHz           | 25 cm        | 30 cm              | dewow, bandpass, Kirchhoff migration, Hilbert     |
```

```
Table 2. Catalogue of GPR anomalies at Mound 12, with interpretation and validation status.

| ID | Grid       | Depth (m) | Size          | Interpretation     | Validation status         |
|----|------------|-----------|---------------|--------------------|---------------------------|
| A1 | N10, E14   | 0.9 to 1.2 | 14 m diam.   | keyhole lodge wall | historically corroborated |
| A2 | N12, E16   | 2.5       | 2 chambers    | tomb chambers      | excavation-confirmed      |
| A3 | N14, E20   | 1.1 to 1.4 | cluster      | chamber cluster    | unconfirmed, prospective  |
```
