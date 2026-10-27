#!/bin/bash
# Assemble deck.js from the template and the section sources.
cd "$(dirname "$0")"
{ cat head.js; for f in ../sections/c*.js; do cat "$f"; echo; done
  echo "pres.writeFile({fileName:'Deck.pptx'}).then(()=>{ fs.writeFileSync('eqlist.json',JSON.stringify(EQL)); fs.writeFileSync('est.json',JSON.stringify(EST)); fs.writeFileSync('keys.json',JSON.stringify(KEYS)); });"; } > deck.js
