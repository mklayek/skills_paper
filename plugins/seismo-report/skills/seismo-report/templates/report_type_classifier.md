# Report-type classifier (seismo-report)

&nbsp;&nbsp;&nbsp;&nbsp;Read every input, then match it to one primary report type. The type sets which chapters carry weight; the full chapter list from `MASTER_REPORT_TEMPLATE.md` is always present, but the emphasized chapters differ.

| If the inputs show ... | Primary type | Emphasized chapters |
|---|---|---|
| A single event, waveforms, location, magnitude | Earthquake event analysis | Dataset, Methodology, Results, Interpretation, Source parameters |
| PSHA/DSHA, hazard curves, response spectra | Seismic hazard study | Study Area, Methodology, Ground-motion model, Results, Validation |
| Raw/processed traces, filtering, picks | Waveform analysis | Instrumentation, Processing Workflow, Results, Interpretation |
| Spectra, corner frequency, moment, stress drop | Source-parameter estimation | Mathematical Background, Methodology, Results, Discussion |
| Simulated vs recorded motions, FAS, GOF | Ground-motion simulation | Methodology, Data Processing, Results, Validation, Comparison |
| Velocity models, iterations, misfit, kernels | FWI results | Mathematical Background, Methodology, Results, Interpretation, Validation |
| Cross-correlations, dispersion, Green's functions | Ambient-noise analysis | Methodology, Results, Interpretation |
| GPR + seismic joint panels | GPR-seismic comparison | Datasets, Methodology, Comparison, Interpretation |

&nbsp;&nbsp;&nbsp;&nbsp;When several types apply, name the dominant one in the Executive Summary and keep the union of emphasized chapters. When none fits cleanly, default to Earthquake event analysis and note the ambiguity. Chapters with no supporting input still appear and read `Yet to be developed`.
