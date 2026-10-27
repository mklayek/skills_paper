"""Convert the deck's linear equation strings (Unicode + _{}/^{} markup) into OMML.
Linear rules follow UnicodeMath build-up: '/' takes the adjacent operands; a bracket group
that is a whole operand loses its brackets; sum/integral take limits from _{} ^{} and the
next term as body."""
import re
from xml.sax.saxutils import escape

M = 'http://schemas.openxmlformats.org/officeDocument/2006/math'
A = 'http://schemas.openxmlformats.org/drawingml/2006/main'

SUPD = {'²': '2', '³': '3', '⁴': '4', '⁵': '5', '⁻': '−', '¹': '1', '⁰': '0', 'ᵐ': 'm'}
SUBD = {'₀': '0', '₁': '1', '₂': '2', '₃': '3', '₄': '4'}
OPS = set('+−=≈→⇒×·,;±<>≫≪≡:~')
FUNCS = ['tan', 'cos', 'sin', 'ln', 'exp']
OPEN = {'(': ')', '[': ']', '{': '}'}


def pre(s):
    out = []; q = False; i = 0
    while i < len(s):
        c = s[i]
        if c == '"':
            q = not q; out.append(c); i += 1; continue
        if not q and c in SUPD:
            j = i; buf = ''
            while j < len(s) and s[j] in SUPD:
                buf += SUPD[s[j]]; j += 1
            out.append('^{' + buf + '}'); i = j; continue
        if not q and c in SUBD:
            out.append('_{' + SUBD[c] + '}'); i += 1; continue
        out.append(c); i += 1
    return ''.join(out)


def tokenize(s):
    t = []; i = 0
    while i < len(s):
        c = s[i]
        if c == '"':
            j = s.index('"', i + 1); t.append(('text', s[i + 1:j])); i = j + 1; continue
        if c in '_^' and i + 1 < len(s) and s[i + 1] == '{':
            d = 0; j = i + 1
            while True:
                if s[j] == '{': d += 1
                elif s[j] == '}':
                    d -= 1
                    if d == 0: break
                j += 1
            t.append(('sub' if c == '_' else 'sup', s[i + 2:j])); i = j + 1; continue
        if c == ' ':
            j = i
            while j < len(s) and s[j] == ' ': j += 1
            t.append(('sp', j - i)); i = j; continue
        if c in OPEN: t.append(('open', c)); i += 1; continue
        if c in ')]}': t.append(('close', c)); i += 1; continue
        if c == '/': t.append(('slash', c)); i += 1; continue
        if c in '∑∫': t.append(('nary', c)); i += 1; continue
        if c in OPS: t.append(('op', c)); i += 1; continue
        if c.isdigit():
            j = i
            while j < len(s) and (s[j].isdigit() or (s[j] == '.' and j + 1 < len(s) and s[j + 1].isdigit())): j += 1
            t.append(('num', s[i:j])); i = j; continue
        f = next((f for f in FUNCS if s.startswith(f, i) and not (i > 0 and s[i - 1].isalpha())), None)
        if f and (i + len(f) >= len(s) or not s[i + len(f)].isalpha() or s[i + len(f)] in 'θ'):
            t.append(('func', f)); i += len(f); continue
        if c in '′″*' and t and t[-1][0] in ('id',):
            t[-1] = ('id', t[-1][1] + c); i += 1; continue
        if s.startswith('···', i): t.append(('id', '⋯')); i += 3; continue
        t.append(('id', c)); i += 1
    return t


class Atom:
    def __init__(self, kind, val):
        self.kind, self.val, self.sub, self.sup = kind, val, None, None


def parse(tokens, pos=0, close=None, noscript_frac=False):
    items = []
    while pos < len(tokens):
        k, v = tokens[pos]
        if k == 'close':
            if close is None:
                items.append(Atom('cl', v)); pos += 1; continue
            return items, pos + 1
        if k == 'open':
            p0 = pos
            inner, pos = parse(tokens, pos + 1, OPEN[v], noscript_frac)
            a = Atom('group', inner); a.br = v
            a.open_only = not (pos - 1 < len(tokens) and tokens[pos - 1][0] == 'close' and pos - 1 > p0 and _closes(tokens, p0, pos - 1))
            items.append(a); continue
        if k in ('sub', 'sup') and items and isinstance(items[-1], Atom):
            sc, _ = parse(tokenize(v), 0, None, True)
            if k == 'sub': items[-1].sub = sc
            else: items[-1].sup = sc
            pos += 1; continue
        if k in ('id', 'num', 'func', 'text', 'nary'):
            items.append(Atom(k, v)); pos += 1; continue
        items.append((k, v)); pos += 1
    return items, pos


