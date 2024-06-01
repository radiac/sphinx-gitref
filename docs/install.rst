============
Installation
============

To install sphinx-gitref in your project, run::

    pip install sphinx-gitref


In your Sphinx ``conf.py``, add ``sphinx_gitref`` to the ``extensions`` list::

   extensions = [
       ...
       'sphinx_gitref',
   ]

sphinx-gitref should now work for most projects, but you can customise its defaults with some
configuration options.


Configuration
=============

Define the following variables in Sphinx ``conf.py`` to customise how sphinx-gitref
links to your code.


``gitref_relative_project_root``
--------------------------------

Explicitly specify the relative path to the project root form your docs' source dir.

The project root is the root directory of your git repository.

sphinx-gitref will walk up the directory tree from your documentation source, looking
for the first directory with a ``.git`` dir. It will use this as the project root.

If it mis-detects the path, you can configure it with a relative path. For example, if
your docs are in ``docs/``, you can specify one parent up as::

    gitref_relative_project_root = ".."


``gitref_remote_url``
---------------------

Explicitly specify the remote URL.

sphinx-gitref will try to detect your remote origin URL from the ``.git`` dir in your
project root. If it can't find it, or detects the wrong remote, you can set or override
the remote URL explicitly with::

    gitref_remote_url = "https://github.com/username/repository.git"


``gitref_branch``
-----------------

Explicitly specify the branch to link to.

sphinx-gitref will try to detect your current branch from the ``.git`` dir in your
project root. If it can't find it, or you'd like it to use a different branch, you can
set or override it explicitly with::

    gitref_branch = "master"


``gitref_label_format``
-----------------------

Change the link label format when a coderef is provided without an explicit label, eg
``:gitref:`filename.py::coderef```

sphinx-gitref defaults to using showing the coderef and dropping the filename. This can
be overridden by setting a format string::

    gitref_label_format = "{filename} {coderef}"


``gitref_updating``
-------------------

If ``True`` the hash file will be updated.

It is strongly recommended that you do not set it in your ``conf.py`` - instead you
should set it temporarily, either by using the ``sphinx-gitref`` update command::

    sphinx-gitref update

or pass the setting into Sphinx, eg::

    sphinx-build ... -D gitref_updating=True
