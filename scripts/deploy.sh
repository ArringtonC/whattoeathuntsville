#!/bin/sh
# Builds the public preview and publishes it to the gh-pages branch (GitHub Pages).
# Remove PUBLIC_SHOW_DRAFTS at launch so only reviewed restaurants go live.
set -e
export SITE_URL=https://arringtonc.github.io BASE_PATH=/whattoeathuntsville PUBLIC_SHOW_DRAFTS=true
npm run build
touch dist/.nojekyll   # keep GitHub from hiding the _astro folder
cd dist
git init -q -b gh-pages
git add -A
git -c user.name="Arrington Copeland" -c user.email="arrington.copeland@gmail.com" commit -q -m "Deploy $(date -u +%Y-%m-%dT%H:%MZ)"
git push -fq https://github.com/ArringtonC/whattoeathuntsville.git gh-pages
rm -rf .git
echo "Published: https://arringtonc.github.io/whattoeathuntsville/"
