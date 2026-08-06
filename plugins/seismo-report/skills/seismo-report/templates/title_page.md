# Title page (seismo-report) — image-style, logos + numbered affiliations

_The report opens with a formal, vertically-distributed title page: institution logo(s) at
the top, the title and subtitle in the upper-middle, and the author + numbered affiliations +
date at the bottom (the classic academic title-page layout). It is authored ONCE as an HTML
`<div class="titlepage">` block that the web-style HTML (`report_web.css`) lays out as a full
page; the PDF build replaces it with `scripts/titlepage.tex` (a LaTeX `titlepage` placed before
the Table of Contents). Do NOT keep a `# Title Page` heading — the title page is not a TOC entry,
and no stray date line should precede it._

## HTML title page (copy-paste at the very top of the master, before `# Abstract`)

```
<div class="titlepage">
<div class="tp-top">
<div class="tp-logos">
<img class="tp-logo" src="figs/logo_cnu.png" alt="Chonnam National University">
<img class="tp-logo" src="figs/logo_cwnu.png" alt="Changwon National University">
</div>
</div>
<div class="tp-mid">
<div class="tp-title">{{Auto-generated report title: study type, key result, region/event}}</div>
<div class="tp-sub">{{subtitle, e.g. Vp and Vs Models Constrained by the 2016 Gyeongju and 2017 Pohang Earthquake Sequences}}</div>
<div class="tp-desc">A scientific interpretation report<br>{{purpose line}}</div>
</div>
<div class="tp-bot">
<div class="tp-author">Dr. Mrinal Kanti Layek<sup>1,2</sup></div>
<div class="tp-aff"><span class="tp-aff-n">1</span> Postdoctoral Researcher (박사후 연구원), Geophysics &amp; AI Lab, Department of Energy &amp; Resources Engineering, Chonnam National University, Gwangju, Republic of Korea [61186]<br>
지구물리 및 인공지능 연구실, 에너지자원공학과, 전남대학교, 광주광역시, 대한민국 [61186]</div>
<div class="tp-aff"><span class="tp-aff-n">2</span> Brain-Pool (BP) Researcher, Earthquake Engineering and Seismic Hazard Laboratory, Department of Civil Engineering, Changwon National University (CWNU), 20 Changwondaehak-Ro, Uichang-Gu, Changwon-Si, Gyeongsangnam-Do 51140, South Korea</div>
<div>layek.mk@gmail.com &nbsp;&middot;&nbsp; github.com/mklayek</div>
<div class="tp-date">{{YYYY-MM-DD}} &nbsp;&middot;&nbsp; Document version {{v1.0}}</div>
</div>
</div>
```

The `.titlepage` / `.tp-*` styles live in `scripts/report_web.css`. Logos go in `figs/`
(`logo_cnu.png`, `logo_cwnu.png`); if a logo is missing, omit its `<img>` — never point at a file
that does not exist. When the author has a single affiliation, drop the `<sup>1,2</sup>` markers
and the second `.tp-aff` line.

## PDF title page

The PDF build (see `scripts/build_report.py to_pdf` / `templates/formatting_spec.md`) strips the
`<div class="titlepage">` block and everything before `# Abstract`, then injects
`scripts/titlepage.tex` with `pandoc --include-before-body=titlepage.tex` so the LaTeX
`titlepage` (logos via `\includegraphics`, title, and the numbered `\textsuperscript{1,2}`
affiliations) renders as page 1, before the auto Table of Contents. Suppress LaTeX's auto figure
label with `\captionsetup{labelformat=empty}` so captions read as "Fig. N." only.

## Fixed author block (both affiliations)

```
Dr. Mrinal Kanti Layek
1  Postdoctoral Researcher | 박사후 연구원, Geophysics & AI Lab, Department of Energy & Resources
   Engineering, Chonnam National University, Gwangju, Republic of Korea [61186]
   지구물리 및 인공지능 연구실, 에너지자원공학과, 전남대학교, 광주광역시, 대한민국 [61186]
2  Brain-Pool (BP) Researcher, Earthquake Engineering and Seismic Hazard Laboratory, Department of
   Civil Engineering, Changwon National University (CWNU), 20 Changwondaehak-Ro Uichang-Gu
   Changwon-Si, Gyeongsangnam-Do 51140, South Korea
Email — layek.mk@gmail.com  ·  github.com/mklayek
```

## Notes
The title is bold and centered, the subtitle italic, the author in bold with superscript
affiliation numbers, each numbered affiliation below it, then email/GitHub, then the date and
version. The Korean lines render with an East-Asian font on DOCX and xelatex export (xeCJK /
Malgun Gothic — see `formatting_spec.md`). The Table of Contents is generated automatically on
export (`--toc`); do not add a manual "Table of Contents" section for the web-style HTML or PDF.
