# publish

1. modify version in `setup.py`
2. `rm -rf dist && python setup.py sdist`
3. `twine upload dist/*`