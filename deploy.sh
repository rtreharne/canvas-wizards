#!/bin/bash

rm -rf docs
jupyter-book build book
cp -rf book/_build/html .
mv html/ docs/
touch docs/.nojekyll
mv docs/_sources/* docs/
git add -A
git commit -m 'updating!'
git push origin main
