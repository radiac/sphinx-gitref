"""
Check local repo management
"""
import pytest

from sphinx_gitref.git import Repo

from .common import GIT_CONFIG


@pytest.fixture()
def paths(tmp_path):
    class paths:
        root = tmp_path

        # Git
        git = tmp_path / ".git"
        config = tmp_path / ".git" / "config"
        head = tmp_path / ".git" / "HEAD"

    paths.git.mkdir()
    return paths


def test_dir_does_not_exist__fails_silently(paths):
    paths.git.rmdir()
    repo = Repo(paths.git)
    assert repo.path is None
    assert repo.get_remote_url() is None
    assert repo.get_local_branch() is None


def test_config_does_not_exist__fails_silently(paths):
    repo = Repo(paths.git)
    assert repo.path == paths.git
    assert repo.get_remote_url() is None


def test_head_does_not_exist__fails_silently(paths):
    repo = Repo(paths.git)
    assert repo.path == paths.git
    assert repo.get_local_branch() is None


def test_config_exists__origin_found(paths):
    paths.config.write_text(GIT_CONFIG)
    repo = Repo(paths.git)
    assert repo.get_remote_url() == "git@github.com:wildfish/sphinx_gitref.git"


def test_config_valid_but_without_origin__fails_silently(paths):
    paths.config.write_text(GIT_CONFIG.replace("github.com", "example.com"))
    repo = Repo(paths.git)
    assert repo.get_remote_url() == "git@example.com:wildfish/sphinx_gitref.git"


def test_config_valid_but_with_unknown_origin__fails_silently(paths):
    paths.config.write_text(
        u"""[core]
        repositoryformatversion = 0
        filemode = true
        bare = false
        logallrefupdates = true
[branch "master"]
        remote = origin
        merge = refs/heads/master
"""
    )
    repo = Repo(paths.git)
    assert repo.get_remote_url() is None


def test_config_invalid__fails_loudly(paths):
    try:
        from configparser import MissingSectionHeaderError
    except ImportError:
        from ConfigParser import MissingSectionHeaderError

    paths.config.write_text(u"invalid")
    repo = Repo(paths.git)

    with pytest.raises(MissingSectionHeaderError):
        repo.get_remote_url()


def test_head_invalid__fails_silently(paths):
    paths.config.write_text(GIT_CONFIG)
    paths.head.write_text(u"invalid\n")
    repo = Repo(paths.git)
    assert repo.get_local_branch() is None


def test_head_valid__returns_branch_name(paths):
    paths.config.write_text(GIT_CONFIG)
    paths.head.write_text(u"ref: refs/heads/master\n")
    repo = Repo(paths.git)
    assert repo.get_local_branch() == "master"
