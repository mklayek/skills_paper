# -*- coding: utf-8 -*-
"""Source equations (LaTeX from the chapter) -> PowerPoint OMML, via pandoc's docx writer.

Reads eqinv.json (+ eqfix.json overrides {id: latex}), writes eqomml.json {id: oMathPara xml}
styled for pptx (Cambria Math, size and color from omml.Style), left aligned.
"""
import io, json, os, re, subprocess, sys, zipfile
from lxml import etree
import omml

sys.stdout = io.open(1, "w", encoding="utf-8", closefd=False)
M = "http://schemas.openxmlformats.org/officeDocument/2006/math"
W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
A = "http://schemas.openxmlformats.org/drawingml/2006/main"
SZ = 2200


def latex_of():
    inv = json.load(io.open("eqinv.json", encoding="utf-8"))
    fix = {}
    if os.path.exists("eqfix.json"):
        fix = {int(k): v for k, v in json.load(io.open("eqfix.json", encoding="utf-8")).items()}
    return {e["id"]: fix.get(e["id"], e["latex"]) for e in inv}


def clean(lat):
    # pandoc's texmath does not know a few OCR-era spellings
    lat = lat.replace("\\operatorname*", "\\operatorname").replace("\\displaystyle", "")
    lat = re.sub(r"\\(?:big|Big|bigg|Bigg)([lr]?)", r"", lat)
    return lat


def rpr(italic, bold):
    return etree.fromstring(
        f'<a:rPr xmlns:a="{A}" lang="en-US" sz="{SZ}" b="{1 if bold else 0}" i="{1 if italic else 0}">'
        f'<a:solidFill><a:srgbClr val="0B2A55"/></a:solidFill>'
        f'<a:latin typeface="Cambria Math" panose="02040503050406030204" pitchFamily="18" charset="0"/>'
        f'<a:cs typeface="Cambria Math" panose="02040503050406030204" pitchFamily="18" charset="0"/></a:rPr>')


def restyle(om):
    for wr in om.iter(f"{{{W}}}rPr"):
        wr.getparent().remove(wr)
    for r in om.iter(f"{{{M}}}r"):
        sty = r.find(f"{{{M}}}rPr/{{{M}}}sty")
        v = sty.get(f"{{{M}}}val") if sty is not None else "i"
        t = r.find(f"{{{M}}}t")
        r.insert(list(r).index(t), rpr(v in ("i", "bi"), v in ("b", "bi")))
    for c in om.iter(f"{{{M}}}ctrlPr"):
        for k in list(c):
            c.remove(k)
        c.append(rpr(True, False))
    return om


def main():
    lat = latex_of()
    md = "\n\n".join(f"EQMARK{i}\n\n$${clean(l)}$$" for i, l in sorted(lat.items())) + "\n"
    io.open("_eqs.md", "w", encoding="utf-8").write(md)
    r = subprocess.run(["pandoc", "_eqs.md", "-f", "markdown", "-o", "_eqs.docx"], capture_output=True, text=True, encoding="utf-8")
    if r.stderr.strip():
        print("⚠️ pandoc:", r.stderr.strip()[:2000])
    doc = etree.fromstring(zipfile.ZipFile("_eqs.docx").read("word/document.xml"))
    out, cur, bad = {}, None, []
    for p in doc.iter(f"{{{W}}}p"):
        txt = "".join(p.itertext()).strip()
        oms = p.findall(f".//{{{M}}}oMath")
        if not oms and txt.startswith("EQMARK"):
            cur = int(txt[6:]); continue
        if oms and cur is not None:
            om = restyle(oms[0])
            xml = etree.tostring(om, encoding="unicode")
            out[cur] = (f'<m:oMathPara xmlns:m="{M}" xmlns:a="{A}"><m:oMathParaPr><m:jc m:val="left"/></m:oMathParaPr>'
                        + re.sub(r' xmlns:\w+="[^"]+"', "", xml).replace("<m:oMath>", "<m:oMath>", 1) + "</m:oMathPara>")
            cur = None
    for i in lat:
        if i not in out:
            bad.append(i)
    json.dump(out, io.open("eqomml.json", "w", encoding="utf-8"), ensure_ascii=False)
    print(f"✅ {len(out)} source equations converted to OMML" + (f", ❌ missing {bad}" if bad else ""))


if __name__ == "__main__":
    main()
