_Template date: 2026-07-09_

# Data Acquisition — template

## Purpose & writing logic

&nbsp;&nbsp;&nbsp;&nbsp;The Data Acquisition section records the physical facts of the survey: what antenna, at what spacing, over what grid, with what GPS or georeferencing, in what ground. It is the reproducibility spine of the paper. Across the three source papers the level of hardware detail rises with the number of co-authors. Goodman et al. (1995) name a 300 MHz antenna with a 45 cm aperture and a scan density in running prose. Dalan et al. (2011) name make, model, and even improvised probe materials ("a cardboard tube with bands of aluminum foil"). Goodman et al. (2014) compress frequencies, line spacing, and penetration into one paragraph and let ground conditions carry the "why."

&nbsp;&nbsp;&nbsp;&nbsp;Generally the writing logic is to state the acquisition parameters as declarative, checkable facts, and to anchor line spacing to the lateral extent of the target. In this case the reusable move is to give a rationale clause with each hardware choice, so a lower frequency is tied to deeper stratigraphic targets and a tighter line spacing is tied to a small feature. That's why the acquisition text reads as a set of justified settings rather than an equipment inventory.

## When to write / what belongs here

&nbsp;&nbsp;&nbsp;&nbsp;Write this as the acquisition half of Methods, before processing. It belongs here whenever a reader needs the survey settings to judge resolution and depth reach. In this case the natural table-ification point lives here: the flat prose list of frequencies, spacings, and windows should be lifted into a survey-parameters table for a full journal article, as Goodman et al. (2014) never do but plainly could. Keep processing steps out of this file; they belong in `07_processing.md`.

What belongs here:
- Antenna frequency or frequencies and the selection rationale.
- Line spacing and any denser spacing over key targets.
- Sampling (scans per meter, samples per scan, time window).
- Survey grid layout, orientation, and extent.
- GPS or georeferencing method.
- Instrument make, model, and system.
- Ground conditions affecting penetration.

## Recommended paragraph flow

1. Name the antenna frequency or frequencies and why each was chosen (resolution versus depth trade-off).
2. State the survey grid: extent, orientation, line direction, and the survey pattern.
3. Give line spacing, with tighter spacing over specific targets called out.
4. Give the sampling scheme (scans per meter, time window, marker interval).
5. State the GPS or georeferencing method and coordinate system.
6. State the ground conditions (soil type, resistivity, moisture) and the penetration depth achieved.

## Fill-in skeleton

&nbsp;&nbsp;&nbsp;&nbsp;GPR surveys employed `{{frequency list, e.g. 200, 270, 500}}` MHz antennas `{{system name if relevant}}`. `[Instruction: give a frequency-selection rationale, e.g. the lower frequency for deeper stratigraphic targets, the higher for shallow resolution.]` The survey covered a `{{extent, e.g. 54 hectare}}` grid oriented `{{orientation}}`, with profiles recorded in a `{{pattern}}` direction.

&nbsp;&nbsp;&nbsp;&nbsp;Profiles were recorded at `{{value}}` cm line intervals, narrowing to `{{value}}` cm over `{{target zone, e.g. mound tops}}`. `[Instruction: always tie the spacing to the target size, the way all three papers do.]` Data were sampled at `{{scans per meter}}` with a `{{time window}}` ns window, and a marker was placed every `{{unit}}`.

&nbsp;&nbsp;&nbsp;&nbsp;Positions were fixed using `{{GPS / total station / grid-tape method}}` in `{{coordinate system, e.g. WGS-84}}`. `[Instruction: state the georeferencing even if it is a simple local grid; Goodman et al. (2014) drape slices on Google Earth, which implies a georeferencing step worth naming.]`

&nbsp;&nbsp;&nbsp;&nbsp;Ground conditions were `{{soil type, e.g. highly resistive volcanic soils}}`, permitting penetration to `{{depth in ns or m}}` even with the `{{highest frequency}}` antenna.

### Survey-parameters table template (Table 1)

