"""
Set up the extension in sphinx

The ``setup()`` function will be called automatically by Sphinx
"""
from pathlib import Path

from .builders import NullBuilder
from .constants import DEFAULT_LABEL_FORMAT, HASH_FILENAME
from .git import Repo
from .hasher import Hasher
from .remote import registry
from .role import gitref


def get_project_root(doc_root: Path, option: str | None):
    # See if gitref_relative_project_root has told us where to look
    if option is not None:
        project_root = (doc_root / option).absolute()
        if not project_root.is_dir():
            raise ValueError(
                f"Project root {project_root} does not exist"
                " - check your gitref_relative_project_root"
            )
        return project_root

    # Try to detect it
    project_root = doc_root
    while project_root != project_root.parent:
        if (project_root / ".git").is_dir():
            return project_root
        project_root = project_root.parent

    # Couldn't find it
    raise ValueError(
        "Could not find ancestor path containing a .git dir"
        " - configure with gitref_relative_project_root"
    )


def complete_config(app):
    conf_dir = Path(app.confdir)
    # Find path for hash file
    app.env.hash_path = conf_dir / HASH_FILENAME

    # Find path for project root - where we'll find .git
    app.env.project_root = get_project_root(
        conf_dir, app.config.gitref_relative_project_root
    )
    repo = Repo(app.env.project_root / ".git")

    # Update config with defaults from the repo
    if app.config.gitref_remote_url is None:
        app.config.gitref_remote_url = repo.get_remote_url()
    if app.config.gitref_branch is None:
        app.config.gitref_branch = repo.get_local_branch()


def lookup_remote(app):
    """
    Once configuration is complete, build the Remote
    """
    config = app.config
    try:
        remote_url = config.gitref_remote_url
        if not remote_url:
            raise AttributeError
    except AttributeError:
        raise ValueError("Could not determine gitref_remote_url, must set explicitly")

    try:
        branch = config.gitref_branch
        if not branch:
            raise AttributeError
    except AttributeError:
        raise ValueError("Could not determine gitref_branch, must set explicitly")

    config.gitref_remote = registry.get_by_url(remote_url, branch)


def prepare_hasher(app):
    hashing = app.config.gitref_hashing
    updating = app.config.gitref_updating
    if hashing and not updating and not app.env.hash_path.exists():
        raise ValueError("Could not load gitref hash - run with --gitref-update?")

    app.hasher = Hasher(
        file=app.env.hash_path,
        project_root=app.env.project_root,
        hashing=hashing,
        updating=updating,
    )

    if not updating:
        app.hasher.check()


def handle_builder_inited(app):
    complete_config(app)
    lookup_remote(app)
    prepare_hasher(app)


def handle_get_outdated(app, env, added, changed, removed):
    if app.config.gitref_updating:
        # If updating, mark all documents as outdated
        return env.found_docs
    return added | changed | removed


def handle_build_finished(app, exception):
    app.hasher.finish()


def setup(app):
    """
    Prepare config values and register role
    """
    from . import __version__

    # Add config variables, defaults come later
    app.add_config_value("gitref_relative_project_root", default=None, rebuild="html")
    app.add_config_value("gitref_remote_url", None, "html")
    app.add_config_value("gitref_branch", None, "html")
    app.add_config_value("gitref_label_format", DEFAULT_LABEL_FORMAT, "html")
    app.add_config_value("gitref_hashing", default=True, rebuild="env")
    app.add_config_value("gitref_updating", default=False, rebuild="env")

    # Listen for hooks
    app.connect("builder-inited", handle_builder_inited)
    app.connect("env-get-outdated", handle_get_outdated)
    app.connect("build-finished", handle_build_finished)

    # Add builder
    app.add_builder(NullBuilder)

    # Register role
    app.add_role("gitref", gitref)

    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
