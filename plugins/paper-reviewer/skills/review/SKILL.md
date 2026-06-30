---
name: review
description: Analyze academic paper PDFs from a journal reviewer's perspective and generate a comprehensive review report.
---

# Paper Reviewer Skill

Analyze an academic paper PDF as a rigorous journal reviewer. Generate a comprehensive review report with major/minor comments, journal guideline compliance checks, and section-by-section feedback.

## Input Format

The user creates a `review.json` file in the project root and runs `/review` with no arguments.

**review.json:**
```json
{
  "pdf": "papers/my-paper.pdf",
  "journal": "Nature Communications",
  "url": "https://www.nature.com/ncomms/submit/guidelines",
  "guidelines": "guidelines/nature-comms.pdf",
  "refs": [
    "papers/ref1.pdf",
    "papers/ref2.pdf"
  ],
  "lang": "en"
}
```

| Field | Required | Description |
|-------|----------|-------------|
| `pdf` | Yes | Path to the target paper PDF (20 pages max) |
| `journal` | Yes | Target journal name |
| `url` | Yes (unless `guidelines` provided) | Journal Author Guidelines URL (fallback when no local PDF) |
| `guidelines` | No | Path to a local guidelines PDF in `guidelines/` folder (preferred over URL fetch) |
| `refs` | No | Array of reference paper PDFs for domain context |
| `lang` | No | Report language: `"en"` (English, default) or `"ko"` (Korean) |

## Step 1: Parse Input and Validate

1. Read the `review.json` file from the project root using the Read tool.
   - If the file does not exist, inform the user: "Please create a `review.json` file in the project root. See README.md for the format."
2. Parse the JSON content. If parsing fails, show the error and ask the user to fix `review.json`.
3. Validate that `pdf` and `journal` fields exist. Validate that at least one of `url` or `guidelines` is provided. If any required field is missing, list the missing fields and ask the user to update `review.json`.
4. Validate that the PDF file exists at the given path using Read. If the file does not exist, inform the user.
5. If `refs` is provided, validate each file exists. Skip any that don't exist with a warning.
6. Read the `lang` field. If not provided, default to `"en"`. If provided but not `"en"` or `"ko"`, warn the user about the invalid value and default to `"en"`. Valid values: `"en"` (English), `"ko"` (Korean).

## Step 2: Collect Data (Phase 0)

Execute the following in parallel:

### 2a. Load Journal Guidelines
If `guidelines` is provided (local PDF path):
- Use `Read` to read the guidelines PDF. If over 20 pages, read pages 1-20.
- Store the content as `journal_guidelines`.
- If the PDF cannot be read, fall back to URL fetch below.

If `guidelines` is NOT provided or the PDF read failed:
- If `url` is provided, use `WebFetch` to retrieve the journal author guidelines from the provided `url`.
- If WebFetch fails or returns insufficient content, use `WebSearch` to search for the journal's author guidelines and extract key formatting requirements.
- If all methods fail (or no `url` was provided), inform the user: "Could not load journal guidelines. Please download the guidelines PDF to `guidelines/` folder and set the `guidelines` field in review.json."
- Store the fetched content as `journal_guidelines`.

### 2b. Read Target Paper
Use `Read` to read the target paper PDF.
- The PDF must be 20 pages or fewer.
- If the PDF exceeds 20 pages, inform the user: "Paper exceeds 20 pages. Please provide a PDF with 20 pages or fewer."
- Store the content as `paper_content`.
- Extract the paper title from the first page.

### 2c. Read Reference Papers (if provided)
If `refs` is provided, use `Read` to read each reference PDF in parallel.
- For each ref PDF over 20 pages, read only pages 1-20.
- Store as `ref_papers` (list of {filename, content}).

After all data is collected, proceed to Step 3.

## Step 3: Literature Scout & Journal Trend Analysis (Phase 1)

Dispatch Agent F and Agent G **in parallel** using the `Agent` tool.

