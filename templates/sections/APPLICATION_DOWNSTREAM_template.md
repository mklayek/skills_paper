# 🔗 Reusable Template — **DOWNSTREAM APPLICATION** Section (V)

> Domain-agnostic scaffold for a *downstream-application* top-level section, reverse-engineered from
> J. Ge *et al.*, “Wavelet-GAN…,” *IEEE TGRS*, vol. 62, Art. 5918214, 2024 (§V, “Application of Wavelet-GAN
> in Inversion”).

---

## 1. Role & Function

**Role:** demonstrate the method's value as a **preprocessing step inside a larger pipeline** — show that better
cleaning yields a better end-to-end result on a separate, established task. **Function:** elevate the contribution
from "we remove the artifact well" to "removing it our way measurably improves what people actually do next."
Plug the method's output into a **fixed, third-party downstream model** and contrast against the field-standard
preprocessing baseline; pre-empts the "so what?" objection.

## 2. Paragraph Flow

1. **Why the downstream task suffers** — name the downstream task; explain how the artifact corrupts its results.
2. **Conventional preprocessing's flaw** — the field-standard step everyone uses + the specific information it destroys.
3. **Experiment setup** — feed *our output* vs *baseline-preprocessing output* into the **same pretrained downstream model**; give data source + acquisition details.
4. **Result contrast + figure** — baseline-preprocessed → wrong/degraded downstream result; our-preprocessed → result close to ground truth; **diagnose why** the baseline failed.
5. **Reliability conclusion** — better preprocessing of our kind improves downstream reliability.

## 3. Component Slots

`[DOWNSTREAM TASK + WHY ARTIFACT HURTS IT]` · `[CONVENTIONAL PREPROCESSING FLAW]` ·
`[EXPERIMENT SETUP + acquisition details]` · `[RESULT CONTRAST OURS vs BASELINE + figure]` ·
`[RELIABILITY CONCLUSION]`

## 4. Fill-in Template

> "The presence of **[ARTIFACT]** can seriously affect the results of **[DOWNSTREAM TASK]** [CIT].
> **[DOWNSTREAM-MODEL FAMILY]** methods are typically trained on **[idealized/simulated data]**, which does not
> account for **[ARTIFACT]**. In practice, the data are usually preprocessed by **[CONVENTIONAL METHOD]** to
> remove **[ARTIFACT]** before being fed into **[DOWNSTREAM MODEL]**. However, this causes **[SIGNAL OF
> INTEREST]** to lose **[KEY INFORMATION]**, resulting in **[INACCURATE DOWNSTREAM RESULT]** [CIT]. In this
> section, we test the effectiveness of **[OUR METHOD]** within **[DOWNSTREAM TASK]**. We collected real
> **[DATA TYPE]** from a known **[TARGET]** and processed it with **[OUR METHOD]** and **[BASELINE]**,
> respectively, then input each into the pretrained **[DOWNSTREAM MODEL]** [CIT]. The data were acquired with
> **[INSTRUMENT]**, **[KEY PARAMETERS]**; the target was **[DESCRIPTION/GEOMETRY]**, and **[MEDIUM PROPERTY]**
> was **[VALUE]**. As shown in Fig. **[N(panel)]**, with **[BASELINE]**-processed input the downstream model
> produced a result far from the truth, because residual **[ARTIFACT]** was erroneously interpreted as
> **[SIGNAL OF INTEREST]**. In contrast, panels **[N(panels)]** show that **[OUR METHOD]** removes **[ARTIFACT]**
> and the resulting **[DOWNSTREAM OUTPUT]** is much closer to the true **[GROUND TRUTH]**. Therefore,
> **[OUR METHOD]** can be used for **[DOWNSTREAM-TASK]** preprocessing to improve the reliability of
> **[DOWNSTREAM RESULT]**."

## 5. Figures · Interpretation · Citations · Tone

- **Figure:** one multi-panel application figure; standard layout — (a) acquisition/survey schematic; (b) ground
  truth; (c) baseline-preprocessed input; (d) downstream result from baseline; (e) our-preprocessed input;
  (f) downstream result from ours. Cite panels inline in flow order; pair them ("compare (d) and (f) against (b)").
- **Interpretation:** hold the downstream model **fixed**, vary only the preprocessing → any difference is
  attributable to the cleaning method. Read each result **against ground truth**. Always supply a **mechanism**
  for the baseline's failure (e.g., "residual artifact mistaken for true signal"), not just a verdict.
- **Citations:** downstream task importance + artifact sensitivity [refs]; conventional-preprocessing weakness
  [ref]; the third-party downstream model by name with its primary ref at first mention. Reference-light overall.
- **Tone:** 4–6 compact paragraphs / one column; applied, evidence-first; first-person plural for the experiment;
  hedged on causal diagnosis ("we suspect/believe") but firm on the observed outcome + recommendation.

## 6. Transition Out → Conclusion

End on the reliability claim phrased as a forward-looking recommendation ("…can be used for **[task]**
preprocessing to improve reliability"), which the Conclusion restates as a headline contribution.

## 7. ✅ Checklist

- [ ] Names a concrete downstream task and explains the artifact's specific failure mode there.
- [ ] Identifies the conventional preprocessing baseline and the information it destroys.
- [ ] Holds the downstream model **fixed**; varies **only** the preprocessing.
- [ ] Reads all results against **ground truth**; gives a **mechanism** for the baseline failure.
- [ ] Multi-panel figure cited panel-by-panel in flow order.
- [ ] Closes with a reliability recommendation that the Conclusion can echo.
