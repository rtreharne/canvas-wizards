#!/bin/bash

rm -rf docs
jupyter-book build book
cp -rf book/_build/html .
mv html/ docs/
touch docs/.nojekyll
mv docs/_sources/* docs/
git add -A
git commit -m "auto update from .deploy.sh"
while true; do
    read -p "Push to git repo?" yn
    case $yn in
        [Yy]* ) git push origin main; break;;
        [Nn]* ) exit;;
        * ) echo "Please answer yes or no.";;
    esac
done

git push origin main