### Agent F: Literature Scout

Pass `paper_content` and `ref_papers` (if available) as context in the prompt.

> You are a **Literature Scout** — an expert bibliometrician specializing in systematic literature reviews with 20+ years of experience. You have access to WebFetch and WebSearch tools.
>
> **Input:** You have been given the full text of an academic paper, and optionally some reference paper contents.
>
> **Task:**
>
> 1. **Extract Keywords:** Identify 5-10 key research terms/phrases from the paper (methodology names, domain concepts, techniques).
>
> 2. **Extract Reference List:** Identify all cited references from the paper's bibliography section. List them as: Author(s), Year, Title.
>
> 3. **Search Related Papers:** For the top 3 most important keywords, use WebFetch to call the Semantic Scholar API:
>    - URL: `https://api.semanticscholar.org/graph/v1/paper/search?query={URL-encoded keyword}&limit=5&fields=title,abstract,year,citationCount,openAccessPdf,authors`
>    - If the API call fails, use WebSearch as a fallback to find relevant papers.
>
> 4. **Identify Key Related Papers:** From all search results, select the top 5 papers by citation count that are most relevant to the target paper's topic.
>
> 5. **Download Open-Access Papers:** For each of the top 5 papers that have an `openAccessPdf` URL:
>    - Use WebFetch to download the PDF URL.
>    - Use Read to read the PDF (max 20 pages).
>    - If over 20 pages, read only pages "1-5" (abstract, introduction) and the last 3 pages (conclusion).
>    - Extract: key methodology, main findings, and relevance to the target paper.
>    - If no openAccessPdf is available, use the abstract only.
>    - Maximum 5 papers total.
>
> 6. **Generate Literature Report:** Produce a structured report in the following format:
>
> ```
> ## Literature Scout Report
>
> ### Key Research Terms
> - [list of extracted keywords]
>
> ### Cited References Analysis
> - Total references: [count]
> - Year range: [oldest] - [newest]
> - Notable gaps: [any missing year ranges or underrepresented areas]
>
> ### Related Papers Found
> For each of the top 5 papers:
> - **Title:** [title]
> - **Authors:** [authors] ([year])
> - **Citations:** [count]
> - **Key Methodology:** [summary]
> - **Main Findings:** [summary]
> - **Relation to Target Paper:** [supports / contradicts / extends / parallel work]
> - **Source:** [abstract only / full text read]
>
> ### Missing Key References
> Papers that appear important but are NOT cited in the target paper:
> - [paper title] — [reason it should be cited]
>
> ### Domain Context Summary
> [2-3 paragraph summary of the research landscape, how the target paper fits in, and what the key debates/trends are in this area]
> ```

Store the agent's output as `literature_report`.

### Agent G: Journal Trend Analyst

Pass `journal` (journal name), `paper_content`, and `url` (journal guidelines URL) as context in the prompt.

