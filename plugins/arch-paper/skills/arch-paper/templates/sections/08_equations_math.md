_Template date: 2026-07-09_

# Equations and Mathematics — template

## Purpose & writing logic

&nbsp;&nbsp;&nbsp;&nbsp;This section is where the paper presents the GPR depth, velocity, and time-slice mathematics: how each relation is written, numbered, defined, and tied to the processing chain. The honest finding across the three source papers is that none of them display a single numbered equation. Goodman et al. (1995) give velocity as a bare value, "a nominal velocity of 5 cm ns," and leave the depth relation implicit. Dalan et al. (2011) state one velocity, "an estimated microwave velocity of 7 cm ns was measured," with no derivation, and outsource all modeling math to cited programs. Goodman et al. (2014) name inverse-distance gridding and Kirchhoff migration only as terms.

&nbsp;&nbsp;&nbsp;&nbsp;Generally the writing logic for a compressed case-study is citation-as-definition: name the operation, cite the fuller source, and report only inputs and outputs. However, a full journal Methods section should make the core relations explicit. In this case the reusable move is to present each equation on its own line in `$$...$$`, number it with `\tag`, define every symbol immediately after, and tie the equation to the processing step it powers. That's why this template supplies ready LaTeX templates the source papers omit, clearly flagged as an enhancement over what the originals show.

## When to write / what belongs here

&nbsp;&nbsp;&nbsp;&nbsp;Write this inside or immediately after the Processing section, wherever a quantitative relation is first used. It belongs here whenever the paper converts travel time to depth, estimates velocity from a hyperbola, or defines the amplitude quantity mapped in a time slice. For a short proceedings chapter you may skip displayed equations entirely and cite the method source instead, exactly as all three papers do. For a full journal article, present at least the two-way travel time, the velocity-from-permittivity, and the depth relations explicitly.

What belongs here:
- Two-way travel time and its relation to depth.
- Velocity from dielectric permittivity.
- Velocity estimated from a diffraction hyperbola.
- The depth-slice amplitude quantity.
- Any interpolation or gridding weight used, if made explicit.

## Recommended paragraph flow

1. Introduce the physical quantity being defined and why it matters for interpretation.
2. Present the equation on its own line, numbered with `\tag`.
3. Define every symbol immediately after the equation, in order of appearance.
4. State the value or range used in this study and where it came from.
5. Tie the equation to the processing step it powers and note any assumption or limitation.

## Fill-in skeleton with ready LaTeX templates

&nbsp;&nbsp;&nbsp;&nbsp;`[Instruction: each equation goes on its own line in a $$...$$ block with a blank line above and below. Keep the \tag number inside the block. Define symbols in the sentence right after. Inline symbols use single $...$.]`

Two-way travel time to depth, given a velocity:

$$ d = \frac{v\,t}{2} \tag{1} $$

&nbsp;&nbsp;&nbsp;&nbsp;where $d$ is the reflector depth, $v$ is the radar wave velocity in the ground, and $t$ is the two-way travel time. `[Instruction: state the velocity value used and cross-reference the processing section.]`

Radar velocity from the relative dielectric permittivity:

$$ v = \frac{c}{\sqrt{\varepsilon_r}} \tag{2} $$

&nbsp;&nbsp;&nbsp;&nbsp;where $c \approx 0.3\ \text{m/ns}$ is the speed of light in vacuum and $\varepsilon_r$ is the relative dielectric permittivity of the soil. `[Instruction: give the assumed or measured $\varepsilon_r$ and note that it varies with moisture, per Dalan et al. (2011).]`

Velocity estimated from the asymptotes of a diffraction hyperbola:

$$ v = \frac{2\,x}{\sqrt{t^{2} - t_{0}^{2}}} \tag{3} $$

&nbsp;&nbsp;&nbsp;&nbsp;where $x$ is the horizontal offset from the hyperbola apex, $t$ is the two-way time at offset $x$, and $t_{0}$ is the apex two-way time. `[Instruction: state that the hyperbola was fitted to a point-source diffraction on a radargram, the method both Goodman papers reference without writing this formula.]`

Combined depth directly from time and permittivity:

$$ d = \frac{c\,t}{2\sqrt{\varepsilon_r}} \tag{4} $$

&nbsp;&nbsp;&nbsp;&nbsp;where the symbols are as defined above. `[Instruction: use this when you want a single depth expression that folds in the permittivity, rather than a separate velocity step.]`

The depth-slice amplitude quantity (averaged squared amplitude within a window):

$$ A(x,y,z) = \frac{1}{n}\sum_{i=1}^{n} a_i^{2} \tag{5} $$

