# -*- coding: utf-8 -*-
"""v2 coverage rule: every source equation (eqinv.json) and every chapter figure must be in the deck.

Also writes ../extract/annotated.md: the chapter text with each display equation replaced by
[EQ#id] so slides can reference it as '§#id'.
"""
import glob, io, json, re, sys
sys.stdout = io.open(1, "w", encoding="utf-8", closefd=False)
import json as _j; CFG = _j.load(open("deck_config.json", encoding="utf-8"))   # per-deck settings
SRC = CFG["source_md"]
t = io.open(SRC, encoding="utf-8").read()
inv = json.load(io.open("eqinv.json", encoding="utf-8"))
k = iter(range(1, 10 ** 6))
ann = re.sub(r"\$\$(.+?)\$\$", lambda m: f"[EQ#{next(k)}] $${m.group(1).strip()}$$", t, flags=re.S)
ann = re.sub(r"!\[[^\]]*\]\((?:\.\./)?figs/(fig_[\w]+)\.\w+\)", r"[FIG \1]", ann)
io.open("../extract/annotated.md", "w", encoding="utf-8").write(ann)

src = "".join(io.open(f, encoding="utf-8").read() for f in sorted(glob.glob("../sections/c*.js")))
used_eq = {int(x) for x in re.findall(r"'§#(\d+)'", src)}
figs = set(re.findall(r"figs/(fig_[\w]+)\.\w+", t))
used_fig = set(re.findall(r"'(fig_[\w]+)'", src))
miss_eq = sorted({e["id"] for e in inv} - used_eq)
miss_fig = sorted(figs - used_fig, key=lambda s: [int(x) if x.isdigit() else x for x in re.findall(r"\d+|[a-z]+$", s)])
dup = [f for f in used_fig if len(re.findall(f"'{f}'", src)) > 1]
print(f"🧮 equations: {len(used_eq & {e['id'] for e in inv})}/{len(inv)} used" + (f", ❌ missing {len(miss_eq)}: {miss_eq}" if miss_eq else ", ✅ none missing"))
print(f"🖼️ figures: {len(used_fig & figs)}/{len(figs)} used" + (f", ❌ unused {len(miss_fig)}: {miss_fig}" if miss_fig else ", ✅ none unused"))
if dup: print("⚠️ figures used twice:", dup)
semi = [l.strip()[:90] for l in src.splitlines() if ";" in re.sub(r"'[^']*›[^']*'|^\s*//.*|;\s*$|\);\s*$", "", l)
        and re.search(r"'[^']*;[^']*'", l) and "›" not in l]
if semi: print(f"⚠️ semicolons in slide text: {len(semi)}", *semi[:8], sep="\n   ")
