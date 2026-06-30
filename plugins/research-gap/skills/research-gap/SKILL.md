---
name: research-gapmkl
description: Identifies research gaps from uploaded documents/links and generates novel research project proposals
type: skill
---

# Skill: research-gapmkl

## Purpose

Identify and formulate novel research ideas by analyzing existing literature and detecting potential research gaps. Operates on uploaded research materials such as PDF files, documents, or provided web links.

## When to Use

Use this skill when the user uploads research papers, provides research links, or asks for research gap analysis, literature review, or novel research idea generation.

## Workflow

1. **Document Analysis**: Extract and summarize main contributions, datasets, algorithms, and conclusions from provided documents
2. **Literature Search**: Search the internet for closely related studies, recent publications, and known limitations
3. **Gap Detection**: Compare uploaded material with the broader research landscape to identify:
   - Knowledge gaps
   - Unresolved problems
   - Methodological limitations
   - Unexplored application areas
4. **Idea Generation**: Propose a unique research idea based on the most promising gap
5. **Proposal Writing**: Generate a structured research proposal document

## Sub-Agents (Internal Coordination)

1. **Document Analysis Agent** — reads uploaded papers
2. **Literature Search Agent** — identifies related studies on the internet
3. **Research Gap Detection Agent** — synthesizes limitations and opportunities
4. **Research Proposal Generation Agent** — converts the detected gap into a structured plan

## Output Directory

All outputs organized inside `research_gap/` directory:

```
research_gap/
├── research_summary.md      # Analyzed papers, insights, and gaps
├── research_project.md      # Full structured proposal
└── abstract.md              # Standalone abstract
```

## Research Proposal Format

1. Abstract
2. Introduction
3. Background / Literature Review
4. Research Gap Identification
5. Proposed Methodology
6. Experimental Design / Data Strategy
7. Expected Results
8. Discussion and Potential Impact
9. Conclusion
10. Possible Future Work

## Critical Rules

- Always analyze provided documents thoroughly before searching for gaps
- Support findings with evidence from the literature
- Propose novel and feasible research directions
- Generate complete, structured proposal documents
