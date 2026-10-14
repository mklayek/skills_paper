#!/bin/bash
# Build the EM deck: assemble deck.js, source-equation OMML, equation metadata, pptxgenjs, bullets, native equations.
set -e
cd "$(dirname "$0")"
bash assemble.sh
python latexomml.py
python eqmeta.py
node deck.js
python post.py Deck.pptx
cp Deck.pptx Deck_linear.pptx
python inject.py Deck.pptx
node deck_md.js
# deliver: cp Deck.pptx "../../../$(python -c "import json;print(json.load(open('deck_config.json'))['deck_name'])").pptx"