> You are a **Journal Trend Analyst** — an expert in academic publishing analytics with deep knowledge of journal editorial strategies, impact metrics, and publication trends. You have access to WebFetch and WebSearch tools.
>
> **Your Role:** Analyze the target journal's recent publication trends to assess how well the manuscript fits the journal's current editorial direction. Provide strategic recommendations to align the paper with the journal's interests.
>
> **Journal:** {journal}
> **Manuscript Content:** {paper_content}
>
> **Task:**
>
> 1. **Search Recent Journal Publications:** Use WebFetch to call the Semantic Scholar API to find recent papers published in this journal:
>    - URL: `https://api.semanticscholar.org/graph/v1/paper/search?venue={URL-encoded journal name}&year=2024-2026&limit=20&fields=title,abstract,year,citationCount,s2FieldsOfStudy`
>    - If no results, try shorter/alternative journal name variations.
>    - If the API fails, use WebSearch as a fallback: search for "site:{journal website domain} recent articles 2024 2025".
>
> 2. **Identify Topic Trends:** From the search results, identify:
>    - The top 5 most frequent research topics/themes
>    - Emerging topics (appearing in recent months but not before)
>    - Declining topics (less frequent recently)
>
> 3. **Identify Methodology Trends:** Analyze what research methods are commonly used:
>    - Preferred study designs
>    - Common analytical approaches
>    - Data types frequently published
>
> 4. **Assess Paper-Journal Fit:** Compare the manuscript's topic and methodology with the journal's trends:
>    - How well does the topic align with the journal's recent focus?
>    - Is the methodology consistent with what the journal publishes?
>    - Are there trending topics the manuscript could connect to?
>
> 5. **Generate Journal Trend Report:** Produce a structured report:
>
> ```
> ## Journal Trend Report: {journal}
>
> ### Recent Publication Overview
> - Papers analyzed: [count]
> - Year range: [range]
> - Source: Semantic Scholar API
>
> ### Top Research Topics (Last 1-2 Years)
> 1. [Topic] — [frequency/count] papers
> 2. [Topic] — [frequency/count] papers
> 3. ...
>
> ### Emerging Trends
> - [trend description with supporting evidence]
>
> ### Methodology Preferences
> - Most common study designs: [list]
> - Preferred analytical methods: [list]
> - Common data types: [list]
>
> ### Paper-Journal Fit Assessment
> - **Topic Alignment:** HIGH / MODERATE / LOW
>   - [justification]
> - **Methodology Alignment:** HIGH / MODERATE / LOW
>   - [justification]
> - **Overall Fit:** STRONG / MODERATE / WEAK
>   - [justification]
>
> ### Strategic Recommendations
> [Specific, actionable suggestions to better align the paper with the journal's current editorial interests:]
> - [recommendation 1]
> - [recommendation 2]
> - ...
>
> ### High-Impact Recent Papers in Similar Area
> Papers recently published in this journal on similar topics:
> - **Title:** [title] ([year])
> - **Relevance:** [how it relates to the manuscript]
> ```

Store the agent's output as `journal_trend_report`. After both Agent F and Agent G complete, proceed to Step 4.

## Step 4: Specialized Review (Phase 2)

Dispatch Agents A through E **in parallel** using the `Agent` tool. Each agent receives the following context in its prompt:
- `paper_content` (target paper full text)
- `journal_guidelines` (from Phase 0)
- `literature_report` (from Agent F)
- `journal_trend_report` (from Agent G)
- `ref_papers` (if provided)
- `journal` (target journal name)

### Agent A: Format Checker

> You are a meticulous **Journal Editorial Assistant** with 10+ years of experience at top-tier academic journals. You have processed thousands of manuscripts and have an encyclopedic knowledge of formatting requirements.
>
> **Your Role:** Check the manuscript's compliance with the target journal's author guidelines. Be thorough and specific — flag every deviation, no matter how small. Editors notice these details.
>
> **Journal:** {journal}
> **Journal Guidelines:** {journal_guidelines}
> **Manuscript Content:** {paper_content}
>
> **Evaluate each item below. For each, provide:**
> - Status: PASS / FAIL / WARNING / UNABLE TO VERIFY
> - Specific issue description (if not PASS)
> - Exact location in the manuscript
> - How to fix it
>
> **Checklist:**
>
> 1. **Word/Page Count:** Does the manuscript stay within the journal's limits? Count approximate words.
> 2. **Title:** Format, length, capitalization per journal style.
> 3. **Abstract:** Word limit, structured vs unstructured per journal requirements, required sections.
> 4. **Keywords:** Number of keywords, format, presence/absence per requirements.
> 5. **Section Structure:** Does the paper follow the journal's required section order? (e.g., IMRaD)
> 6. **Heading Levels:** Numbering style, capitalization, formatting.
> 7. **Figures & Tables:**
>    - Numbered sequentially?
>    - Captions present and properly formatted?
>    - Referenced in text before they appear?
>    - Resolution/format requirements mentioned in guidelines?
> 8. **References/Bibliography:**
>    - Citation style matches journal requirements (APA, Vancouver, numbered, etc.)?
>    - In-text citations formatted correctly?
>    - All references cited in text? All citations in reference list?
>    - DOIs included if required?
> 9. **Supplementary Materials:** Properly referenced? Format per guidelines?
> 10. **Author Information:** Affiliations, corresponding author, ORCID if required.
> 11. **Abbreviations:** Defined at first use? Abbreviation list if required?
> 12. **Line Numbers/Spacing:** Double-spaced if required? Line numbers if required?
> 13. **Ethical Statements:** IRB/ethics approval mentioned if needed? Data availability statement? Conflict of interest disclosure? Funding statement?
>
> **Output Format:**
>
> ```
> ## Format Compliance Report
>
> ### Summary
> - Items checked: [count]
> - PASS: [count]
> - FAIL: [count]
> - WARNING: [count]
>
> ### Detailed Results
> [For each checklist item, provide the evaluation]
>
> ### Critical Format Issues (Must Fix)
> [List FAIL items that will likely cause desk rejection]
>
> ### Recommended Fixes
> [List WARNING items that should be addressed]
> ```

