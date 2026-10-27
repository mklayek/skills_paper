# -*- coding: utf-8 -*-
"""Color each native equation: left-hand side and right-hand side in different colors,
alternating between two color sets on successive equations (v3 rule).

Set A: LHS black, RHS deep blue.  Set B: LHS dark red, RHS green.
The split is at the first relation sign (=, ≈, ≤, ≥, ∝, ...) at the top level of the math,
row by row inside aligned (eqArr) blocks. With no relation sign, the whole equation takes the LHS color.
"""
import copy
from lxml import etree

M = "http://schemas.openxmlformats.org/officeDocument/2006/math"
A = "http://schemas.openxmlformats.org/drawingml/2006/main"
SETS = [("000000", "1E3A8A"), ("991B1B", "16A34A")]
REL = "=≈≤≥∝≡≃≅≪≫<>"
q = lambda tag: "{%s}%s" % (M, tag)


def paint(el, color):
    for c in el.iter("{%s}srgbClr" % A):
        c.set("val", color)


def first_rel(run):
    t = run.find(q("t"))
    if t is None or not t.text: return -1
    for k, ch in enumerate(t.text):
        if ch in REL: return k
    return -1


def split_run(run, k):
    """Split an m:r at character k: returns (before, rel_and_after)."""
    t = run.find(q("t")); txt = t.text
    if k == 0: return None, run
    left = copy.deepcopy(run); left.find(q("t")).text = txt[:k]
    t.text = txt[k:]
    run.addprevious(left)
    return left, run


def color_seq(children, lhs, rhs):
    side = "L"
    for ch in list(children):
        tag = etree.QName(ch).localname
        if tag in ("rPr", "ctrlPr", "oMathParaPr", "eqArrPr", "dPr"):
            continue
        if tag == "eqArr":
            for row in ch.findall(q("e")):
                color_seq(row, lhs, rhs)
            continue
        if side == "L" and tag == "d" and ch.find(".//" + q("eqArr")) is not None:
            paint(ch, lhs)                      # brackets keep the LHS color
            for e in ch.findall(q("e")):
                color_seq(e, lhs, rhs)
            continue
        if side == "L" and tag == "r":
            k = first_rel(ch)
            if k >= 0:
                left, right = split_run(ch, k)
                if left is not None: paint(left, lhs)
                paint(right, rhs); side = "R"
                continue
        paint(ch, lhs if side == "L" else rhs)


def color_equation(el, n):
    lhs, rhs = SETS[n % 2]
    for om in el.iter(q("oMath")):
        color_seq(om, lhs, rhs)
