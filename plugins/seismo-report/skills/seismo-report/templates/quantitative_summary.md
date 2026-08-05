# Quantitative summary (seismo-report)

&nbsp;&nbsp;&nbsp;&nbsp;The report states the recurring seismological quantities wherever the data supports them, rather than leaving a result only in a figure. These are the event origin time, the hypocentre and depth, the magnitude ($M_w$, $M_L$), the peak ground acceleration (PGA), the peak ground velocity (PGV), the peak ground displacement (PGD), the corner frequency $f_c$, the seismic moment $M_0$, the stress drop $\Delta\sigma$, the signal-to-noise ratio (SNR), the cross-correlation coefficient and lag, the misfit reduction, and the goodness-of-fit (GOF) scores.

## Example: event-parameter table

Table 1. Event parameters for the analyzed earthquake.

| Parameter | Symbol | Value | Unit |
|---|---|---|---|
| Origin time | $t_0$ | {{YYYY-MM-DD HH:MM:SS}} | UTC |
| Hypocentre | lat, lon | {{xx.xxx, yy.yyy}} | degrees |
| Depth | $h$ | {{value}} | km |
| Moment magnitude | $M_w$ | {{value}} | - |
| Local magnitude | $M_L$ | {{value}} | - |
| Seismic moment | $M_0$ | {{value}} | N·m |
| Corner frequency | $f_c$ | {{value}} | Hz |
| Stress drop | $\Delta\sigma$ | {{value}} | MPa |

## Example: goodness-of-fit table

Table 2. Goodness-of-fit between recorded and simulated ground motion.

| Station | Component | Cross-correlation | Lag | GOF score | Frequency band |
|---|---|---|---|---|---|
| {{STA1}} | {{HHZ}} | {{0.xx}} | {{value s}} | {{value}} | {{0.1-1 Hz}} |
| {{STA2}} | {{HHE}} | {{0.xx}} | {{value s}} | {{value}} | {{0.1-1 Hz}} |
