# Title page + Table of Contents (seismo-report)

_The report opens with a formal centered title page, then a Table of Contents. The author block is fixed and always present unless the user overrides it. Insert project info and version when supplied; the confidentiality line is optional._

## Title page (copy-paste, replace {{...}})

```
# Title Page

<div align="center">

&nbsp;

**{{Auto-generated report title: study type, key result, region/event, frequency band}}**

&nbsp;

_A scientific interpretation report_

_{{purpose line, e.g. prepared for research documentation and as the basis of a future journal manuscript}}_

&nbsp;

_By_

**DR. MRINAL KANTI LAYEK**

Postdoctoral Researcher | 박사후 연구원

&nbsp;

<img src="figs/logo_cnu.png" width="150" alt="institution logo">

&nbsp;

**Geophysics & AI Lab, Department of Energy & Resources Engineering**

**Chonnam National University, Gwangju, Republic of Korea [61186]**

지구물리 및 인공지능 연구실, 에너지자원공학과, 전남대학교, 광주광역시, 대한민국 [61186]

Email — layek.mk@gmail.com  ·  github.com/mklayek

&nbsp;

{{Project: <name/number> — include only if provided}}

**{{YYYY-MM-DD}}**  ·  Document version {{v1.0}}

{{Confidentiality: <statement> — optional}}

</div>

<div style="page-break-after: always;"></div>
```

## Table of Contents

```
# Table of Contents

&nbsp;&nbsp;&nbsp;&nbsp;{{The contents table below is generated automatically on export (`--toc`); this heading and note are the only placeholder needed in the Markdown master.}}

<div style="page-break-after: always;"></div>
```

## Notes
The title stays bold, the purpose lines italic, the author in bold capitals with the role line under it, then the logo, then the institution block in bold with the Korean affiliation line, then the email and GitHub, then optional project info, the date, and the version. The Korean lines render with an East-Asian font on DOCX and xelatex export (see `formatting_spec.md`).
