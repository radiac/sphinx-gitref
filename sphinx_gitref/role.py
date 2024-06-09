"""
Sphinx role
"""
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from docutils import nodes, utils
from sphinx.util.nodes import split_explicit_title

from .exceptions import ParseError
from .parser import python_to_node

if TYPE_CHECKING:
    from docutils.parsers.rst.states import Inliner


def gitref(
    name: str,
    rawtext: str,
    text: str,
    lineno: int,
    inliner: Inliner,
    options: dict | None = None,
    content=[],
):
    """
    Reference a file in git

    Uses the ``gitref_repo`` config value

    Usage:
        :gitref:`target`
        :gitref:`label <target>`

    where ``target`` is a filename with an optional reference to a definition in the
    code:

    * ``path/to/filename.py``
    * ``path/to/filename.py#L6``
    * ``path/to/filename.py::coderef``
    * ``path/to/filename.py::code.ref``

    Renders HTML:
        <a href="url">label</a>
    """
    # Collect config vars
    app = inliner.document.settings.env.app
    try:
        remote = app.config.gitref_remote
        if not remote:
            raise AttributeError
    except AttributeError:
        raise ValueError("Config does not specify gitref_remote")

    hasher = app.hasher

    # Process text value
    has_t, title, target = split_explicit_title(text)
    title = utils.unescape(title)
    target = utils.unescape(target)

    # Find the target
    found = hasher.find_target(target)
    filename, coderef = hasher.name_ref[target]

    # Set title if not set
    if title == target:
        if coderef is not None:
            title = app.config.gitref_label_format.format(
                filename=filename,
                coderef=coderef,
            )

    if target in hasher.errors:
        error = hasher.errors[target]
        inliner.reporter.error(f'[gitref] Error resolving "{target}": {error}')
        return [nodes.Text(title)], []

    ref = remote.get_url(filename=filename, line=hasher.lines.get(target))

    node = nodes.reference(rawtext, title, refuri=ref, **(options or {}))
    return [node], []
