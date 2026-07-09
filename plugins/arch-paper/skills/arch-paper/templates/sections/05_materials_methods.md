_Template date: 2026-07-09_

# Materials and Methods — template

## Purpose & writing logic

&nbsp;&nbsp;&nbsp;&nbsp;The Materials and Methods section tells the reader exactly what was done, in the order it was done, so the survey could be repeated by someone else. Across the three source papers the register varies a lot. Goodman et al. (1995) fold the whole method into an italic run-in sub-heading (*Time slice creation*) under the Introduction, with no separate "Methods" title at all. Dalan et al. (2011) give a full, spatially-organized methods block where each technique carries its own instrument spec, calibration constant, and candid note about mechanical failures. Goodman et al. (2014) compress the entire method into a single dense paragraph inside the "GPR Survey" narrative and lean on cited references for the "why."

&nbsp;&nbsp;&nbsp;&nbsp;Generally the writing logic is the same in all three. The section names the acquisition geometry first, then the instrument, then the processing chain, and it is honest about what was not done and why. In this case the reusable move is to describe the procedure as a completed, chronological pipeline in the passive voice, and to justify each choice with physical reasoning rather than silence. That's why the section reads as a narrated workflow, not a bullet dump.

## When to write / what belongs here

&nbsp;&nbsp;&nbsp;&nbsp;Write this section after the Site/Setting section and before Results. It belongs here whenever the reader needs to know how the data were collected and reduced before they can trust a result. This template is the umbrella "Methods" section. The finer detail of acquisition parameters lives in `06_data_acquisition.md`, the processing chain lives in `07_processing.md`, and any displayed formulas live in `08_equations_math.md`. So keep this file as the high-level scaffold that points into those three, and do not duplicate the survey-parameters table or the equation blocks here.

What belongs here:
- A one-sentence statement of the overall survey strategy and its objective.
- Instrument and system identification (make, model, antenna).
- Acquisition geometry (line spacing, direction, marker interval) at summary level.
- The processing chain named in order.
- An explicit statement of what was not done and why.
- Software and version used to generate the results.

## Recommended paragraph flow

1. State the overall survey strategy and its objective in one sentence, tying it to the archaeological question.
2. Describe acquisition geometry (survey pattern, line spacing, and the rationale for that spacing).
3. Identify the instrument and system (make, model, antenna frequency, aperture).
4. Name the processing chain in the order performed, one operation after another.
5. State explicitly what was not done (migration, deconvolution, or similar) and justify it with physical reasoning.
6. Close with the software and version used, plus any calibration or cross-validation against an independent measurement.

## Fill-in skeleton

&nbsp;&nbsp;&nbsp;&nbsp;`{{Data type, e.g. Radar profiles}}` were collected in a `{{pattern, e.g. zig-zag / parallel}}` direction across the survey grid at `{{site name}}`. The interval chosen between profiles was `{{value + unit}}`, which was believed sufficient to map `{{target feature type}}`. `[Instruction: give the spacing rationale in the same sentence, the way all three papers tie spacing to the lateral extent of the suspected target.]`

&nbsp;&nbsp;&nbsp;&nbsp;A `{{frequency}}` MHz antenna `{{with aperture, if relevant}}` was used, recording to a `{{time window}}` ns range. `[Instruction: name the instrument make and model here if known; Dalan et al. always name make and model, Goodman papers often only the frequency.]` The data were later resampled to a constant `{{value}}` and `{{correction type(s)}}` were applied.

&nbsp;&nbsp;&nbsp;&nbsp;Processing included `{{flat list: dewow, time-zero, gain, bandpass filter, migration, Hilbert transform}}`. `[Instruction: for a compressed paper name each step without justifying it and cite a companion reference; for a full journal paper justify each step against the data problem it fixes, and cross-link to 07_processing.md.]`

&nbsp;&nbsp;&nbsp;&nbsp;`{{Processing step, e.g. Migration or deconvolution}}` was not applied to any of the data in this study. In part the reason is that `{{physical justification}}`. `[Instruction: keep this "what we did not do" statement. It is a genre marker of honesty and it sets up the interpretive caveats in Results.]`

