# -*- coding: utf-8 -*-
"""v4 rule: slide titles take the source section names (subsection, or lettered part).
Consecutive slides of the same part get "<name> (continued)". Slides not listed keep their title.
Book semicolons become colons (no-semicolon rule); letters such as "(c)" are dropped."""
import glob, io, json, re, sys
sys.stdout = io.open(1, "w", encoding="utf-8", closefd=False)
R = [  # (first index, last index, marker, name)
 (2, 3, "◆", "Introduction and Historical Background"),
 (5, 10, "■", "Vector and Scalar Potentials"),
 (11, 11, "■", "Description of EM Fields"),
 (12, 13, "●", "Biot–Savart law: magnetic field of a long wire"),
 (14, 14, "●", "Vector potential of a current element"),
 (15, 16, "●", "Long straight horizontal wire"),
 (17, 19, "●", "Large rectangle"),
 (20, 26, "●", "Small horizontal coil (vertical magnetic dipole)"),
 (27, 27, "●", "Horizontal magnetic dipole"),
 (28, 33, "●", "Vertical straight wire (vertical electric dipole)"),
 (34, 34, "■", "Combination of FD Fields"),
 (35, 40, "●", "Amplitude and phase relations"),
 (41, 43, "●", "Elliptic polarization"),
 (44, 51, "●", "Mutual inductance: general theory"),
 (52, 52, "●", "Self-inductance"),
 (53, 54, "●", "Mutual inductance: numerical example"),
 (55, 56, "●", "Conductor response"),
 (57, 57, "■", "Fields in the Time Domain"),
 (58, 59, "●", "Method of TD analysis"),
 (60, 62, "●", "Long straight horizontal wire in the time domain"),
 (63, 67, "●", "Large rectangle in the time domain"),
 (68, 74, "●", "Small horizontal coil in the time domain"),
 (76, 76, "◆", "EM Equipment"),
 (77, 78, "■", "Power Sources"),
 (79, 79, "■", "Transmitter Loops"),
 (80, 80, "■", "Receiver Coils"),
 (81, 81, "■", "Receiver Amplifiers"),
 (82, 82, "■", "Receiver Amplifiers and Indicators"),
 (83, 84, "■", "Compensating Networks"),
 (85, 85, "◆", "EM Field Systems for Ground Surveys"),
 (86, 88, "●", "Fixed vertical-loop transmitter"),
 (89, 89, "●", "Broadside (parallel-line) method"),
 (90, 91, "●", "Shoot-back method"),
 (92, 93, "●", "AFMAG method"),
 (94, 95, "●", "VLF method"),
 (96, 97, "●", "Turam method"),
 (98, 99, "●", "Moving source (horizontal-loop) method"),
 (100, 100, "■", "Time-Domain EM Ground Systems"),
 (101, 101, "●", "PEM (pulse EM)"),
 (102, 103, "●", "SIROTEM"),
 (104, 105, "●", "EM37"),
 (106, 107, "●", "UTEM"),
 (108, 108, "●", "Megasource transient EM"),
 (109, 109, "■", "Measurement of H"),
 (110, 110, "■", "Assessment of EM Ground Methods"),
 (112, 112, "◆", "Airborne EM Systems"),
 (113, 113, "■", "Quadrature Method and Turair System"),
 (114, 115, "■", "Airborne VLF"),
 (116, 121, "■", "Phase-Component Measurements"),
 (122, 124, "■", "Transient (Input) Method"),
 (125, 125, "■", "Cryogenic EM System and Assessment of Airborne EM"),
 (126, 126, "◆", "EM Field Procedures"),
 (128, 128, "■", "Interpretation: Introduction"),
 (129, 132, "●", "Analog model systems"),
 (133, 137, "●", "Dip-angle measurement: fixed vertical-loop transmitter"),
 (138, 139, "●", "Dip-angle measurement: broadside (parallel line)"),
 (140, 142, "●", "AFMAG and VLF results"),
 (143, 147, "●", "Measurement of phase components: horizontal loop"),
 (148, 153, "●", "Measurement of phase components: Turam"),
 (154, 160, "●", "Sheet conductors: miscellaneous considerations"),
 (161, 165, "●", "Sheet conductors: characteristic curves"),
 (166, 175, "●", "FDEM systems: ac circuit analysis"),
 (177, 177, "■", "Ground Systems: TDEM over Dipping Sheet"),
 (178, 186, "●", "PEM"),
 (187, 193, "●", "EM37"),
 (194, 206, "●", "SIROTEM"),
 (207, 213, "●", "UTEM"),
 (214, 216, "●", "Characteristic curves"),
 (217, 217, "■", "The Sphere Model in FD and TD Ground Systems"),
 (218, 219, "●", "Sphere model: frequency domain"),
 (220, 222, "●", "Sphere model: time domain"),
 (224, 224, "■", "Layered Structure: EM Depth Sounding"),
 (225, 237, "●", "Frequency-domain sounding"),
 (238, 243, "●", "Time-domain sounding"),
 (245, 245, "■", "Interpretation of Airborne EM Data"),
 (246, 246, "●", "Preliminary interpretation"),
 (247, 247, "■", "Turair"),
 (248, 253, "■", "Airborne VLF"),
 (254, 263, "■", "Phase-Component AEM"),
 (264, 271, "■", "Resistivity Mapping"),
 (272, 272, "■", "Input AEM"),
 (273, 279, "●", "Vertical-sheet response"),
 (280, 280, "●", "Dipping half-plane"),
 (281, 281, "●", "Conductive overburden"),
 (282, 282, "●", "Conducting sphere"),
 (283, 285, "●", "Mapping shallow structure"),
 (286, 288, "●", "Bathymetry"),
]
NEW = {}
for a, b, mk, name in R:
    for k in range(a, b + 1):
        NEW[k] = f"{mk}  {name}" + ("" if k == a else " (continued)")
k = 0
for fn in sorted(glob.glob("../sections/c*.js")):
    src = io.open(fn, encoding="utf-8").read()
    def sub(m):
        global k
        kind, title = m.group(1), m.group(2)
        new = NEW.get(k, title) if kind != "SEC" else title
        k += 1
        return f"{kind}('{new}'"
    src = re.sub(r"^(T|S|TB|SEC)\('([^']*)'", sub, src, flags=re.M)
    io.open(fn, "w", encoding="utf-8").write(src)
print("slides renamed:", len(NEW), "of", k)
