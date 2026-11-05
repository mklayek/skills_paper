"""png-explain example: self induction and mutual induction (two panels + comparison table).

Rebuilds the layout of reference_style.png in the png-explain style: white background, black text,
color only for highlights, TikZ schematics, page border, 16:9.
Run:  python spec_self_mutual_induction.py
"""
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "scripts"))
from png_explain import build  # noqa: E402

SELF_TIKZ = r"""
\begin{circuitikz}[line width=1.1pt, scale=1.4]
\draw (0,0) to[battery1, l_=$\mathcal{E}$] (0,1.6) -- (0.2,1.6) to[cspst, l=$S$] (1.5,1.6) -- (1.88,1.6);
\foreach \k in {0,...,13} \draw[line width=1.4pt] ({2.0+0.28*\k},1.6) ellipse (0.12 and 0.55);
\draw (5.76,1.6) -- (6.3,1.6) -- (6.3,0) -- (0,0);
\draw[blue, dashed, line width=0.9pt] (3.82,1.6) ellipse (2.45 and 0.95);
\draw[blue, dashed, line width=0.9pt] (3.82,1.6) ellipse (2.95 and 1.3);
\node[blue] at (7.05,1.6) {\Large$\Phi$};
\draw[red, -{Latex[length=3mm]}, line width=1.5pt] (2.3,3.25) -- (5.4,3.25) node[midway, above] {changing current $I$};
\node at (1.72,2.45) {\Large$L$};
\node at (3.82,-0.5) {induced emf opposes the change (Lenz's law)};
\end{circuitikz}"""

MUTUAL_TIKZ = r"""
\begin{circuitikz}[line width=1.1pt, scale=1.4]
\draw (0,0) to[sV] (0,1.6) -- (0.78,1.6);
\foreach \k in {0,...,6} \draw[line width=1.4pt] ({0.9+0.26*\k},1.6) ellipse (0.12 and 0.55);
\draw (2.58,1.6) -- (2.9,1.6) -- (2.9,0) -- (0,0);
\foreach \k in {0,...,6} \draw[line width=1.4pt] ({3.9+0.26*\k},1.6) ellipse (0.12 and 0.55);
\draw (3.78,1.6) -- (3.5,1.6) -- (3.5,0) -- (6.3,0) -- (6.3,0.45);
\draw (5.58,1.6) -- (6.3,1.6) -- (6.3,1.15);
\draw[fill=white] (6.3,0.8) circle (0.35) node {$e_2$};
\draw[blue, dashed, line width=0.9pt] (3.2,1.6) ellipse (2.75 and 1.0);
\node[blue] at (3.2,2.85) {\Large$\Phi$};
\draw[red, -{Latex[length=2.5mm]}, line width=1.5pt] (0.15,2.0) -- (0.75,2.0) node[left=7mm, red] {$I_1$};
\node[align=center] at (1.68,3.35) {primary coil\\($N_1$ turns)};
\node[align=center] at (4.68,3.35) {secondary coil\\($N_2$ turns)};
\node at (3.2,-0.5) {changing $I_1$ induces an emf in the secondary coil};
\end{circuitikz}"""

SPEC = {
    "title": r"Self Induction \hl{\&} Mutual Induction",
    "subtitle": "Electromagnetism · Inductance",
    "panels": [
        {
            "head": "Self induction", "color": "blue",
            "definition": r"Self induction is the phenomenon in which a changing current in a coil induces an emf in the \kw{same coil}.",
            "figure": {"tikz": SELF_TIKZ},
            "equation": r"e=-L\,\frac{dI}{dt}",
            "symbols": [("e", "induced emf (V)"), ("L", "self inductance (H)"),
                        (r"dI/dt", "rate of change of current (A/s)")],
            "points": ["Also called the \\kw{back emf}.",
                       "Depends on the number of turns, the area of the coil and the core material.",
                       "Unit of inductance: henry (H)."],
            "example": ["Switch on a fan or a motor: the current does not rise instantly.",
                        "Self induction resists the sudden change."],
        },
        {
            "head": "Mutual induction", "color": "red",
            "definition": r"Mutual induction is the phenomenon in which a changing current in one coil induces an emf in \kw{another nearby coil}.",
            "figure": {"tikz": MUTUAL_TIKZ},
            "equation": r"e_2=-M\,\frac{dI_1}{dt}",
            "symbols": [("e_2", "induced emf in the secondary (V)"), ("M", "mutual inductance (H)"),
                        (r"dI_1/dt", "rate of change of the primary current (A/s)")],
            "points": ["Needs \\kw{two coils}.",
                       "Depends on the distance between the coils, the number of turns and the core material.",
                       "The basis of transformers."],
            "example": ["A transformer moves energy from one coil to the other.",
                        "No direct electrical connection between the coils."],
        },
    ],
    "table": {
        "head": "Self induction vs mutual induction",
        "rows": [("Coils", "One coil", "Two coils"),
                 ("Emf induced in", "The same coil", "The second coil"),
                 ("Cause", "Its own current change", "Current change in the nearby coil"),
                 ("Example", "Inductor, choke", "Transformer")],
    },
}

if __name__ == "__main__":
    tmp = Path(tempfile.gettempdir()) / "png_explain_example"
    sys.exit(build(SPEC, out=HERE / "self_mutual_induction_explain.png", docs=HERE,
                   work=tmp / "build", archive=tmp / "archive"))
