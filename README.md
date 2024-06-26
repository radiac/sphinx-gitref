# Sphinx Gitref

[![PyPI](https://img.shields.io/pypi/v/sphinx-gitref.svg)](https://pypi.org/project/sphinx-gitref/)
[![Documentation](https://readthedocs.org/projects/sphinx-gitref/badge/?version=latest)](https://sphinx-gitref.readthedocs.io/en/latest/)
[![Tests](https://github.com/radiac/sphinx-gitref/actions/workflows/ci.yml/badge.svg)](https://github.com/radiac/sphinx-gitref/actions/workflows/ci.yml)
[![Coverage](https://codecov.io/gh/radiac/sphinx-gitref/branch/main/graph/badge.svg?token=Q9AKPHRJF5)](https://codecov.io/gh/radiac/sphinx-gitref)

Keep your sphinx docs in sync with your code.

Adds a `` :gitref:`..` `` role to Sphinx to link to your code on GitHub, GitLab or
Bitbucket, and to make sure the references in your docs match the code.

Key features:

* Check code referenced in documentation still exists
* Check code hashes and alert when something has changed
* Link to source code on github
* Incorporate into tests or git hooks

Supports Python 3.7+

## Quickstart

### Installation

Install:

```bash
pip install sphinx-gitref
```

In your Sphinx ``conf.py``, add ``sphinx_gitref`` to the ``extensions`` list:

```python
extensions = [
    ...
    'sphinx_gitref',
]
```

See
[Configuration](https://sphinx-gitref.readthedocs.io/en/latest/install.html#configuration)
for options to customise gitref's defaults.


### In reStructuredText

You can then use the `` :gitref:`..` `` role to link to a file on GitHub, GitLab,
Bitbucket, or your own remote git service:

```
This file is :gitref:`README.rst`
For more information, see the :gitref:`project README <README.rst>`
```

or link to a variable, function or class in a python file::

```
The method which turns a reference into a line number
is :gitref:`sphinx_python/parse.py::python_to_lineno` -
this will raise a warning if the reference is not found.

Reference class attributes as you would in Python, such
as :gitref:`sphinx_python/git.py::Repo.path`.
```


### Code hash checks

If the file, line number or code reference is not in your code, or if they code's hash
does not match the hash in the database, your docs will fail to build.

You can check your references are up-to-date with::

    sphinx-gitref check

When adding new references, or when referenced code has changed, you can update the hash
database with::

    sphinx-gitref update

See the [documentation](https://sphinx-gitref.readthedocs.io/en/latest/usage.html) for
more detailed usage instructions and options.
