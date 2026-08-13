_Template date: 2026-07-09_

# Acknowledgements & Supplementary Material — template

## Purpose & writing logic

    The Acknowledgements section credits the people, institutions, funding, and tools that made the fieldwork and analysis possible but do not rise to authorship. The three source papers span the full range of what this section can be. Goodman et al. (1995) used two short paragraphs: named municipal and museum contacts who enabled site access, then a software-attribution sentence with a copyright line. Dalan et al. (2011), a nine-author collaboration, ran an unusually long and specific acknowledgement, crediting the funding agreement, property access, logistical help down to who mowed the site, the training-workshop context, and a full roll-call of student assistants by name and contribution. Goodman et al. (2014) collapsed the whole section to a single sentence crediting only the processing software.

    The writing logic is proportional and concrete. Credit scales with the size and complexity of the collaboration. Name specific individuals and their specific roles rather than thanking "the many people who helped." Two conventions recur across all three papers and should be preserved: an explicit software or tool attribution sentence (functioning as a reproducibility disclosure, since these papers predate formal Data Availability statements), and named local or site-authority contacts who granted access.

## When to write / what belongs here

    Write the Acknowledgements near the end, once the author list and figure credits are final, so you can be sure a contributor belongs here rather than in the byline. What belongs here: funding source or cooperative agreement, property owner or heritage authority who granted access and permits, logistical and field support (crews, drivers, equipment loans, site preparation), the workshop or training-course context if the data originated there, named credit for a figure or dataset compiled by a student or junior collaborator, and the named processing or acquisition software with version and, if proprietary, its copyright line. Supplementary material, where the venue supports it, belongs alongside: extended data tables, full anomaly catalogues, additional depth-slice panels, GPX or geodata files, and processing scripts, each pointed to from the main text.

    What does not belong: anyone who meets authorship criteria (they go in the byline), and vague blanket thanks.

## Fill-in skeleton

Acknowledgements:

```
{{Funding / origin sentence}}
Work at the {{site name}} was {{stimulated / supported / funded}} by {{funding body or cooperative agreement}} {{and the context that generated it, e.g., an NPS training course}}.

{{Access / permission sentence}}
Permission to work at the site was graciously provided by {{property owner or heritage authority}}.

{{Logistical / field support sentence}}
{{Concrete support, e.g., site mowing / equipment / transport}} was provided by {{named individuals}}. {{Named individual}} of {{institution or town}} and {{named individual}} from {{institution or town}} assisted in coordinating and supporting this research.

{{Named figure / dataset credit sentence}}
The {{map / dataset}} was assembled by {{name}} ({{role, e.g., MSUM undergraduate student}}) from data collected during {{campaign}}.

{{Software / tool attribution sentence}}
All {{product, e.g., depth-slice}} results were generated using {{software name and version}} ({{Copyright year, developer or lab}}).
```

Supplementary material (if the venue supports it):

```
Supplementary material available online:
- Table S{{n}}: {{full anomaly catalogue / complete survey-parameter listing}}
- Figure S{{n}}: {{additional depth-slice panels / uncropped radargrams}}
- Data S{{n}}: {{GPX tracklogs / GeoJSON / KML exports / processing scripts}}
```

    Inline instruction: name individuals with their role or institution. Keep the software sentence even if the target journal has a separate Data Availability statement, because it also credits the tool. If proprietary software is used, include its copyright line as the source papers did (GPR-SLICE in all three). Point to every supplementary item from the main text at least once.

## Expected content

    A complete Acknowledgements section, sized to the collaboration, names the funding or project origin, the access and permit grantors, the logistical and field support with specific people and roles, any workshop or training context, named credit for figures or datasets produced by junior contributors, and the acquisition and processing software with version and copyright. A single-sentence software-only acknowledgement is acceptable for a compressed chapter (Goodman et al., 2014); a full journal paper with a large team warrants a paragraph with a named roll-call (Dalan et al., 2011). Supplementary material, when present, is listed with stable labels (Table S1, Figure S1, Data S1) and each item is referenced from the body.

## Style / format rules

- Name specific individuals and their specific roles, not blanket thanks.
- Always include a software or tool attribution sentence with version and, if proprietary, a copyright line.
- Credit scales with collaboration size: one sentence for a compressed chapter, a full paragraph with a roll-call for a large team.
- Anyone meeting authorship criteria goes in the byline, not here.
- Supplementary items get stable labels (Table S1, Figure S1, Data S1) and each is pointed to from the main text.
- Use US English. No em dashes (recast with a comma or a new sentence). Avoid semicolons; use separate sentences.
- First-line indent applies to the running prose of this section as to the rest of the body.

## Common phrases / real examples

- "The authors are grateful to Koji Tobita of the city of Nakajima Machi and to Katsumi Arita from Shintomi Machi for their efforts in coordinating and supporting this research study." (Goodman et al., 1995, named local contacts with roles)
- "All time slice results were generated using GPR-SLICE software (Copyright 1995, Geophysical Archaeometry Laboratory)." (Goodman et al., 1995, software attribution with copyright line)
- "Permission to work at the site was graciously provided by the Archaeological Conservancy." (Dalan et al., 2011, access and permission)
- "Site mowing was provided by Charles Rotenberger, Gordon Bergman and Kyle Kopacheck." (Dalan et al., 2011, concrete logistical support named individually)
- "The resistance map was assembled by Chrys Harris (MSUM undergraduate student) from data collected during MSUM Field Schools (2007 and 2008) and the NPS workshop." (Dalan et al., 2011, named figure credit)
- "GPR imaging and specialized vector imaging at Saitobaru National Kofun Burial Mounds were accomplished using GPR-SLICE v7.0 Software." (Goodman et al., 2014, single-sentence software-only acknowledgement)

## Quality checklist

- [ ] Funding source or project origin is named.
- [ ] Access, permit, or property-owner permission is credited to a named authority.
- [ ] Logistical and field support names specific individuals and their roles, not blanket thanks.
- [ ] An acquisition and processing software attribution sentence is present, with version and copyright line if proprietary.
- [ ] No one meeting authorship criteria appears here instead of in the byline.
- [ ] Section length is proportional to collaboration size.
- [ ] Supplementary items, if any, have stable labels and are each referenced from the main text.
- [ ] US English, no em dashes, no stray semicolons.

## Short worked example

```
Acknowledgements

    Fieldwork at Mound 12, Saitobaru, was supported by a cooperative agreement between the Saitobaru Archaeological Museum and the Geophysical Archaeometry Laboratory, and grew out of the 2015 regional prospection workshop. Permission to survey was graciously provided by the Miyazaki Prefecture heritage office. Site clearing and equipment transport were provided by Kenji Sato and Aiko Mori. The base site plan was assembled by Rei Tanaka (graduate assistant) from data collected during the 2014 and 2015 field schools. All depth-slice and isosurface results were generated using GPR-SLICE v7.0 software (Copyright 2015, Geophysical Archaeometry Laboratory).

Supplementary material available online:
- Table S1: complete anomaly catalogue for all surveyed mounds, with validation status.
- Figure S1: full depth-slice progression from 0.3 to 10.3 m for Mound 12.
- Data S1: georeferenced depth-slice rasters (GeoTIFF) and GPX tracklogs.
```
