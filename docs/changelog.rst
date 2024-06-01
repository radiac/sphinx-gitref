=========
Changelog
=========

Changes for upcoming releases will be listed without a release date - these
are available by installing the development branch from github (see
:doc:`install` for details).

Changelog
=========

0.4.0, TBC
----------

Features:

* Add hash checking
* Add ``sphinx-gitref check`` command to check without building
* Add ``sphinx-gitref update`` to update the hash file


0.3.1, 2024-05-19
-----------------

Changes:

* Set ``parallel_read_safe=True``
* Expand documentation

Thanks to:

* Martijn Pieters (mjpieters) for the ``parallel_read_safe`` change (#11)


0.3.0, 2024-05-19
-----------------

Features:

* Add project root override with ``gitref_relative_project_root``

Changes:

* Better project root detection with override support (fixes #12)
* Support latest Sphinx


0.2.1, 2022-02-19
-----------------

Changes

* Improve repository pattern matching


0.2.0, 2022-02-13
-----------------

Features:

* Add custom label formatting with ``gitref_label_format``

Changes:

* Fix bug when node target has no id
* Improve branch detection to support a recently detached ``HEAD``


0.1.0, 2020-04-18
-----------------

* Initial release
