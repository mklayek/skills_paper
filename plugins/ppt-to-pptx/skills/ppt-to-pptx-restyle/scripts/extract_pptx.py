# -*- coding: utf-8 -*-
"""Extract verbatim per-slide text + every per-slide image from a .pptx.
Usage:  python extract_pptx.py <src.pptx> <out_dir>
  -> <out>/text/all_text.md         (verbatim text, per slide, incl. speaker notes)
  -> <out>/figures/slideNN_rMM.ext  (all images referenced by each slide, via slide rels)
Images are pulled from slide.part.rels (reltype 'image'), which catches grouped/embedded
images that a picture-shape walk misses. Deduped per slide by content hash; tiny (<60px)
decorations skipped.
"""
import os, sys, hashlib
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE
from PIL import Image

SRC, OUT = sys.argv[1], sys.argv[2]
FIG = os.path.join(OUT, "figures"); os.makedirs(FIG, exist_ok=True)
os.makedirs(os.path.join(OUT, "text"), exist_ok=True)

def texts_of(slide):
    out = []
    def walk(shapes):
        for sh in shapes:
            if sh.shape_type == MSO_SHAPE_TYPE.GROUP:
                walk(sh.shapes); continue
            if sh.has_text_frame:
                for p in sh.text_frame.paragraphs:
                    out.append((p.level or 0, ("".join(r.text for r in p.runs) or p.text)))
            if sh.has_table:
                for row in sh.table.rows:
                    out.append((0, " | ".join(c.text for c in row.cells)))
    walk(slide.shapes)
    return out

def images_of(slide, i):
    seen, paths = set(), []
    for rel in slide.part.rels.values():
        if "image" not in rel.reltype: continue
        try: blob = rel.target_part.blob
        except Exception: continue
        h = hashlib.md5(blob).hexdigest()
        if h in seen: continue
        seen.add(h)
        ext = rel.target_part.partname.ext.lstrip(".").lower()
        if ext == "gif": continue
        name = os.path.join(FIG, f"slide{i:02d}_r{len(paths)+1:02d}.{ext}")
        with open(name, "wb") as f: f.write(blob)
        try:
            w, hh = Image.open(name).size
            if max(w, hh) < 60: os.remove(name); continue
        except Exception:
            os.remove(name); continue
        paths.append(name)
    return paths

prs = Presentation(SRC)
lines, nimg = ["# Full text extraction\n"], 0
for i, slide in enumerate(prs.slides, 1):
    lines.append(f"\n## Slide {i}\n")
    for _, t in texts_of(slide):
        if t and t.strip(): lines.append(t)
    if slide.has_notes_slide and slide.notes_slide.notes_text_frame:
        n = slide.notes_slide.notes_text_frame.text.strip()
        if n: lines.append(f"\n> [Speaker notes] {n}")
    nimg += len(images_of(slide, i))

with open(os.path.join(OUT, "text", "all_text.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print("slides:", len(prs.slides), "| images extracted:", nimg)
print("text ->", os.path.join(OUT, "text", "all_text.md"))
print("figures ->", FIG)
