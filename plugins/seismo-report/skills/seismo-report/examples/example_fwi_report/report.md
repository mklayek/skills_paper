2026-08-05
Author: Dr. Mrinal Kanti Layek
Geophysics & AI Lab, Department of Energy & Resources Engineering, Chonnam National University, Gwangju, Republic of Korea [61186]

<!-- seismo-report worked example: report type FWI results (per templates/report_type_classifier.md). Emphasized chapters are Mathematical Background, Methodology, Results, Interpretation, Validation; this short worked example carries only Title Page, Table of Contents, Executive Summary, Results, and References to demonstrate the build pipeline end to end. -->

# Title Page

<div align="center">

&nbsp;

**Full-Waveform Inversion Velocity Models of the Southern Korean Peninsula (0.075 Hz)**

&nbsp;

_A scientific interpretation report_

_Prepared for research documentation and as the basis of a future journal manuscript_

&nbsp;

_By_

**DR. MRINAL KANTI LAYEK**

Postdoctoral Researcher | 박사후 연구원

&nbsp;

**Geophysics & AI Lab, Department of Energy & Resources Engineering**

**Chonnam National University, Gwangju, Republic of Korea [61186]**

지구물리 및 인공지능 연구실, 에너지자원공학과, 전남대학교, 광주광역시, 대한민국 [61186]

Email — layek.mk@gmail.com  ·  github.com/mklayek

&nbsp;

Project: FWI0075 3-D southern-peninsula velocity model

**2026-08-05**  ·  Document version v1.0

</div>

<div style="page-break-after: always;"></div>

# Table of Contents

&nbsp;&nbsp;&nbsp;&nbsp;{{The contents table below is generated automatically on export (`--toc`); this heading and note are the only placeholder needed in the Markdown master.}}

<div style="page-break-after: always;"></div>

# Executive Summary

&nbsp;&nbsp;&nbsp;&nbsp;This report interprets one iteration of a three-dimensional full-waveform inversion (FWI) run over the southern Korean Peninsula, driven by a 0.075 Hz low-pass observation band. The inverted grid recovers a P-wave velocity ($V_p$) structure spanning 5.85 to 6.48 km/s and an S-wave velocity ($V_s$) structure spanning 3.27 to 3.85 km/s across the model domain. Generally, the fast, high-$V_p$ blocks track the basement highs beneath the peninsula, and the coupled $V_p$-$V_s$ pattern points to a lithology-driven rather than a fluid-driven origin for the strongest anomalies. The main figure of this short example, the model-grid panel, carries the full three-dimensional context needed to read that pattern.

# Results

![Figure 1. Three-dimensional FWI model grid over the southern Korean Peninsula at 0.075 Hz, showing the P-wave velocity ($V_p$) and S-wave velocity ($V_s$) panels side by side. The recovered range is Vp 5.85 to 6.48 km/s and Vs 3.27 to 3.85 km/s across the inverted domain.](figs/fig1_model_grid.png)

&nbsp;&nbsp;&nbsp;&nbsp;Figure 1 shows the recovered $V_p$ and $V_s$ grids from the 0.075 Hz FWI run side by side over the same three-dimensional domain, and the two panels track each other closely rather than diverging, which is the first sign that the update is a genuine lithology signal and not an artifact of one wave type alone. The $V_p$ panel ranges from 5.85 to 6.48 km/s and the $V_s$ panel from 3.27 to 3.85 km/s, and the ratio between the two stays close to the crustal average through most of the volume, so the elevated blocks read as denser or more competent crustal material rather than as a fluid-saturated zone, since a fluid-driven anomaly would depress $V_s$ more sharply than $V_p$ and break that ratio. The fastest material sits where the grid samples the shallow basement highs beneath the peninsula, which is consistent with the outcrop geology in that part of the domain, and the slower material collects along the sediment-filled basins, where the softer, less consolidated section is expected to slow both wave types together. Throughout the volume the update pattern looks smooth rather than blocky, which is a resolution signature. It shows the inversion had enough wavefield illumination at 0.075 Hz to recover long-wavelength structure cleanly, though it also means that any sharp, sub-wavelength boundary in the true model is smeared across several grid cells in this single-band result. In this case the single low-frequency band cannot by itself resolve fine layering, so a multi-scale run that adds progressively higher frequency bands would sharpen the boundaries that this 0.075 Hz result only outlines. So the headline result of this chapter is that the coupled $V_p$-$V_s$ pattern is physically consistent, spatially coherent with known basement structure, and limited in resolution by the single frequency band used to produce it.

# References

&nbsp;&nbsp;&nbsp;&nbsp;{{Author-date, alphabetical, real works only. If no references are available, this chapter reads Yet to be developed.}}

Yet to be developed