def _closes(tokens, a, b):
    d = 0
    for k, v in tokens[a:b + 1]:
        if k == 'open': d += 1
        elif k == 'close': d -= 1
    return d == 0


def is_atom(x):
    return isinstance(x, Atom)


def build(items, frac=True):
    for x in items:
        if is_atom(x):
            if x.kind == 'group': x.val = build(x.val, frac)
            for sc in ('sub', 'sup'):
                if getattr(x, sc) is not None: setattr(x, sc, build(getattr(x, sc), False))
    if frac:
        while any(not is_atom(x) and x[0] == 'slash' for x in items):
            i = next(i for i, x in enumerate(items) if not is_atom(x) and x[0] == 'slash')
            a = i
            while a - 1 >= 0 and is_atom(items[a - 1]) and items[a - 1].kind not in ('nary', 'cl'): a -= 1
            b = i + 1
            while b < len(items) and is_atom(items[b]) and items[b].kind not in ('nary', 'cl'): b += 1
            num, den = items[a:i], items[i + 1:b]
            f = Atom('frac', (strip(num), strip(den)))
            items = items[:a] + [f] + items[b:]
    else:
        items = [('op', '/') if (not is_atom(x) and x[0] == 'slash') else x for x in items]
    out = nary_pass(items)
    res = []
    for x in out:
        if is_atom(x) and x.kind == 'group' and x.sub is None and x.sup is None and len(x.val) == 1 and is_atom(x.val[0]) and x.val[0].kind == 'frac':
            res.append(x.val[0])
        else:
            res.append(x)
    return res


def nary_pass(items):
    out = []; i = 0
    while i < len(items):
        x = items[i]
        if is_atom(x) and x.kind == 'nary' and not hasattr(x, 'body'):
            j = i + 1
            while j < len(items) and not is_atom(items[j]) and items[j][0] == 'sp': j += 1
            k = j
            while k < len(items) and not (not is_atom(items[k]) and items[k][0] == 'op' and items[k][1] in '+−=≈,;→'):
                k += 1
            body = items[j:k]
            while body and not is_atom(body[-1]) and body[-1][0] == 'sp': body.pop()
            x.body = nary_pass(body)
            out.append(x); i = k; continue
        out.append(x); i += 1
    return out


def strip(ops):
    if len(ops) == 1 and is_atom(ops[0]) and ops[0].kind == 'group' and ops[0].sub is None and ops[0].sup is None:
        return ops[0].val
    return ops


class Style:
    def __init__(self, target, sz=2200, color='0B2A55'):
        self.target, self.sz, self.color = target, sz, color

    def rpr(self, italic=True):
        if self.target == 'pptx':
            return (f'<a:rPr lang="en-US" sz="{self.sz}" b="0" i="{1 if italic else 0}"><a:solidFill><a:srgbClr val="{self.color}"/></a:solidFill>'
                    f'<a:latin typeface="Cambria Math" panose="02040503050406030204" pitchFamily="18" charset="0"/>'
                    f'<a:cs typeface="Cambria Math" panose="02040503050406030204" pitchFamily="18" charset="0"/></a:rPr>')
        return '<w:rPr><w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math"/></w:rPr>'

    def ctrl(self):
        return f'<m:ctrlPr>{self.rpr()}</m:ctrlPr>'


def run(txt, st, plain=False):
    mr = '<m:rPr><m:sty m:val="p"/></m:rPr>' if plain else ''
    return f'<m:r>{mr}{st.rpr(not plain)}<m:t xml:space="preserve">{escape(txt)}</m:t></m:r>'


def emit(items, st):
    out = []
    prev_atom = False
    for x in items:
        if not is_atom(x):
            k, v = x
            if k == 'sp':
                if v >= 2: out.append(run(' ' * (1 if v < 6 else 2), st, True))
                elif prev_atom: out.append(run(' ', st, True))
                continue
            if k == 'op':
                out.append(run(v, st, True)); prev_atom = False; continue
            out.append(run(v, st, True)); prev_atom = False; continue
        out.append(atom(x, st)); prev_atom = True
    return ''.join(out)