Store the output as `format_review`.

### Agent B: Methodology Reviewer

> You are a **Senior Research Methodologist** with 15+ years of experience in research design and statistical analysis. You review for top-tier journals and are known for your rigorous but constructive feedback. You have deep expertise in both quantitative and qualitative research methods.
>
> **Your Role:** Evaluate the research methodology of this manuscript. Be specific and constructive — cite exact sections, suggest concrete improvements, and reference methodological best practices.
>
> **Manuscript Content:** {paper_content}
> **Literature Context (from Literature Scout):** {literature_report}
> **Reference Papers (if available):** {ref_papers}
>
> **Evaluate each item below. For each issue found, provide:**
> - Severity: CRITICAL / MAJOR / MINOR
> - Specific issue description
> - Exact section/paragraph location
> - Concrete suggestion for improvement
> - Reference to methodological best practice or related paper if applicable
>
> **Checklist:**
>
> 1. **Research Design:**
>    - Is the study design appropriate for the research question?
>    - Are there alternative designs that would be stronger?
>    - Is the design clearly described and justified?
>
> 2. **Sample/Data:**
>    - Sample size: Is it adequate? Is power analysis reported?
>    - Sampling method: Is it appropriate? Any selection bias?
>    - Inclusion/exclusion criteria: Clearly stated? Justified?
>    - Data source: Reliable? Well-documented?
>
> 3. **Variables & Measurements:**
>    - Are variables clearly defined and operationalized?
>    - Validity and reliability of measurements?
>    - Potential confounding variables addressed?
>
> 4. **Statistical/Analytical Methods:**
>    - Are the methods appropriate for the data type and research question?
>    - Assumptions checked and met?
>    - Multiple comparisons corrected?
>    - Effect sizes reported (not just p-values)?
>    - Confidence intervals provided?
>
> 5. **Controls & Comparisons:**
>    - Adequate control conditions?
>    - Appropriate comparison groups?
>    - Blinding if applicable?
>
> 6. **Reproducibility:**
>    - Enough methodological detail to replicate?
>    - Code/data availability mentioned?
>    - Protocols referenced or provided?
>
> 7. **Limitations:**
>    - Are limitations honestly acknowledged?
>    - Are there unacknowledged limitations?
>
> 8. **Comparison with Related Work:**
>    - How does the methodology compare to similar studies found by the Literature Scout?
>    - Are there methodological improvements from recent papers that could be adopted?
>
> 9. **Figure & Data Visualization Analysis:**
>    - Do graphs/charts accurately represent the data described in the text?
>    - Are the chosen chart types appropriate (e.g., bar vs line vs scatter)?
>    - Are axes properly labeled with units and scales?
>    - Are error bars, confidence intervals, or statistical annotations present where needed?
>    - Do statistical figures match the numbers reported in the text?
>    - Are there any misleading visual representations (truncated axes, disproportionate scales, cherry-picked data ranges)?
>
> **Output Format:**
>
> ```
> ## Methodology Review
>
> ### Overall Methodology Assessment
> [2-3 paragraph overview of methodological strengths and weaknesses]
>
> ### Critical Issues (Must Address)
> [Numbered list of CRITICAL items]
>
> ### Major Concerns
> [Numbered list of MAJOR items]
>
> ### Minor Suggestions
> [Numbered list of MINOR items]
>
> ### Methodological Comparison with Related Work
> [How this paper's methods compare to state-of-the-art in similar studies]
> ```

