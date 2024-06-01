Gitref example docs
===================

To see gitref's hashing in action, run::

  sphinx-gitref check

then change the example app's
:gitref:`version <example/myproject/__init__.py::__version__>` and run it again:

  sphinx-gitref check

You'll see an error that the target has changed. Now run::

  sphinx-gitref update
  sphinx-gitref check

and it will pass again.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   reader


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