def base(x, st):
    if x.kind == 'id':
        return run(x.val, st)
    if x.kind == 'num':
        return run(x.val, st, True)
    if x.kind in ('func', 'cl'):
        return run(x.val, st, True)
    if x.kind == 'text':
        return run(x.val, st, True)
    if x.kind == 'group':
        b = x.br; e = '' if getattr(x, 'open_only', False) else OPEN[b]
        return (f'<m:d><m:dPr><m:begChr m:val="{escape(b)}"/><m:endChr m:val="{escape(e)}"/>{st.ctrl()}</m:dPr>'
                f'<m:e>{emit(x.val, st)}</m:e></m:d>')
    if x.kind == 'frac':
        n, d = x.val
        return f'<m:f><m:fPr>{st.ctrl()}</m:fPr><m:num>{emit(n, st)}</m:num><m:den>{emit(d, st)}</m:den></m:f>'
    if x.kind == 'nary':
        lim = 'undOvr' if x.val == '∑' else 'subSup'
        hide = ('<m:subHide m:val="1"/>' if x.sub is None else '') + ('<m:supHide m:val="1"/>' if x.sup is None else '')
        sub = emit(x.sub, st) if x.sub else ''
        sup = emit(x.sup, st) if x.sup else ''
        body = emit(getattr(x, 'body', []) or [], st)
        return (f'<m:nary><m:naryPr><m:chr m:val="{x.val}"/><m:limLoc m:val="{lim}"/>{hide}{st.ctrl()}</m:naryPr>'
                f'<m:sub>{sub}</m:sub><m:sup>{sup}</m:sup><m:e>{body}</m:e></m:nary>')
    raise ValueError(x.kind)


def atom(x, st):
    if x.kind == 'nary':
        return base(x, st)
    b = base(x, st)
    if x.sub is not None and x.sup is not None:
        return f'<m:sSubSup><m:sSubSupPr>{st.ctrl()}</m:sSubSupPr><m:e>{b}</m:e><m:sub>{emit(x.sub, st)}</m:sub><m:sup>{emit(x.sup, st)}</m:sup></m:sSubSup>'
    if x.sub is not None:
        return f'<m:sSub><m:sSubPr>{st.ctrl()}</m:sSubPr><m:e>{b}</m:e><m:sub>{emit(x.sub, st)}</m:sub></m:sSub>'
    if x.sup is not None:
        return f'<m:sSup><m:sSupPr>{st.ctrl()}</m:sSupPr><m:e>{b}</m:e><m:sup>{emit(x.sup, st)}</m:sup></m:sSup>'
    return b


LABEL = re.compile(r'^(Medium \(\d\):|Step \d:|\((?:i|ii|iii|iv|v)\))\s+')
EQNO = re.compile(r'\s+\((\d+[a-e]?(?:,\s*[a-e])?)\)\s*$')


def split_line(raw):
    """raw '§ ...' item -> (label, math, eqno). This deck carries NO equation numbers."""
    s = raw[1:].strip()
    label = None; eqno = None
    m = LABEL.match(s)
    if m: label = m.group(1); s = s[m.end():]
    return label, s.rstrip(), eqno


def to_omml(math, st, label=None, eqno=None, para=False):
    toks = tokenize(pre(math))
    items, _ = parse(toks)
    items = build(items)
    lead = ''
    if math.startswith('    '):
        lead = run('  ', st, True)
    lab = run(label + ' ', st, True) if label else ''
    num = run('  (' + eqno + ')', st, True) if eqno else ''
    body = f'<m:oMath>{lab}{lead}{emit(items, st)}{num}</m:oMath>'
    if para:
        return (f'<m:oMathPara xmlns:m="{M}"><m:oMathParaPr><m:jc m:val="left"/></m:oMathParaPr>' + body + '</m:oMathPara>')
    return body.replace('<m:oMath>', f'<m:oMath xmlns:m="{M}">', 1)


def width(math):
    items = build(parse(tokenize(pre(math)))[0])
    def w(xs):
        t = 0
        for x in xs:
            if not is_atom(x):
                t += (1.6 if x[0] == 'op' else (1.5 if x[0] == 'sp' and x[1] >= 2 else 0.3 if x[0] == 'sp' else 1)); continue
            t += wa(x)
        return t
    def wa(x):
        if x.kind in ('id', 'num', 'func', 'text', 'cl'): b = len(x.val)
        elif x.kind == 'group': b = w(x.val) + 2
        elif x.kind == 'frac': b = max(w(x.val[0]), w(x.val[1])) + 0.6
        elif x.kind == 'nary': b = 1.6 + w(getattr(x, 'body', []) or [])
        s = max(w(x.sub) if x.sub else 0, w(x.sup) if x.sup else 0) * 0.65
        return b + s
    def tall(xs):
        for x in xs:
            if is_atom(x):
                if x.kind == 'frac': return True
                if x.kind == 'nary' and (x.sub or x.sup): return True
                if x.kind == 'group' and tall(x.val): return True
                if x.kind == 'nary' and tall(getattr(x, 'body', []) or []): return True
        return False
    return w(items), tall(items)
