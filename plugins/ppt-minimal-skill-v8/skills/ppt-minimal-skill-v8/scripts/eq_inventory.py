# -*- coding: utf-8 -*-
"""Every display equation in the chapter master Markdown -> eqinv.json (id, page, section, latex, context)."""
import io, json, re, sys
sys.stdout = io.open(1, "w", encoding="utf-8", closefd=False)
import json as _j; CFG = _j.load(open("deck_config.json", encoding="utf-8"))   # per-deck settings
SRC = CFG["source_md"]
t = io.open(SRC, encoding="utf-8").read()
out, page, sec = [], None, ""
for m in re.finditer(r"<!-- p\.(\d+) -->|^(#{1,4} [^\n]+)$|\$\$(.+?)\$\$", t, re.S | re.M):
    if m.group(1):
        page = int(m.group(1)); continue
    if m.group(2):
        sec = m.group(2).strip("# ").strip(); continue
    raw = m.group(3).strip()
    tag = re.search(r"\\tag\{([^}]*)\}", raw)
    lat = re.sub(r"\\tag\{[^}]*\}", "", raw).strip()
    lat = re.sub(r"\\q?quad\s*\(?7\.\d+[a-z]?\)?\s*$", "", lat).strip()
    lat = re.sub(r"\(\s*7\.\d+[a-z]?\s*\)\s*$", "", lat).strip()
    ctx = re.sub(r"\s+", " ", t[max(0, m.start() - 300):m.start()])[-300:]
    out.append({"id": len(out) + 1, "page": page, "sec": sec, "tag": tag.group(1) if tag else "", "latex": lat, "ctx": ctx})
json.dump(out, io.open("eqinv.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print(len(out), "equations,", sum(1 for e in out if e["tag"]), "tagged")