&nbsp;&nbsp;&nbsp;&nbsp;where $A(x,y,z)$ is the mapped slice amplitude at position $(x,y)$ and depth $z$, $a_i$ is the sampled reflection amplitude within the spatial and depth window, and $n$ is the number of samples in that window. `[Instruction: this is the explicit form of the "average squared amplitude" the 1995 paper defines only in prose; present it for a full journal Methods section.]`

Inverse-distance-weighted gridding weight, if made explicit:

$$ w_i = \frac{1}{r_i^{\,p}} \tag{6} $$

&nbsp;&nbsp;&nbsp;&nbsp;where $w_i$ is the weight of sample $i$, $r_i$ is its distance to the grid node, and $p$ is the weighting exponent (the source papers use $p = 2$). `[Instruction: include only if the gridding scheme is discussed quantitatively; otherwise name it in the processing text and cite the algorithm.]`

## Expected scientific content

- The depth relation $d = v t / 2$, numbered and defined.
- The velocity-from-permittivity relation $v = c / \sqrt{\varepsilon_r}$.
- The hyperbola velocity estimate, tied to a fitted diffraction.
- The depth-slice amplitude definition.
- The stated velocity value and its origin (nominal, hyperbola-fitted, or lab-measured).
- The assumed permittivity and a note that it varies with moisture.
- Any gridding weight, if made explicit.

## Citation strategy

&nbsp;&nbsp;&nbsp;&nbsp;Generally cite the source of any relation you name but do not derive, and outsource forward or inverse modeling math to the cited program. In this case cite a standard geophysics text for the velocity-permittivity and travel-time relations (for example Telford et al. or a GPR methods text), cite the time-slice amplitude definition to Goodman et al. (1995), and cite the external modeling program where the deeper math lives, the way Dalan et al. (2011) cite Won and Bevis (1987) and Blakely (1995). Use author-year in-text refs `(Author et al., 2023)`, and place equations in `$...$` and `$$...$$` only.

## Figure/table references typical here

&nbsp;&nbsp;&nbsp;&nbsp;A radargram showing the fitted diffraction hyperbola used for the velocity estimate is the typical figure here. A velocity or permittivity table may accompany a multi-site study. Refer to figures as "Figure N" spelled out in body text.

## Tense & voice guidance

&nbsp;&nbsp;&nbsp;&nbsp;Generally state the relations in the present tense, since an equation is a standing physical fact, so write "depth is given by." However, the specific value used in this study takes the simple past, as in "a velocity of 7 cm/ns was estimated." Throughout, keep the voice impersonal and let the symbols carry the subject.

## Common phrases / sentence openers

- "A nominal velocity of 5 cm ns was used first to correct the radargrams for topography over the profiles."
- "Depth calibration for the site was estimated by matching to a faint hyperbola seen on one of the radargrams."
- "An estimated microwave velocity of 7 cm ns was measured."
- "Averages of the squared amplitude of the reflected radar signal over a horizontal spatial window and a vertical time (depth) window were used as the time slice parameter to be mapped."
- "The mathematics for aperture dispersion has still to be addressed."

## Quality checklist

- [ ] Every displayed equation is in a `$$...$$` block with a `\tag` number and blank lines around it.
- [ ] Every symbol is defined immediately after the equation it appears in.
- [ ] Inline symbols use `$...$`, not bare text.
- [ ] The stated velocity value and its origin (nominal, hyperbola, or lab) are given.
- [ ] The permittivity assumption is stated, with a moisture caveat.
- [ ] Each equation is tied to the processing step it powers.
- [ ] Any relation named but not derived carries a citation.
- [ ] Relations are in present tense; the study-specific value is in past tense.

## Short worked example

&nbsp;&nbsp;&nbsp;&nbsp;Radar wave velocity in the ground follows from the relative dielectric permittivity:

$$ v = \frac{c}{\sqrt{\varepsilon_r}} \tag{2} $$

&nbsp;&nbsp;&nbsp;&nbsp;where $c \approx 0.3\ \text{m/ns}$ and $\varepsilon_r$ is the soil permittivity. For the moderately dry silt at this site, $\varepsilon_r$ was taken as about 9, giving $v \approx 0.1\ \text{m/ns}$, which agreed with a value estimated independently by fitting a diffraction hyperbola on one radargram. Reflector depth then follows from the two-way travel time:

$$ d = \frac{v\,t}{2} \tag{1} $$

&nbsp;&nbsp;&nbsp;&nbsp;where $t$ is the two-way time to the reflector. Using this relation, the chamber-ceiling reflection at a two-way time of 50 ns maps to a depth of about 2.5 m, consistent with the depth later confirmed by excavation. The quantity mapped in each time slice was the averaged squared amplitude within a 30 cm depth window, computed as in equation (5).