| Parameter | Value | Notes / rationale |
|---|---|---|
| Antenna frequency(ies) | `{{200, 270, 500 MHz}}` | `{{lower = deeper stratigraphy}}` |
| System / instrument | `{{make, model}}` | `{{}}` |
| Line spacing | `{{50 cm; 25 cm over mound tops}}` | `{{tied to target extent}}` |
| Line direction / pattern | `{{zig-zag / parallel, orientation}}` | `{{}}` |
| Sampling density | `{{scans per meter}}` | `{{resampled to constant value}}` |
| Time window | `{{ns}}` | `{{penetration observed}}` |
| Grid extent | `{{area / dimensions}}` | `{{}}` |
| Georeferencing | `{{GPS / total station / local grid}}` | `{{coordinate system}}` |
| Ground conditions | `{{soil type, resistivity, moisture}}` | `{{affects penetration}}` |

## Expected scientific content

- Antenna frequency(ies) with a resolution-versus-depth rationale.
- Grid extent, orientation, and survey pattern.
- Line spacing, including any denser spacing over targets.
- Sampling density and time window.
- Marker or fiducial interval for along-line positioning.
- GPS or georeferencing method and coordinate system.
- Instrument make, model, and system name.
- Ground conditions and observed penetration depth.
- A survey-parameters table (Table 1) for full journal format.

## Citation strategy

&nbsp;&nbsp;&nbsp;&nbsp;Generally acquisition text is light on citations, since the settings are the authors' own. In this case cite the origin of any nonstandard survey design or the companion reference that documents the field protocol in full, and cite the instrument or calibration source when a specific conversion factor is stated, the way Dalan et al. (2011) attribute a susceptibility calibration factor to Bartington Instruments. Use author-year in-text refs `(Author et al., 2023)`, sentence-final.

## Figure/table references typical here

&nbsp;&nbsp;&nbsp;&nbsp;A grid-layout or regional context map is commonly referenced here (Figure 1 in all three papers is a locational or context map). The survey-parameters table is Table 1. A photograph of the instrument in the field is optional but common in multi-instrument papers. Refer to figures as "Figure N" spelled out in body text.

## Tense & voice guidance

&nbsp;&nbsp;&nbsp;&nbsp;Generally use the simple past, passive voice, because acquisition is a completed procedure with the data as subject. So write "Profiles were recorded at 50 cm intervals." However, ground conditions that still hold take the present tense, as when a paper states that penetration in the resistive soils is quite good. Throughout, keep the register factual and avoid first person.

## Common phrases / sentence openers

- "A 300 MHz radar antenna with a 45 cm aperture was used in the survey."
- "Profiles for most sites were recorded at 50cm intervals."
- "GPR surveys employing varying frequencies from 200, 270 and 500 MHz have been expedited."
- "Penetration depths with GPR are quite good in the highly resistive volcanic soils."
- "The magnetic data were collected... with a Bartington 601-2 dual fluxgate gradiometer using a 1-m line spacing and an eight-sample per m collection strategy."
- "Because the spatial sampling would vary between metre marks due to varying antenna speeds, the data were later resampled to a constant 50 scans m."

## Quality checklist

- [ ] Antenna frequency(ies) are stated with a selection rationale.
- [ ] Line spacing is given and tied to target size, with any denser spacing called out.
- [ ] Sampling density and time window are stated.
- [ ] The GPS or georeferencing method and coordinate system are named.
- [ ] Instrument make and model are identified.
- [ ] Ground conditions and observed penetration depth are stated.
- [ ] A survey-parameters table is included for full journal format.
- [ ] The section is in simple past, passive voice, with no unjustified first person.

## Short worked example

&nbsp;&nbsp;&nbsp;&nbsp;GPR surveys at the Raj Ghat grid employed 270 and 500 MHz antennas, with the lower frequency reserved for the deeper stratigraphic targets and the higher frequency used to resolve shallow structure. The survey covered a 60 by 40 m grid oriented along the river bank, with profiles recorded in parallel lines. Profiles were recorded at 50 cm intervals, narrowing to 25 cm over the suspected mound crest. Data were sampled at a constant 50 scans per meter with a 200 ns window, and a fiducial marker was placed every meter. Positions were fixed with a handheld GPS in WGS-84 and later reprojected to UTM 44N. Ground conditions were firm, moderately resistive floodplain silt, permitting penetration to roughly 180 ns even with the 500 MHz antenna. Table 1 summarizes the acquisition parameters.