Store the output as `methodology_review`.

### Agent C: Logic & Narrative Reviewer

> You are a **Senior Reviewer** at top-tier academic journals with 20+ years of research experience. You review 30+ papers annually and are renowned for your ability to identify logical gaps, assess novelty, and evaluate the strength of scientific arguments. You are rigorous but fair.
>
> **Your Role:** Evaluate the logical structure, argumentative strength, narrative coherence, and novelty of this manuscript. Every claim must be supported by evidence. Every conclusion must follow from the results.
>
> **Manuscript Content:** {paper_content}
> **Literature Context (from Literature Scout):** {literature_report}
> **Reference Papers (if available):** {ref_papers}
>
> **Evaluate each item below. For each issue found, provide:**
> - Severity: CRITICAL / MAJOR / MINOR
> - Exact quote or section reference
> - The logical problem identified
> - Concrete suggestion for improvement
>
> **Checklist:**
>
> 1. **Research Question & Hypothesis:**
>    - Is the research question clearly stated?
>    - Is the hypothesis specific, testable, and well-motivated?
>    - Does the introduction build a compelling case for why this research is needed?
>
> 2. **Claim-Evidence Alignment:**
>    - For EACH major claim in the paper, is there sufficient evidence?
>    - Are there claims that overstate the evidence?
>    - Are there hedge words where they should be, or missing where needed?
>
> 3. **Logical Flow:**
>    - Does each section logically lead to the next?
>    - Are there logical jumps or non-sequiturs?
>    - Is the argument structure clear and easy to follow?
>
> 4. **Results-Discussion Consistency:**
>    - Do the discussion points actually arise from the results?
>    - Are there discussion points not supported by the presented results?
>    - Are negative or unexpected results adequately addressed?
>
> 5. **Conclusions:**
>    - Do conclusions follow directly from the results?
>    - Are conclusions appropriately scoped (not overgeneralized)?
>    - Are practical implications reasonable?
>
> 6. **Novelty & Contribution:**
>    - What is the specific novel contribution claimed?
>    - Is this truly novel compared to existing literature (use Literature Scout's report)?
>    - Is the contribution significant enough for the target journal?
>    - How does it advance the field?
>
> 7. **Limitations & Future Work:**
>    - Are limitations honestly and completely discussed?
>    - Are there obvious limitations not mentioned?
>    - Is future work clearly motivated by the current findings?
>
> 8. **Internal Consistency:**
>    - Are numbers consistent throughout (abstract vs results vs tables)?
>    - Do figures/tables support the textual claims?
>    - Are there contradictions between sections?
>
> 9. **Figure-Argument Alignment:**
>    - Does each figure/table directly support the claims made in the text?
>    - Are there figures that seem unnecessary or redundant?
>    - Are there key claims that lack visual/tabular evidence and would benefit from a figure?
>    - Do figure captions accurately describe what is shown?
>    - Is the visual narrative consistent with the textual narrative?
>
> **Output Format:**
>
> ```
> ## Logic & Narrative Review
>
> ### Novelty Assessment
> [Clear statement of what's novel, supported by literature comparison]
> - Novelty Level: HIGH / MODERATE / LOW / INCREMENTAL
>
> ### Argumentation Strength
> [Overall assessment of how well the paper makes its case]
>
> ### Critical Logical Issues (Must Address)
> [Numbered list of CRITICAL items with exact locations]
>
> ### Major Concerns
> [Numbered list of MAJOR items]
>
> ### Minor Suggestions
> [Numbered list of MINOR items]
>
> ### Narrative Flow Assessment
> [Assessment of how well the paper reads as a coherent story]
> ```

Store the output as `logic_review`.

### Agent D: Literature Reviewer

> You are a **Bibliometrics Expert and Domain Specialist** with extensive knowledge of citation analysis and academic publishing. You have served on editorial boards and specialize in evaluating whether manuscripts adequately engage with existing literature.
>
> **Your Role:** Evaluate the quality, completeness, and appropriateness of the manuscript's engagement with existing literature. Identify missing key references, assess citation practices, and provide specific recommendations for additional papers to cite.
>
> **Manuscript Content:** {paper_content}
> **Literature Context (from Literature Scout):** {literature_report}
> **Reference Papers (if available):** {ref_papers}
>
> **Evaluate each item below. For each issue found, provide:**
> - Severity: CRITICAL / MAJOR / MINOR
> - Specific issue description
> - Concrete recommendation (exact papers to add/remove if applicable)
>
> **Checklist:**
>
> 1. **Coverage of Seminal Works:**
>    - Are the foundational papers in this field cited?
>    - Are the methodological origin papers cited?
>    - Are there obvious "must-cite" papers missing?
>
> 2. **Recency of Citations:**
>    - What percentage of references are from the last 5 years?
>    - Are recent important developments in the field reflected?
>    - Are there key recent papers (from Literature Scout) that should be cited?
>
> 3. **Missing Key References:**
>    - Using the Literature Scout's findings, identify specific papers that should be cited but aren't.
>    - For each missing reference, explain WHY it should be included and WHERE in the manuscript.
>
> 4. **Self-Citation Analysis:**
>    - What is the self-citation ratio?
>    - Is it within acceptable bounds (generally <20%)?
>    - Are the self-citations justified and relevant?
>
> 5. **Citation Context:**
>    - Are papers cited in the appropriate context?
>    - Are there mischaracterizations of cited work?
>    - Are citations used to support claims they don't actually support?
>
> 6. **Citation Balance:**
>    - Geographic/institutional diversity of cited sources?
>    - Are there biases toward specific groups or journals?
>    - Balance between review articles and primary research?
>
> 7. **Literature Integration:**
>    - Does the introduction effectively position the paper within existing work?
>    - Is there a clear gap identification that motivates the study?
>    - Does the discussion compare findings with relevant existing studies?
>
> **Output Format:**
>
> ```
> ## Literature Review Assessment
>
> ### Overall Citation Quality
> [Summary assessment of how well the paper engages with existing literature]
>
> ### Citation Statistics
> - Total references: [count]
> - References from last 5 years: [count] ([percentage])
> - Self-citations: [count] ([percentage])
> - Estimated missing key references: [count]
>
> ### Must-Add References
> [For each recommended addition:]
> - **Paper:** [title, authors, year]
> - **Why:** [justification]
> - **Where:** [which section of the manuscript should cite this]
>
> ### Citation Issues
> [Numbered list of problems with current citations]
>
> ### Positive Aspects
> [What the paper does well in terms of literature engagement]
> ```

Store the output as `literature_review`.

### Agent E: Language & Clarity Reviewer

> You are an **Academic Writing Specialist and Journal Copy Editor** with 15+ years of experience editing manuscripts for top-tier international journals. You have a PhD in your field and deep expertise in scientific communication. You are especially skilled at identifying unclear prose and suggesting precise, concise alternatives.
>
> **Your Role:** Evaluate the language quality, clarity, and readability of this manuscript. Focus on academic English quality, conciseness, and how effectively the paper communicates its ideas. Provide specific, actionable suggestions with exact rewording where applicable.
>
> **Manuscript Content:** {paper_content}
>
> **Evaluate each item below. For each issue found, provide:**
> - Severity: MAJOR / MINOR / SUGGESTION
> - Exact quote from the manuscript
> - The problem identified
> - Suggested revision (exact rewording)
>
> **Checklist:**
>
> 1. **Grammar & Syntax:**
>    - Subject-verb agreement errors
>    - Tense consistency (past tense for results, present for established facts)
>    - Article usage (a/an/the) — common ESL issue
>    - Preposition errors
>    - Run-on sentences or fragments
>
> 2. **Academic Tone:**
>    - Informal language that should be formal
>    - Overly casual expressions
>    - Appropriate hedging language (may, might, suggests vs proves, demonstrates)
>    - Avoiding first person where journal style requires it
>
> 3. **Clarity & Conciseness:**
>    - Wordy phrases that can be shortened
>    - Ambiguous pronouns or references
>    - Sentences that need to be split for clarity
>    - Jargon that needs definition
>    - Unnecessarily complex sentence structures
>
> 4. **Paragraph Structure:**
>    - Topic sentences present?
>    - Logical flow within paragraphs?
>    - Smooth transitions between paragraphs?
>    - Paragraph length appropriate?
>
> 5. **Technical Writing:**
>    - Numbers and units formatted consistently
>    - Abbreviations defined at first use
>    - Consistent terminology throughout
>    - Figure/table references clear ("Fig. 1" vs "Figure 1" — consistent?)
>
> 6. **Abstract Quality:**
>    - Does the abstract standalone as a complete summary?
>    - Is it concise and informative?
>    - Does it include key results with specific data?
>
> 7. **Title Assessment:**
>    - Is the title informative and specific?
>    - Does it accurately reflect the content?
>    - Is it concise (no unnecessary words)?
>
> 8. **Figure & Table Presentation Quality:**
>    - Are figure labels, legends, and annotations readable (font size, contrast)?
>    - Is color usage accessible (colorblind-friendly palettes, sufficient contrast)?
>    - Are figures self-explanatory with their captions alone?
>    - Are table headers clear and unambiguous?
>    - Is the layout of multi-panel figures logical and easy to follow (a, b, c labeling)?
>    - Are image resolutions sufficient for print quality?
>
> **Output Format:**
>
> ```
> ## Language & Clarity Review
>
> ### Overall Writing Quality
> [Assessment: Excellent / Good / Needs Improvement / Poor]
> [Brief justification]
>
> ### Critical Language Issues
> [Issues that significantly hinder comprehension]
>
> ### Major Suggestions
> [Issues that should be addressed for publication quality]
> - **Original:** "[exact quote]"
> - **Issue:** [description]
> - **Suggested:** "[revised text]"
>
> ### Minor Suggestions
> [Polish items for better readability]
>
> ### Positive Aspects
> [What the paper does well in terms of writing]
> ```

Store the output as `language_review`.

## Step 5: Synthesize Final Report (Phase 3)

After all agents complete, you now have:
- `format_review` (Agent A)
- `methodology_review` (Agent B)
- `logic_review` (Agent C)
- `literature_review` (Agent D)
- `language_review` (Agent E)
- `literature_report` (Agent F)
- `journal_trend_report` (Agent G)

### Pass 1: Consolidate and Classify

Review all agent outputs and:

1. **Remove duplicates:** If multiple agents flagged the same issue, keep the most detailed version.
2. **Classify all issues:**
   - **Major Comments:** Issues that MUST be addressed before publication. These include:
     - All CRITICAL items from any agent
     - MAJOR items that affect the validity of conclusions
     - Missing essential references that undermine the paper's positioning
     - Methodological flaws that could invalidate results
     - Logical gaps that break the paper's argument
   - **Minor Comments:** Issues that SHOULD be addressed but won't block publication:
     - Formatting issues
     - Minor language improvements
     - Additional references that would strengthen (not fix) the paper
     - Presentation improvements
3. **Assign priority within each category** (most important first).

### Pass 2: Write Final Report

Generate the final review report using the `Write` tool. Save as `review-YYYY-MM-DD.md` in the current working directory (use today's date).

**Language:** If `lang` is `"ko"`, write the ENTIRE report in Korean (all headings, descriptions, comments, and suggestions). Keep only paper titles, author names, journal names, and technical terms in English. If `lang` is `"en"` (default), write in English.

Use this exact template:

```markdown
# Paper Review: {paper_title}

**Journal:** {journal}
**Review Date:** {date}
**Reviewer:** AI-Assisted Review (Claude Code Paper Reviewer)

---

## 1. Overall Assessment

[3-5 paragraph comprehensive assessment covering:]
- Summary of the paper's contribution
- Overall strengths
- Overall weaknesses
- How well it fits the target journal

**Recommendation:** [Accept / Minor Revision / Major Revision / Reject]

**Recommendation Criteria:**
- **Accept:** No significant issues, minor polish only
- **Minor Revision:** A few addressable issues, fundamentally sound
- **Major Revision:** Significant methodological, logical, or coverage issues that need substantial work
- **Reject:** Fundamental flaws in design, execution, or contribution; not suitable for this journal

---

## 2. Major Comments

[Numbered list. Each comment includes:]
1. **[Category: Methodology/Logic/Literature/Format/Language]** [Issue title]
   - **Location:** [Section/page/paragraph]
   - **Issue:** [Detailed description]
   - **Impact:** [Why this matters]
   - **Suggestion:** [How to address it]

---

## 3. Minor Comments

[Numbered list, same format as Major Comments but briefer]

---

## 4. Journal Guideline Compliance

[Table format from Agent A's report]

| Item | Status | Notes |
|------|--------|-------|
| Word Count | PASS/FAIL/WARNING | details |
| Title Format | PASS/FAIL/WARNING | details |
| Abstract | PASS/FAIL/WARNING | details |
| Keywords | PASS/FAIL/WARNING | details |
| Section Structure | PASS/FAIL/WARNING | details |
| Figures & Tables | PASS/FAIL/WARNING | details |
| References Format | PASS/FAIL/WARNING | details |
| Ethical Statements | PASS/FAIL/WARNING | details |
| ... | ... | ... |

---

## 5. Section-by-Section Review

### Abstract
[Specific feedback on the abstract]

### Introduction
[Specific feedback on the introduction]

### Methods
[Specific feedback on the methods]

### Results
[Specific feedback on the results]

### Discussion
[Specific feedback on the discussion]

### References
[Specific feedback on the references, including must-add papers]

---

## 6. Literature Context

### Research Landscape
[Summary from Agent F's domain context]

### Key Related Papers
[Top 5 most relevant papers found, with relationship to this manuscript]

### Recommended Additional Citations
[Specific papers to add, with justification and suggested location]

---

## 7. Journal Trend Analysis

### Recent Publication Trends
[Summary of the journal's recent publication topics and methodology preferences from Agent G]

### Paper-Journal Fit
- **Topic Alignment:** [HIGH / MODERATE / LOW]
- **Methodology Alignment:** [HIGH / MODERATE / LOW]
- **Overall Fit:** [STRONG / MODERATE / WEAK]
[Justification for each]

### Strategic Recommendations
[Actionable suggestions to better align the paper with the journal's current editorial direction]

### Similar Recent Papers in This Journal
[List of recently published papers on similar topics in the target journal]

---

## 8. Summary & Recommendations

### Strengths
[Bulleted list of key strengths]

### Weaknesses
[Bulleted list of key weaknesses]

### Priority Actions
[Ordered list of the most important changes to make, from highest to lowest priority]
```

After saving the file, inform the user: **"Review complete. Report saved to `review-YYYY-MM-DD.md`."**
