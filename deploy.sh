#!/bin/bash

# create documentation from notebook
jupyter nbconvert README.ipynb --to markdown

poetry build
poetry publish

