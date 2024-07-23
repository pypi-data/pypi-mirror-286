# Sequence, alignments and phylogeny utilities

Python package providing utilities for:
- sequences (nucleotides or amino acids)
- alignments
- phylogeny

## Creating the pip package and upload

See Generating distribution archive from this [page](https://packaging.python.org/tutorials/packaging-projects/).

Go to the directory containing the `*.toml` file and run:
```bash
python3 -m pip install --upgrade build

python3 -m build
```

## Upload of the new or updated package

### upload to the TestPyPi repository

Use Twine to upload the new package or the new version of the package to [TestPyPi](https://test.pypi.org/):
```bash
python3 -m twine upload --repository testpypi dist/*
```
When prompted for the username, enter `__token__` and the password of the token for `test.pypi.org`.

To test if the package is correctly uploaded and functional, create a virtual env and install the package.

```bash
# virtual env
python3 -m venv test_env
source test_env/bin/activate

# download package
python -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple viro-seq-utils

# launch Python
python
``` 

Test the package:
```python
from viro_seq_utils import aln_utils
```
The upload is OK if no error message is displayed.

Remove the virtual environment:
```bash
deactivate

rm -r test_env/
```

### upload to the PyPi repository

Use Twine to upload the new package or the new version of the package to [PyPi](https://pypi.org/):
```bash
python3 -m twine upload dist/*
```

When prompted for thr username, enter `__token__` and the password of the token: `pypi.org`.

