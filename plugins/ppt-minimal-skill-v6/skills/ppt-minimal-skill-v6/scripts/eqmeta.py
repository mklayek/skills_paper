import re, json, omml, os
INV = {e["id"]: e["latex"] for e in json.load(open("eqinv.json", encoding="utf-8"))}
if os.path.exists("eqfix.json"):
    INV.update({int(k): v for k, v in json.load(open("eqfix.json", encoding="utf-8")).items()})


def latex_size(l):
    """Rough built-up width (em) and whether the source equation stacks (fractions, limits)."""
    tall = bool(re.search(r"\\(?:d?frac|int|oint|sum|sqrt|prod|lim|begin)", l))
    s = re.sub(r"\\(?:mathbf|boldsymbol|mathrm|text|operatorname|left|right|quad|qquad|,|;|!)", "", l)
    s = re.sub(r"\\d?frac\{([^{}]*)\}\{([^{}]*)\}", lambda m: max(m.group(1), m.group(2), key=len), s)
    s = re.sub(r"\\[A-Za-z]+", "x", s)
    s = re.sub(r"[_^]\{([^{}]*)\}", lambda m: m.group(1)[: max(1, len(m.group(1)) // 2)], s)
    s = re.sub(r"[{}\s]", "", s)
    return len(s) * 0.9, tall


src = open('deck.js', encoding='utf-8').read()
meta = {}
for raw in re.findall(r"'(§[^']*)'", src):
    if raw.startswith('§#'):
        if not raw[2:].isdigit(): continue
        w, tall = latex_size(INV[int(raw[2:])]); meta[raw] = [round(w, 1), tall]; continue
    label, math, eqno = omml.split_line(raw)
    w, tall = omml.width(math)
    meta[raw] = [round(w + (len(label) + 2 if label else 0), 1), tall]
json.dump(meta, open('eqmeta.json', 'w', encoding='utf-8'), ensure_ascii=False)
print('equations found:', len(meta))
