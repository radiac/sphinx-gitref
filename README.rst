=============
Sphinx Gitref
=============

.. image:: https://travis-ci.org/wildfish/sphinx-gitref.svg?branch=master
    :target: https://travis-ci.org/wildfish/sphinx-gitref

.. image:: https://codecov.io/gh/wildfish/sphinx-gitref/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/wildfish/sphinx-gitref

Adds a ``:gitref:`..``` role to sphinx to link to your code on GitHub, GitLab or
Bitbucket, and to make sure the references in your docs match the code.

Key features:

* Check code references are up to date
* Link to source code on github
* Incorporate into tests or git hooks

Supports Python 3.6+


Installation
============

Install::

    pip install sphinx-gitref


Modify your Sphinx ``conf.py``:

#. Add ``sphinx_gitref`` to the ``extensions`` list in your Sphinx ``conf.py``::

      extensions = [
          ...
          'sphinx_gitref',
      ]

#. Optional: Explicitly specify the remote URL.

   Gitref will try to detect your remote origin URL from the ``.git`` dir in your docs'
   parent dir. If it can't find it, or detects the wrong remote, you can set or override
   the remote URL explicitly with::

      gitref_remote_url = "https://github.com/username/repository.git"

#. Optional: Explicitly specify the branch to link to.

   Gitref will try to detect your current branch from the ``.git`` dir in your docs'
   parent dir. If it can't find it, or you'd like it to use a different branch, you can
   set or override it explicitly with::

      gitref_branch = "master"


Usage
=====

The ``:gitref:`..``` role supports the following features:

* ``:gitref:`path/to/filename```
* ``:gitref:`path/to/filename.py::coderef```

You can optionally use them with a text label:

* ``:gitref:`text <path/to/filename>```
* ``:gitref:`text <path/to/filename.py::coderef>```

where ``coderef`` is a Python class, function or variable. You can also refer to class
attributes as you would in python, eg ``MyClass.attribute``.

These will be replaced by a link to the code.

If you do not provide a ``coderef``, gitref will just check that the file exists.

Where you provide a ``coderef``, gitref will check that an object with that name exists
in the code, and will add its line number to the link.


Examples
--------

Link to a file on gitref::

    This file is :gitref:`README.rst`
    For more information, see the :gitref:`project README <README.rst>`

Link to a variable, function or class in a python file::

    The method which turns a reference into a line number
    is :gitref:`sphinx_python/parse.py::python_to_lineno` -
    this will raise a warning if the reference is not found.

    Reference class attributes as you would in Python, such
    as :gitref:`sphinx_python/git.py::Repo.path`.


Using in tests
--------------

Because ``sphinx-gitref`` integrates into Sphinx, you can test the references are valid
by performing a test build of your documentation.


Custom remotes
--------------

If your code is stored somewhere other than one of the supported platforms, you can add
a custom remote by subclassing ``sphinx_github.remotes.Remote`` in your Sphinx
``conf.py``; for example::

    from sphinx_github.remotes import Remote
    class Gitea(Remote):
        remote_match = re.compile(r"^git@gitea.example.com:(?P<repo>.+?)\.git$")
        url_pattern = "https://gitea.example.com/{repo}/blob/{branch}/{filename}{line}"
        url_pattern_line = "#L{line}"


Contributing
============

Contributions are welcome by pull request.

They will be merged more quickly if they are provided with unit tests; to run tests
locally with tox::

    pip install tox
    tox
