#!/bin/bash

# create documentation from notebook
jupyter nbconvert README.ipynb --to markdown

source pypi_credentials.sh
echo "Using username: $PYPI_USERNAME"

poetry build
poetry publish --username $PYPI_USERNAME --password $PYPI_PASSWORD

