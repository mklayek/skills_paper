_date: 2026-07-09_

# arch-paper — implementation notes

## How the templates were extracted

&nbsp;&nbsp;&nbsp;&nbsp;The backbone comes from three archaeological ground-penetrating-radar (GPR) papers in the Goodman lineage, read and analyzed by parallel `doc-reader` sub-agents. The first is Goodman, Nishimura and Rogers (1995), "GPR Time Slices in Archaeological Prospection", a short figure-heavy methods paper built around three parallel case studies. The second is Dalan, Bevan, Goodman et al. (2011), "The Measurement and Analysis of Depth in Archaeological Geophysics: Tests at the Biesterfeldt Site, USA", a long multi-technique field-comparison paper with mirrored Methods and Results. The third is Goodman, Higashi, Hongo and Nishimura (2014), "The Search for Subterranean Kofun Burial Chambers on the Island of Kyushu, Japan using Ground Penetrating Radar", a short figure-driven case-study chapter that carries the explicit five-tier evidentiary hierarchy.

&nbsp;&nbsp;&nbsp;&nbsp;Each paper was read verbatim by its own `doc-reader` agent, which produced a per-paper analysis covering section scheme, numbering, abstract style, the Methods and Results architecture, the interpretation approach, figure and table and equation usage, citation density, tense, voice, and how the discussion and conclusions were handled. So the raw material for the template was three independent structural readings rather than one summary.

## The multi-agent pipeline

&nbsp;&nbsp;&nbsp;&nbsp;The pipeline ran in three stages. The first stage fanned out three `doc-reader` agents in parallel, one per source paper, each returning a structured analysis. The second stage fed those three analyses into a synthesis step that produced `templates/master/comparison_report.md`, which holds the side-by-side comparison table, the common patterns that form the reusable backbone, the divergences and what drives them, the ranked best practices, the recommended canonical section order, and the venue-specific pitfalls to avoid. The third stage expanded the synthesis into the master template, the humanization gate, the one-page rules reference, and the 17 per-section files under `templates/sections/`.

&nbsp;&nbsp;&nbsp;&nbsp;The lead compiled the runnable skill last, once the templates were stable, so the skill points at files that already exist and match the section map. The skill is the entry point, and the templates are the reference layer it dispatches to.

## Design decisions

&nbsp;&nbsp;&nbsp;&nbsp;The single most important decision was to make the five-tier evidentiary hierarchy the interpretive spine. All three source papers grade their confidence language, and Paper 3 makes the tiers explicit. Lifting that into a hard rule, where the hedging verb carries the tier and Tier 1 language can never attach to a Tier 4 or Tier 5 anomaly, gives the skill its main guard against overclaiming.

&nbsp;&nbsp;&nbsp;&nbsp;A second decision was to fuse results with interpretation rather than defer all interpretation to a standalone block, because none of the three papers separates them and raw geophysical values are uninformative without immediate archaeological context. The skill keeps the light gloss in Results and the disciplined tier work in Section 6, so a gloss never hardens into a confirmed claim.

&nbsp;&nbsp;&nbsp;&nbsp;A third decision was to default to a headed Methods section with explicit acquisition, processing, and depth-conversion subsections, even though Paper 1 buries Methods in the Introduction. That 1990s short-paper convention is a pitfall for a modern journal, so the backbone corrects it. The skill also presents at least the depth relation and the velocity-from-permittivity relation as displayed equations, even though all three source papers avoid equations, because a methods-contribution paper aimed at a geophysics audience needs them.

&nbsp;&nbsp;&nbsp;&nbsp;A fourth decision was the `Yet to be developed` placeholder rule. Rather than inventing plausible site data to fill a gap, the skill leaves the gap visible and verbatim, which keeps the draft auditable and honest. The humanization gate was made a hard per-sentence check rather than a soft style note, because uniform sentence shape and model tells like em dashes are the clearest signature of machine text.

&nbsp;&nbsp;&nbsp;&nbsp;A final decision was to stamp every generated document with the current date on line one and the default author block immediately below it. That makes each draft self-identifying and carries the lab attribution without the user restating it every time.

## How to extend

&nbsp;&nbsp;&nbsp;&nbsp;To add a source paper, run a fresh `doc-reader` agent over it with the same per-paper analysis prompt, then fold its structural findings into `templates/master/comparison_report.md` by updating the comparison table, the common patterns, and the divergences. Where the new paper introduces a device the backbone lacks, add it to the ranked best-practices list and, if it changes the interpretive discipline, revise the five-tier table in the master template and in the skill. Keep the three existing analyses intact, because the backbone is a synthesis and dropping a source weakens it.

&nbsp;&nbsp;&nbsp;&nbsp;To add a section, create a new `templates/sections/NN_*.md` file that opens with a `_Template date: YYYY-MM-DD_` line and a `# Section — template` heading, matching the existing 17 files. Then add a row to the section map in `SKILL.md` and in `templates/skill/arch-paper.md`, and insert the heading into the canonical order and the copy-paste skeleton in `templates/master/MASTER_TEMPLATE.md`. Give the new section a tense and voice entry in the tense table so the generator knows how to write it. So a new section is wired in at four places, which are the section file, the two section maps, and the master skeleton.

&nbsp;&nbsp;&nbsp;&nbsp;To tune the humanization gate, edit `templates/master/humanization_integration.md`, which is the single source for the enforceable per-sentence rules. The quick inline copy in `SKILL.md` and the expanded copy in `templates/skill/arch-paper.md` should be kept in step with it. Any new rule should carry a one-line rationale and, where useful, a before/after rewrite example in the same style as the existing three.
