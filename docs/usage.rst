=====
Usage
=====

reStructuredText
================

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

Link to a file using gitref::

  This file is :gitref:`README.rst`
  For more information, see the :gitref:`project README <README.rst>`


Link to a variable, function or class in a python file::

    The method which turns a reference into a line number
    is :gitref:`sphinx_python/parse.py::python_to_lineno` -
    this will raise a warning if the reference is not found.

    Reference class attributes as you would in Python, such
    as :gitref:`sphinx_python/git.py::Repo.path`.


Commands
========

``sphinx-gitref check``
-----------------------

Perform a check of the references.

Because ``sphinx-gitref`` is based around the ``:gitref:`` Sphinx role, the best way to
test the references is to build the documentation itself.

This command will perform a full build of the documentation, without writing to disk.

Equivalent to ``sphinx-build -M null ... -E -a``


``sphinx-gitref update``
------------------------

This will update the gitref hash file.

Make sure to commit ``gitref.json`` to your git repository.

Equivalent to ``sphinx-build -M null ... -D gitref_updating=True``


Using in tests
==============

Either run a check::

  sphinx-gitref check

or build the documentation directly.


Custom remotes
==============

sphinx-gitref comes with support for GitHub, GitLab and Bitbucket.

If your code is stored somewhere else, you can add a custom remote by subclassing
``sphinx_github.remotes.Remote`` in your Sphinx ``conf.py``; for example::

    from sphinx_github.remotes import Remote
    class Gitea(Remote):
        remote_match = re.compile(r"^git@gitea.example.com:(?P<repo>.+?)\.git$")
        url_pattern = "https://gitea.example.com/{repo}/blob/{branch}/{filename}{line}"
        url_pattern_line = "#L{line}"
