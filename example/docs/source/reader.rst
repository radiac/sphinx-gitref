======
Reader
======

This example app has a contrived file reader in the file
:gitref:`example/myproject/reader.py`.

There is a :gitref:`example/myproject/reader.py::Reader` class which has a
:gitref:`example/myproject/reader.py::Reader.path` attribute set by
:gitref:`the constructor <example/myproject/reader.py::Reader.__init__>`, and
it will read the contents of that path when
:gitref:`the constructor <example/myproject/reader.py::Reader.read>` is called.

The helper function :gitref:`example/myproject/reader.py::read` takes
a file path object or path string, instantiates the Reader, and returns the contents.