&nbsp;&nbsp;&nbsp;&nbsp;All `{{output product}}` results were generated using `{{software name and version}}`. `[Instruction: name the software even if the target journal has no Data Availability statement.]`

## Expected scientific content

- Overall survey objective stated in method terms, tied to the archaeological question.
- Survey geometry (pattern, line spacing, marker interval) and the physical rationale for the spacing.
- Instrument identification: make, model, antenna frequency, aperture where relevant.
- Ground conditions that affect the survey (soil resistivity, moisture, topographic relief).
- The processing chain named in execution order.
- An explicit "what was not done, and why" statement with physical reasoning.
- Calibration constants or cross-validation against an independent lab or excavation measurement.
- Software name and version.

## Citation strategy

&nbsp;&nbsp;&nbsp;&nbsp;Generally cite where a method choice needs external backing, and stay silent where the choice is standard practice. In this case the density is low and clustered. Cite the originating paper for any named technique (for example the time-slice method to Goodman et al., 1995), cite a companion volume for a full derivation the reader can chase (as in Goodman and Piro, 2013), and self-cite the team's own prior work to show continuity rather than starting from scratch. Use in-text author-year refs `(Author et al., 2023)`, sentence-final, one citation per specific claim, and never stack citations for a general background sentence.

## Figure/table references typical here

&nbsp;&nbsp;&nbsp;&nbsp;Generally this section carries few figures of its own. Where a survey-parameters table is used, reference it here as Table 1 (see `06_data_acquisition.md` for the table template). A method-demonstration figure that pairs raw and corrected data is common, and a site or grid-layout map may be cross-referenced from the Site section. Refer to figures as "Figure N" spelled out in body text.

## Tense & voice guidance

&nbsp;&nbsp;&nbsp;&nbsp;Generally write Methods in the simple past, passive voice, since the procedure is a completed thing and the data are the grammatical subject. So prefer "Profiles were collected" over "we collected profiles." However, a general physical fact embedded inside the narration takes the present tense, as when a paper writes that radar waves transmitted from the antenna are not monofrequency signals. Throughout, avoid first person unless the target venue's house style invites it; the source papers use "we" only at moments of interpretive judgment, never for routine procedure.

## Common phrases / sentence openers

- "Radar profiles were collected in a zig-zag direction across the survey grids at each of the sites."
- "The interval chosen between profiles is normally based on the lateral extent of suspected structures."
- "Migration or deconvolution was not applied to any of the data in this study."
- "Radargram signal processes included dewowing, bandpass filtering, Kirchoff migration and Hilbert transform."
- "GPR surveys employing varying frequencies from 200, 270 and 500 MHz have been expedited."
- "All time slice results were generated using GPR-SLICE software."

## Quality checklist

- [ ] The overall survey objective is stated in one sentence and tied to the archaeological question.
- [ ] Instrument make, model, and antenna frequency are named.
- [ ] Line spacing is given with a rationale, not as a bare number.
- [ ] The processing chain is listed in the order performed.
- [ ] There is an explicit statement of what was not done and why.
- [ ] Software name and version are credited.
- [ ] The section is in simple past, passive voice, with no unjustified first person.
- [ ] No survey-parameters table or displayed equation is duplicated from the acquisition or equations templates.

## Short worked example

&nbsp;&nbsp;&nbsp;&nbsp;Radar profiles were collected in a parallel zig-zag direction across the survey grid at the example site. The interval between profiles was 0.5 m, which was believed sufficient to map the suspected buried moat walls. A 270 MHz antenna was used, recording to a 200 ns range in the highly resistive floodplain soils. The data were later resampled to a constant 50 scans per meter and static corrections were applied. Processing included dewow, time-zero alignment, a spreading-loss gain, bandpass filtering, and Kirchhoff migration. Deconvolution was not applied, because the complex dielectric permittivity of the site was not known and the broadband radar pulse is dispersive. All depth-slice results were generated using GPR-SLICE v7.0.
