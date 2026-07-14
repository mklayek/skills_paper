#!/usr/bin/env python3
"""Build a pandoc reference.docx for methods read-docs:
  - the "Block Text" style (used by Markdown blockquotes) gets a rectangular border + light shading,
    so key-term blockquotes render as bordered boxes in Word;
  - the "Normal" style gets 1.15 line spacing.
Usage:  python3 make_refbox.py [out.docx]   (default: refbox15.docx)
Needs pandoc (system or pypandoc bundled).
"""
import sys, re, zipfile, subprocess, shutil, os, tempfile

OUT = sys.argv[1] if len(sys.argv) > 1 else "refbox15.docx"

def pandoc_path():
    if shutil.which("pandoc"):
        return "pandoc"
    import pypandoc
    return pypandoc.get_pandoc_path()

PB = pandoc_path()
tmp = tempfile.mkdtemp()
default = os.path.join(tmp, "reference.docx")
subprocess.run([PB, "-o", default, "--print-default-data-file", "reference.docx"], check=True)

zin = zipfile.ZipFile(default)
styles = zin.read("word/styles.xml").decode()

# 1) rectangular border + shading on Block Text (pandoc blockquote style)
pbdr = ('<w:pBdr>'
        '<w:top w:val="single" w:sz="8" w:space="6" w:color="333333"/>'
        '<w:left w:val="single" w:sz="8" w:space="6" w:color="333333"/>'
        '<w:bottom w:val="single" w:sz="8" w:space="6" w:color="333333"/>'
        '<w:right w:val="single" w:sz="8" w:space="6" w:color="333333"/></w:pBdr>'
        '<w:shd w:val="clear" w:color="auto" w:fill="F4F4F4"/>')
m = re.search(r'(<w:style [^>]*w:styleId="BlockText">.*?<w:pPr>)(.*?)(</w:pPr>)', styles, re.DOTALL)
if m:
    styles = styles[:m.end(1)] + pbdr + m.group(2) + styles[m.start(3):]
else:
    inject = ('<w:style w:type="paragraph" w:customStyle="1" w:styleId="BlockText">'
              '<w:name w:val="Block Text"/><w:basedOn w:val="Normal"/><w:pPr>' + pbdr +
              '<w:spacing w:before="120" w:after="120"/><w:ind w:left="120" w:right="120"/></w:pPr></w:style>')
    styles = styles.replace("</w:styles>", inject + "</w:styles>")

# 2) 1.15 line spacing on Normal (line=276, lineRule=auto ; 240 = single, 276 = 1.15)
sp = '<w:spacing w:line="276" w:lineRule="auto" w:after="120"/>'
mn = re.search(r'(<w:style [^>]*w:styleId="Normal">.*?<w:pPr>)(.*?)(</w:pPr>)', styles, re.DOTALL)
if mn:
    body = re.sub(r'<w:spacing[^/]*/>', '', mn.group(2))
    styles = styles[:mn.end(1)] + sp + body + styles[mn.start(3):]
else:
    m2 = re.search(r'(<w:style [^>]*w:styleId="Normal">)(.*?)(</w:style>)', styles, re.DOTALL)
    styles = styles[:m2.end(1)] + '<w:pPr>' + sp + '</w:pPr>' + m2.group(2) + styles[m2.start(3):]

with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as zout:
    for it in zin.namelist():
        zout.writestr(it, styles.encode() if it == "word/styles.xml" else zin.read(it))
zin.close()
s = zipfile.ZipFile(OUT).read("word/styles.xml").decode()
print(f"wrote {OUT} | border={'w:pBdr' in s} | 1.15-spacing={'w:line=\"276\"' in s}")
