#!/bin/sh

# create distribution files
python3 setup.py sdist bdist_wheel

# upload files to pypi
twine upload dist/*

# create documentation from notebook
jupyter nbconvert README.ipynb --to markdown
