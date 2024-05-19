"""
Test the :gitref: role
"""
import pytest
from sphinx.application import Sphinx

from .common import GIT_CONFIG

try:
    # Python 2.7
    from StringIO import StringIO
except ImportError:
    from io import StringIO


@pytest.fixture
def paths(tmp_path):
    class paths:
        root = tmp_path

        # Docs
        docs = tmp_path / "docs"
        build = tmp_path / "docs" / "_build"
        html = tmp_path / "docs" / "_build" / "html"
        doctrees = tmp_path / "docs" / "_build" / "doctrees"
        conf = tmp_path / "docs" / "conf.py"

        # Git
        git = tmp_path / ".git"
        git_config = tmp_path / ".git" / "config"
        git_head = tmp_path / ".git" / "HEAD"

        # Code
        example = tmp_path / "example.py"

    paths.docs.mkdir()
    paths.build.mkdir()
    paths.html.mkdir()
    paths.doctrees.mkdir()
    paths.conf.write_text(
        """
master_doc = 'index'
extensions = ["sphinx_gitref"]
"""
    )

    paths.git.mkdir()
    paths.git_config.write_text(GIT_CONFIG)
    paths.git_head.write_text("ref: refs/heads/master\n")

    # Give a sensible default for most tests
    paths.example.write_text("value = 1")

    return paths


EXAMPLE_FUNCTION = """value = 1

def function():
    pass
"""

EXAMPLE_CLASS = """value = 1

class Cls():
    value = 1

    def function():
        pass
"""


@pytest.fixture
def app(paths):
    """
    Create a Sphinx app ready to call app.build

    Output will be available on app._status.getvalue()

    Warnings are app._warnings.getvalue()
    """
    with paths.docs.cwd():
        app = Sphinx(
            srcdir=str(paths.docs),
            confdir=str(paths.docs),
            outdir=str(paths.html),
            doctreedir=str(paths.doctrees),
            status=StringIO(),
            warning=StringIO(),
            buildername="html",
        )
        return app


def test_path__path_renders_as_link(app, paths):
    index = paths.docs / "index.rst"
    index.write_text("foo :gitref:`example.py`")
    app.build()

    html = (paths.html / "index.html").read_text()
    assert (
        '<p>foo <a class="reference external" '
        'href="https://github.com/radiac/sphinx_gitref/blob/master/example.py">'
        "example.py</a></p>"
    ) in html


def test_path__path_renders_as_link_with_label(app, paths):
    index = paths.docs / "index.rst"
    index.write_text("foo :gitref:`Example <example.py>`")
    app.build()

    html = (paths.html / "index.html").read_text()
    assert (
        '<p>foo <a class="reference external" '
        'href="https://github.com/radiac/sphinx_gitref/blob/master/example.py">'
        "Example</a></p>"
    ) in html


def test_path__path_does_not_exist__renders_but_raises_warning(app, paths, capsys):
    paths.example.unlink()
    index = paths.docs / "index.rst"
    index.write_text("foo :gitref:`Example <example.py>`")

    start_warnings = app._warncount
    app.build()

    # Check it renders as before...
    html = (paths.html / "index.html").read_text()
    assert (
        '<p>foo <a class="reference external" '
        'href="https://github.com/radiac/sphinx_gitref/blob/master/example.py">'
        "Example</a></p>"
    ) in html

    # ... but still raises a warning
    assert app._warncount - start_warnings == 1
    assert (
        "Referenced file does not exist: example.py"
        in app._warning.getvalue().splitlines()[-1]
    )


def test_coderef_var__path_renders_as_link(app, paths):
    index = paths.docs / "index.rst"
    index.write_text("foo :gitref:`example.py::value`")
    app.build()

    html = (paths.html / "index.html").read_text()
    assert (
        '<p>foo <a class="reference external" '
        'href="https://github.com/radiac/sphinx_gitref/blob/master/example.py#L1">'
        "value</a></p>"
    ) in html


def test_coderef_var__path_renders_as_link_with_label(app, paths):
    index = paths.docs / "index.rst"
    index.write_text("foo :gitref:`Example <example.py::value>`")
    app.build()

    html = (paths.html / "index.html").read_text()
    assert (
        '<p>foo <a class="reference external" '
        'href="https://github.com/radiac/sphinx_gitref/blob/master/example.py#L1">'
        "Example</a></p>"
    ) in html


def test_coderef_var__does_not_exist__renders_as_link_but_raises_error(app, paths):
    index = paths.docs / "index.rst"
    index.write_text("foo :gitref:`Example <example.py::missing>`")

    start_warnings = app._warncount
    app.build()

    # Check it renders without line numbers
    html = (paths.html / "index.html").read_text()
    assert (
        '<p>foo <a class="reference external" '
        'href="https://github.com/radiac/sphinx_gitref/blob/master/example.py">'
        "Example</a></p>"
    ) in html

    # Check it still raises a warning
    assert app._warncount - start_warnings == 1
    assert (
        'Error resolving code reference "example.py::missing": '
        'Couldn\'t find "missing"'
    ) in app._warning.getvalue().splitlines()[-1]
