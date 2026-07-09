_date: 2026-07-09_

# arch-paper — usage guide

## What this skill does

&nbsp;&nbsp;&nbsp;&nbsp;The `arch-paper` skill turns raw survey project info into a dated, house-style archaeological GPR manuscript skeleton, then populates the sections you have data for and marks the rest `Yet to be developed`. It enforces the Goodman-lineage backbone, the five-tier interpretation discipline, and the humanization gate on every sentence. The output always opens with the current date and the default author block.

## How to invoke

&nbsp;&nbsp;&nbsp;&nbsp;Trigger the skill by asking for an archaeological GPR paper or section in plain language. The skill fires on phrases such as "draft an archaeological GPR paper", "write the interpretation section for my time-slice survey", "structure a manuscript on a buried moat from these results", or "generate a full paper skeleton from my project info". Hand it whatever project info you have. Missing fields are fine and become placeholders rather than blocking the draft.

&nbsp;&nbsp;&nbsp;&nbsp;The fields that most help the generator are the site name and location, the antenna frequency, the survey grid and line spacing, the target features, the key results with at least one quantified value, the validation status of each anomaly, and the list of available figures and tables. Give the validation status per anomaly so the interpretation generator can pick the right evidentiary tier and the matching hedge.

## Example project-info input

&nbsp;&nbsp;&nbsp;&nbsp;A minimal input looks like the block below. The user pastes this, and the skill maps each field onto the manuscript skeleton.

```
Site: Riverbank mound, a river floodplain (generic example site)
Antenna: 400 MHz shielded, GSSI SIR-3000
Grid: 40 m by 30 m, 0.5 m line spacing, bidirectional
Targets: buried brick chamber, a possible moat trace
Velocity: 0.10 m/ns from a hyperbola fit
Results: bright 4 by 3 m rectangular anomaly at ~1.2 m depth (excavated, brick floor recovered);
         a linear low-amplitude trace along the north edge (no dig)
Figures available: regional context map, depth-slice at 1.2 m, excavation photo
Validation: chamber excavation-confirmed; moat trace has spatial coherence only
```

## Example generated dated skeleton (first ~40 lines)

&nbsp;&nbsp;&nbsp;&nbsp;From that input the skill emits a document that begins as follows. The date line comes first, the author block follows, and each section is either populated or marked `Yet to be developed`.

```
2026-07-09

Author: Mrinal Kanti Layek
Affiliation: Geophysics & AI Lab, Department of Energy & Resources Engineering,
Chonnam National University, Gwangju, Republic of Korea [61186]
(Korean: 지구물리 및 인공지능 연구실, 에너지자원공학과, 전남대학교, 광주광역시, 대한민국 [61186])
Email: layek.mk@gmail.com

# Ground-Penetrating Radar Depth-Slice Imaging of a Buried Brick Chamber at a Riverbank Mound

**Authors:** Mrinal Kanti Layek^1
**Keywords:** archaeological prospection, buried brick chamber, ground-penetrating radar, time-slice imaging, river floodplain

## Abstract
Yet to be developed

## 1. Introduction
    The river floodplain around the study region carries a dense record of early historic settlement, and much of it lies buried under later alluvium. The example mound preserves a brick structure whose plan was unknown before this survey, which is the knowledge gap the work addresses. Ground-penetrating radar (GPR) offers a non-invasive way to recover that plan before any excavation. So this paper reports a 400 MHz depth-slice survey of the mound, defines the recurring feature vocabulary of chamber and moat trace in context, and closes on what the imaged plan means for the site chronology.

## 2. Study Area and Archaeological / Historical Context
    The example mound sits on the left bank of a river (Figure 1). Yet to be developed

## 3. Geological and Site Setting
    The near-surface section is fine alluvial silt, which holds moisture and lowers radar velocity where the water table rises. Yet to be developed

## 4. Materials and Methods

### 4.1 Data Acquisition
    A 400 MHz shielded GSSI SIR-3000 antenna was used over a 40 m by 30 m grid at 0.5 m line spacing, collected bidirectionally.
```

&nbsp;&nbsp;&nbsp;&nbsp;The interpretation section for this input would state the excavated 4 by 3 m anomaly plainly, because it is Tier 1, and would place the north-edge linear trace on Tier 4 or Tier 5 with a hedge such as "may correspond to a moat trace" or "tentatively", because it has spatial coherence only. That is the discipline the tier rule enforces.

## Tips

&nbsp;&nbsp;&nbsp;&nbsp;Give the velocity and its origin whenever you have them, because the depth-conversion subsection needs the value to state the depth relation with a real number rather than a placeholder. State the validation status per anomaly so the tier is chosen correctly. Where you have no data for a section, leave it out of the input and let the skill mark it `Yet to be developed` rather than supplying a guess.
