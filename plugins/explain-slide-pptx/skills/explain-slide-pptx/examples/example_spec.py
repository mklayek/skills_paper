"""Example spec for explain-slide-pptx: two slides, two palettes (classic, then ocean-tint).

Run from anywhere:
  python <skill>/scripts/explain_slides.py <skill>/examples/example_spec.py
Writes example_deck.pptx (+ example_deck.md) next to this file.
Slide 1 reproduces the reference slide (assets/reference_solenoid.png).
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
FIG = lambda name: os.path.join(HERE, "figs", name)
WC = "Wikimedia Commons"

DECK = {
    "output": os.path.join(HERE, "example_deck.pptx"),
    "md": os.path.join(HERE, "example_deck.md"),
    "work": os.path.join(HERE, "_build"),
    "palettes": ["classic", "ocean-tint"],          # or "cycle", or one name, or "palette" per slide
    "sizes": {"body": 14, "small": 13, "sym": 13, "eq": 16},
    "slides": [
        {
            "title": "The Solenoid", "highlight": "Solenoid",
            "subtitle": "What it is · Magnetic field · Inductance · Induction · Uses",
            "intro": {
                "head": "What is a solenoid?",
                "figure": {"image": FIG("13_solenoid_coil.png"), "credit": WC},
                "definition": "A **solenoid** is a wire wound in a tight helix, a coil whose length is much greater than its diameter.",
                "points": ["Each turn makes a small loop field, and the loops **add up** inside.",
                           "Inside: a strong, **uniform** field along the axis.",
                           "Outside: a weak field, like a **bar magnet** with N and S ends."],
                "equation": [r"\oint \mathbf{B}\cdot d\mathbf{l}=\mu_0 I_{\mathrm{enc}}", r"\Rightarrow\ Bl=\mu_0 N I"],
                "symbols": [("$I_{enc}$", "current through the loop, $NI$"), ("$l$", "length of the coil (m)")],
            },
            "panels": [
                {"head": "Magnetic field",
                 "definition": "A current through the coil makes a **nearly uniform field** inside. The right-hand grip rule gives its direction.",
                 "figure": {"image": FIG("14_solenoid_field_lines.png"), "credit": WC},
                 "equation": r"B=\mu_0\,\frac{N}{l}\,I",
                 "symbols": [("$B$", "field inside (T)"), ("$μ_{0}$", "4π × 10^{−7} H/m")],
                 "points": ["Iron core: $B$ rises by $μ_{eff}$.", "$B$ does not depend on $r$."],
                 "example": ["$N$ = 500, $l$ = 0.25 m, $I$ = 2 A", "$B$ = 5.0 mT"]},
                {"head": "Inductance & induction",
                 "definition": "The coil links its own flux, so it has an **inductance**. A changing field through it induces a voltage.",
                 "figure": {"image": FIG("23_solenoid_tikz.png")},
                 "equation": [r"L=\frac{\mu_0 N^2 A}{l}", r"e=-NA\,\frac{dB}{dt}"],
                 "symbols": [("$A$", "area (m^{2})"), ("$e$", "induced emf (V)")],
                 "points": ["$L$ ∝ $N^{2}$: **double the turns**, 4$L$.", "Energy $W$ = ½$LI^{2}$."],
                 "example": ["Same coil, $r$ = 2 cm", "$L$ = 1.58 mH"]},
                {"head": "Uses",
                 "definition": "The same coil **sends** a field (transmitter) and **senses** one (receiver).",
                 "figure": {"image": FIG("15_iter_central_solenoid.jpg"), "credit": WC},
                 "equation": r"m=NIA",
                 "symbols": [("$m$", "magnetic moment (A m^{2})")],
                 "points": ["Relays, valves, locks.", "**MRI** and ITER magnets."],
                 "example_title": "In EM surveys",
                 "example": ["Tx: large $m$.", "Rx: $e$ ∝ $NA$ d$B$/d$t$."]},
            ],
        },
        {
            "title": "The Series RLC Circuit", "highlight": "RLC",
            "subtitle": "What it is · Resonance · Damping · Bandwidth · Q factor",
            "intro": {
                "head": "What is an RLC circuit?",
                "figure": {"image": FIG("01_rlc_series_circuit.png"), "credit": WC},
                "definition": "An **RLC circuit** is a resistor $R$, an inductor $L$ and a capacitor $C$ connected to a voltage source.",
                "points": ["$R$ **loses** energy as heat.",
                           "$L$ stores energy in a **magnetic field**, $C$ in an **electric field**.",
                           "Energy swaps between $L$ and $C$, so the circuit **oscillates**."],
                "equation": r"L\frac{dI}{dt}+RI+\frac{q}{C}=V(t)",
                "symbols": [("$q$", "capacitor charge, $I$ = d$q$/d$t$"), ("$ω_{0}$", "1/√($LC$), natural frequency")],
            },
            "panels": [
                {"head": "Resonance",
                 "definition": "At $ω_{0}$ the reactances of $L$ and $C$ cancel, so the circuit **resonates**.",
                 "figure": {"image": FIG("02_rlc_series_resonance_current.png"), "credit": WC},
                 "equation": r"\omega_0=\frac{1}{\sqrt{LC}}",
                 "symbols": [("$f_{0}$", "$ω_{0}$/2π (Hz)")],
                 "points": ["$V$ and $I$ **in phase**.", "$V_{L}$ = $V_{C}$ = $QV$."],
                 "example_title": "Uses", "example": ["Radio tuning.", "Tuned EM loops."]},
                {"head": "Damping",
                 "definition": "$R$ removes energy, so free oscillations **die away**.",
                 "figure": {"image": FIG("05_damped_oscillations.png"), "credit": WC},
                 "equation": [r"\zeta=\frac{R}{2}\sqrt{\frac{C}{L}}"],
                 "symbols": [("$ζ$", "damping ratio")],
                 "points": ["$ζ$ < 1: **rings**.", "$ζ$ = 1: critical."],
                 "example_title": "Uses", "example": ["Car suspension.", "Damped TEM coils."]},
                {"head": "Bandwidth & Q",
                 "definition": "The **bandwidth** is the peak width at half power.",
                 "figure": {"image": FIG("07_q_factor_bandwidth.png"), "credit": WC},
                 "equation": r"Q=\frac{f_0}{\Delta f}",
                 "symbols": [("$Q$", "1/(2$ζ$)")],
                 "points": ["High $Q$: **narrow** peak.", "Low $Q$: broad, fast."],
                 "example": ["$L$ = 10 mH, $C$ = 1 μF", "$R$ = 10 Ω: $Q$ = 10"]},
            ],
        },
    ],
}
