import os
from pathlib import Path

import pytest
from click.testing import CliRunner
from sphinx.application import Sphinx
from sphinx.errors import SphinxError

import sphinx_gitref
from sphinx_gitref.commands import cli

from .test_role import paths  # noqa


@pytest.fixture
def with_pythonpath():
    gitref_path = Path(sphinx_gitref.__file__).parent.parent.absolute()
    orig = os.environ.get("PYTHONPATH", "")
    os.environ["PYTHONPATH"] = f"{orig}:{gitref_path}" if orig else str(gitref_path)
    yield
    os.environ["PYTHONPATH"] = orig


@pytest.fixture
def extra_paths(with_pythonpath, paths):
    paths.conf.write_text(
        """
master_doc = 'index'
extensions = ["sphinx_gitref"]
gitref_hashing = True
"""
    )

    paths.makefile = paths.docs / "Makefile"
    paths.makefile.write_text(
        """SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build
.PHONY: help Makefile
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
"""
    )

    paths.index = paths.docs / "index.rst"
    paths.index.write_text("foo :gitref:`Example <example.py>`")
    return paths


def test_check__no_hashfile__exception(extra_paths):
    runner = CliRunner()
    result = runner.invoke(cli, ["check", str(extra_paths.docs)])
    assert "Could not load gitref hash" in result.output
    assert result.exit_code == 1


def test_update_runs(extra_paths):
    runner = CliRunner()
    result = runner.invoke(cli, ["update", str(extra_paths.docs)])

    hashfile = extra_paths.docs / "gitref.json"
    assert hashfile.exists()
    assert '"example.py"' in hashfile.read_text()
    assert result.exit_code == 0


def test_update_check__runs(extra_paths):
    runner = CliRunner()
    runner.invoke(cli, ["update", str(extra_paths.docs)])
    result = runner.invoke(cli, ["check", str(extra_paths.docs)])
    assert "1 gitref reference found" in result.output
    assert "build succeeded" in result.output
    assert result.exit_code == 0


def test_update_change_check__hash_changed__exception(extra_paths):
    runner = CliRunner()
    runner.invoke(cli, ["update", str(extra_paths.docs)])

    extra_paths.example.write_text("value = 2")

    result = runner.invoke(cli, ["check", str(extra_paths.docs)])
    assert '[gitref] Error resolving "example.py": Target changed' in result.output
    assert "[gitref] References failed. Build failed." in result.output
    assert result.exit_code == 1
