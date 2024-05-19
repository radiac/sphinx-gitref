# Sphinx Gitref


[![PyPI](https://img.shields.io/pypi/v/sphinx-gitref.svg)](https://pypi.org/project/sphinx-gitref/)
[![Tests](https://github.com/radiac/sphinx-gitref/actions/workflows/ci.yml/badge.svg)](https://github.com/radiac/sphinx-gitref/actions/workflows/ci.yml)
[![Coverage](https://codecov.io/gh/radiac/sphinx-gitref/branch/main/graph/badge.svg?token=Q9AKPHRJF5)](https://codecov.io/gh/radiac/sphinx-gitref)

Adds a `` :gitref:`..` `` role to sphinx to link to your code on GitHub, GitLab or
Bitbucket, and to make sure the references in your docs match the code.

Key features:

* Check code references are up to date
* Link to source code on github
* Incorporate into tests or git hooks

Supports Python 3.7+


## Installation

Install::

    pip install sphinx-gitref


In your Sphinx ``conf.py``, add ``sphinx_gitref`` to the ``extensions`` list:

   ```python
   extensions = [
       ...
       'sphinx_gitref',
   ]
   ```

Gitref should now work for most projects, but see "Configuration" below to customise its
defaults.


## Usage

The `` :gitref:`..` `` role supports the following features:

* `` :gitref:`path/to/filename` ``
* `` :gitref:`path/to/filename.py::coderef` ``

You can optionally use them with a text label:

* `` :gitref:`text <path/to/filename>` ``
* `` :gitref:`text <path/to/filename.py::coderef>` ``

where ``coderef`` is a Python class, function or variable. You can also refer to class
attributes as you would in python, eg ``MyClass.attribute``.

These will be replaced by a link to the code.

If you do not provide a ``coderef``, gitref will just check that the file exists.

Where you provide a ``coderef``, gitref will check that an object with that name exists
in the code, and will add its line number to the link.


### Examples

Link to a file on gitref::

```
This file is :gitref:`README.rst`
For more information, see the :gitref:`project README <README.rst>`
```

Link to a variable, function or class in a python file::

```
The method which turns a reference into a line number
is :gitref:`sphinx_python/parse.py::python_to_lineno` -
this will raise a warning if the reference is not found.

Reference class attributes as you would in Python, such
as :gitref:`sphinx_python/git.py::Repo.path`.
```

### Using in tests

Because ``sphinx-gitref`` integrates into Sphinx, you can test the references are valid
by performing a test build of your documentation.


### Custom remotes

If your code is stored somewhere other than one of the supported platforms, you can add
a custom remote by subclassing ``sphinx_github.remotes.Remote`` in your Sphinx
``conf.py``; for example::

```python
from sphinx_github.remotes import Remote
class Gitea(Remote):
    remote_match = re.compile(r"^git@gitea.example.com:(?P<repo>.+?)\.git$")
    url_pattern = "https://gitea.example.com/{repo}/blob/{branch}/{filename}{line}"
    url_pattern_line = "#L{line}"
```


## Configuration

Define the following variables in Sphinx ``conf.py``.


### ``gitref_relative_project_root``

Explicitly specify the relative path to the project root form your docs' source dir.

The project root is the root directory of your git repository.

Gitref will walk up the directory tree from your documentation source, looking for the
first directory with a ``.git`` dir. It will use this as the project root.

If it mis-detects the path, you can configure it with a relative path. For example, if
your docs are in ``docs/``, you can specify one parent up as:

```python
gitref_relative_project_root = ".."
```


### ``gitref_remote_url``

Explicitly specify the remote URL.

Gitref will try to detect your remote origin URL from the ``.git`` dir in your project
root. If it can't find it, or detects the wrong remote, you can set or override the
remote URL explicitly with:

```python
gitref_remote_url = "https://github.com/username/repository.git"
```


### ``gitref_branch``

Explicitly specify the branch to link to.

Gitref will try to detect your current branch from the ``.git`` dir in your project
root. If it can't find it, or you'd like it to use a different branch, you can set or
override it explicitly with::

```python
gitref_branch = "master"
```

### ``gitref_label_format``

Change the link label format when a coderef is provided without an explicit label, eg
`` :gitref:`filename.py::coderef` ``

Gitref defaults to using showing the coderef and dropping the filename. This can be
overridden by setting a format string::

```python
gitref_label_format = "{filename} {coderef}"
```



## Changelog

0.3.0 - 2024-05-19
* Better project root detection with override support (fixes #12)
* Support latest Sphinx

0.2.1 - 2022-02-19
* Improve repository pattern matching

0.2.0 - 2022-02-13
* Add custom label formatting with ``gitref_label_format``
* Fix bug when node target has no id
* Improve branch detection to support a recently detached ``HEAD``

0.1.0 - 2020-04-18
* Initial release
