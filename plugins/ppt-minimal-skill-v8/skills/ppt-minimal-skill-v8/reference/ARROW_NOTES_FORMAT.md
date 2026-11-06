---
description: Convert textbook passages and technical explanations into
  crisp, teaching-ready geophysics notes using the "Concept → Original
  principle/mechanism → Meaning/implication" format while preserving
  source wording and scientific accuracy.
name: crisp-source-faithful-geophysics-notes
---

# Skill: Crisp, Source-Faithful Geophysics Notes

## Purpose

Transform textbook passages, lecture material, and technical
explanations into concise, clear, teaching-ready bullet points. Preserve
the original source's terminology, technical meaning, and key details as
much as possible, while making the content easier to teach, revise, and
remember.

## Core format

Use this structure for each point:

**Concept / Term** → Original principle, definition, or mechanism →
Physical meaning, consequence, limitation, or application.

Examples:

-   **Electrolytic conduction** → Predominant conduction mechanism in
    most rocks → At low frequencies, it is the only conduction mechanism
    when metallic minerals are absent.
-   **Porosity requirement** → Rock structure must be somewhat porous
    when metallic minerals are absent → Electrolytic fluids in pore
    spaces permit current flow.
-   **Warburg impedance** → Magnitude varies inversely with the square
    root of frequency → Corresponds to a frequency exponent of (c =
    0.5).

## Instructions

1.  **Preserve source wording.** Retain the original technical terms,
    phrases, names, symbols, and qualifiers wherever possible.
    Paraphrase only when needed for clarity or concision.
2.  **Keep the original meaning.** Do not strengthen, weaken, or alter
    scientific claims. Preserve conditions such as "at low frequencies,"
    "in most rocks," "typically," and "under these assumptions."
3.  **Be crisp.** Each bullet should normally contain one main idea and
    one clear implication. Remove repetition, filler, and unnecessary
    introductory phrases.
4.  **Use arrow logic.** Use `→` to connect the concept to its mechanism
    and then to its significance. Use two arrows when helpful:
    -   **Concept** → Mechanism or property → Consequence or
        application.
5.  **Retain useful technical detail.** Keep equations, parameter
    symbols, numerical ranges, units, named models, assumptions, and
    important references when they matter to understanding the source.
6.  **Use bold selectively.** Bold the key concept or technical term at
    the start of each bullet. Bold additional phrases only when they are
    essential for teaching or revision.
7.  **Avoid unsupported additions.** Do not add facts, examples,
    explanations, or applications that are not supported by the supplied
    passage unless the user explicitly asks for expansion.
8.  **Do not oversimplify relationships.** Keep distinctions between
    related concepts, mechanisms, assumptions, and limitations. Do not
    merge separate mechanisms into one vague statement.
9.  **Keep equations accurate.** Preserve the source equation where
    provided. If an equation is requested, use standard mathematical
    notation and define symbols only when useful.
10. **Maintain source-specific qualifiers.** If the source says "most IP
    effects," do not change it to "all IP effects." If it says a method
    "can" cause errors, do not say it "always" causes errors.
11. **Prefer teaching-ready language.** Write in clear technical English
    suitable for lecture slides, quick notes, exam revision, and
    geophysics teaching.
12. **Follow the requested scope.** If the user asks to rewrite only the
    supplied text, do not add a general introduction, conclusion, or
    unrelated background section.

## Recommended transformation workflow

1.  Identify the key concepts and technical terms in the passage.
2.  Separate distinct principles, mechanisms, assumptions, numerical
    ranges, and limitations.
3.  Keep the source's important wording and details.
4.  Convert each distinct idea into one concise arrow-format bullet.
5.  Check that no important condition, parameter, or scientific
    qualification has been lost.
6.  Remove redundant wording and ensure each bullet can stand alone in
    teaching notes.

## Output style

Default to a simple bullet list, with no heading unless useful or
requested.

Preferred:

-   **Polarization impedance ((Z_m))** → Represents a shortage or excess
    of ions near clay particles in membrane polarization, or at the
    metallic--ionic interface in electrode polarization → Explains the
    IP effect.
-   **Cole--Cole relaxation model** → Improves the representation of IP
    response parameters → Uses a frequency exponent (c = 0.25)--(0.35)
    for most IP effects.
-   **Frequency exponent ((c))** → Theoretical limits range from 0 to 1
    → May approach 1 for EM coupling and be as low as 0.1 for certain
    minerals.

Avoid:

-   Long paragraphs copied directly from the source.
-   Overly broad summaries that remove technical detail.
-   Replacing source terminology with informal synonyms.
-   Adding unsupported claims or examples.
-   Repeating the same idea in multiple bullets.
-   Using several sentences when one arrow-linked bullet is sufficient.

## Adaptation to user instructions

-   If the user says **"keep the original text as much as possible,"**
    stay close to the source wording and shorten only what is necessary.
-   If the user says **"crisp,"** prioritize brevity while retaining the
    essential scientific content.
-   If the user asks for **"just definition or meaning,"** provide only
    the requested definition or meaning.
-   If the user asks for **detailed notes**, expand the explanation
    while retaining clear structure and source fidelity.
-   If the user provides an established format, follow that format
    rather than imposing a new one.

## Final quality check

Before responding, verify:

-   Does every bullet follow **Concept → Principle/mechanism →
    Implication**, where appropriate?
-   Is the original scientific meaning preserved?
-   Are important terms, equations, symbols, numerical values, and
    qualifications retained?
-   Is the wording concise and suitable for teaching?
-   Have unsupported details and unnecessary explanations been avoided?
