# Per-analysis protocols (seismo-report)

&nbsp;&nbsp;&nbsp;&nbsp;Each block below names what to read from that figure or data kind and the physical reasoning to attach in the Results/Interpretation chapters. Follow the humanization gate in `humanization_gate.md` while writing from these recipes.

## Waveform / time history
&nbsp;&nbsp;&nbsp;&nbsp;Read the amplitude, the duration, the arrival times, the P and S phase separation, and the polarity of the first motion. Attach the source-distance reasoning that the P-S separation implies and the site reasoning that the amplitude and duration pattern suggests. Give the peak ground acceleration (PGA), peak ground velocity (PGV), or peak ground displacement (PGD) with units. State which component the peak came from and at what time.

## Fourier amplitude spectrum (FAS)
&nbsp;&nbsp;&nbsp;&nbsp;Read the spectral shape, the corner frequency $f_c$, the high-frequency decay slope, and any site amplification peak. Attach the source-size reasoning that $f_c$ implies through the source radius and the near-surface attenuation reasoning carried by the kappa parameter $\kappa$. Note whether the decay is closer to $\omega^{-2}$ or a shallower slope and what that implies for the source model.

## Response spectrum
&nbsp;&nbsp;&nbsp;&nbsp;Read the plateau level, the period of the spectral peak, and the ordinates at the periods relevant to typical structures. Attach the structural-period significance, which is the reasoning that connects the peak period to the fundamental period of buildings or bridges at risk. State the spectral acceleration value with units at the period of interest.

## Spectrogram
&nbsp;&nbsp;&nbsp;&nbsp;Read how the frequency content evolves over time, the dispersion pattern if a surface wave train is present, and the coda decay. Attach the path and scattering reasoning, which explains how heterogeneity along the travel path stretches the wave train and shifts energy to lower frequency with time.

## Focal mechanism
&nbsp;&nbsp;&nbsp;&nbsp;Read the two nodal planes, the P and T axes, and the resulting faulting style, whether normal, reverse, or strike-slip. Attach the tectonic-stress reasoning that connects the mechanism to the regional stress field and to any known fault in the area.

## Station map / network geometry
&nbsp;&nbsp;&nbsp;&nbsp;Read the station coverage, the azimuthal gap, and the source-station distances. Attach the location-uncertainty reasoning, which is that a large azimuthal gap or a sparse near-source network widens the epicentral and depth uncertainty.

## Earthquake catalogue
&nbsp;&nbsp;&nbsp;&nbsp;Read the magnitude-frequency distribution, the b-value, and the spatial clustering of events. Attach the seismicity reasoning, which connects a low b-value to higher stress or a clustered pattern to a specific fault segment or aftershock sequence.

## FWI model panels
&nbsp;&nbsp;&nbsp;&nbsp;Read the velocity structure across iterations, the pattern of the model update at each stage, and the trend of the misfit function. Attach the resolution and convergence reasoning, which is the link between ray or wavefield coverage and how well a given depth or region is actually resolved (this is the FWI use case in `E:\WORKS\OUTPUT`).

## Real-vs-simulated comparison / goodness-of-fit (GOF)
&nbsp;&nbsp;&nbsp;&nbsp;Read the amplitude and phase agreement between the recorded and simulated traces, the cross-correlation lag, and how the fit changes with frequency band. Attach the model-adequacy reasoning, which states whether the velocity model, source, or both need revision based on where the misfit concentrates.
