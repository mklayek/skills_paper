#!/bin/bash
# v8 build: font widths, assemble deck.js, source-equation OMML, equation metadata, pptxgenjs (pooled 22 pt fill),
# bullets, native equations, Markdown copy, then the frame slides only when deck_config.json has "frame": true.
set -e
cd "$(dirname "$0")"
[ -f fontwidths.json ] || python fontwidths.py
bash assemble.sh
python latexomml.py
python eqmeta.py
node deck.js
python post.py Deck.pptx
cp Deck.pptx Deck_linear.pptx
python inject.py Deck.pptx
node deck_md.js
if python -c "import json,sys;sys.exit(0 if json.load(open('deck_config.json')).get('frame') else 1)"; then
  python frame.py Deck.pptx Final.pptx
  echo "deliver: Final.pptx (title slide + content + Thank you slide)"
else
  echo "deliver: Deck.pptx (no frame slides, deck_config.json frame=false)"
fi
