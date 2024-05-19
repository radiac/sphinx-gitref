============
Contributing
============

Contributions are welcome, preferably via pull request. Check the github issues and to
see what needs work.

If you have an idea for a new feature, it's worth opening a new ticket to discuss
whether it's suitable for the project, or would be better as a separate package.


Installing
==========

The easiest way to work on sphinx-gitref is to fork the project on GitHub, then::

    git checkout git@github.com:USERNAME/sphinx-gitref.git
    cd sphinx-gitref
    python -m venv .venv
    source .venv/bin/activate
    pip install -r sphinx-gitref/requirements-dev.txt

(replacing ``USERNAME`` with your username).


Testing
=======

It is greatly appreciated when contributions come with tests, and they will lead to a
faster merge and release of your work.

Use ``pytest`` to run the tests::

  cd sphinx-gitref
  pytest

These will also generate a ``coverage`` HTML report.
