#!/bin/bash

# Test the package uploading in the test.pypi site.
# X.Bonnin - 20/12/2108

# Remove existing dist folder
rm -rf dist/

# Create wheel dist.
python setup.py sdist bdist_wheel

# Upload to test.pypi
twine upload --repository-url https://test.pypi.org/legacy/ dist/*