# Welcome to maser.data's documentation!

## Quickstart

To install the package, run the following command:

```
pip install maser.data --extra-index-url https://gitlab.obspm.fr/api/v4/projects/2440/packages/pypi/simple
```

Then use the `Data` class, a wrapper around several classes that allow you to read data from various formats,
including CDF, FITS, and some custom binary formats. By default, the class will try to automagically detect the
format of the file and use the appropriate class to read the data.

```python
from maser.data import Data

filepath = "path/to/my/data/file.ext"
data = Data(filepath=filepath)
```

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/git/https%3A%2F%2Fgitlab.obspm.fr%2Fmaser%2Fmaser4py.git/namespace) You can also launch a Binder environment and browse through the notebook [examples](https://gitlab.obspm.fr/maser/maser4py/-/tree/namespace/examples).

```{toctree}
---
caption: Contents
maxdepth: 2
---

sections/api

```

# Indices and tables

- [genindex](genindex)
- [modindex](modindex)
- [search](search)
