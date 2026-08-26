#!/usr/bin/env bash
# Extract a .docx (or .odt/.rtf) into readable Markdown + all media, for note-making.
# Usage: extract_source.sh <source.docx> <workdir>
# Produces: <workdir>/notes_pandoc.md   and   <workdir>/media/  (image1.png, ...)
# Then READ notes_pandoc.md fully to plan the section hierarchy.
set -e
SRC="$1"; WORK="${2:-./extract}"
mkdir -p "$WORK"
pandoc "$SRC" -f docx -t markdown+pipe_tables+grid_tables-raw_html \
  --extract-media="$WORK" --wrap=none -o "$WORK/notes_pandoc.md"
echo "== markdown =="; wc -l "$WORK/notes_pandoc.md"
echo "== headings =="; grep -nE '^#{1,4} ' "$WORK/notes_pandoc.md" | head -60
echo "== media =="; ls "$WORK"/media/ 2>/dev/null || ls "$WORK" | grep -iE 'png|jpe?g'
echo
echo "Next: inspect images (dimensions) to spot low-res crops; de-rotate any scanned"
echo "table photos and RE-TYPESET them; then organise into sections and write LaTeX."
