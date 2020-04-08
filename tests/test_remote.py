"""
Test the remote definitions
"""

import re

import pytest

from sphinx_gitref.remote import Bitbucket, GitHub, GitLab, Remote, registry


def test_registry_get_by_url__github_ssh__detected():
    url = "git@github.com:user/repo.git"
    remote = registry.get_by_url(url, "branch")
    assert isinstance(remote, GitHub)
    assert remote.repo == "user/repo"
    assert remote.branch == "branch"


def test_registry_get_by_url__github_https__detected():
    url = "https://github.com/user/repo.git"
    remote = registry.get_by_url(url, "branch")
    assert isinstance(remote, GitHub)
    assert remote.repo == "user/repo"
    assert remote.branch == "branch"


def test_github_url__url_without_line__correct_url():
    remote = GitHub("user/repo", "branch")
    assert (
        remote.get_url("filename.py")
        == "https://github.com/user/repo/blob/branch/filename.py"
    )


def test_github_url__url_with_line__correct_url():
    remote = GitHub("user/repo", "branch")
    assert (
        remote.get_url("filename.py", 20)
        == "https://github.com/user/repo/blob/branch/filename.py#L20"
    )


def test_registry_get_by_url__bitbucket_ssh__detected():
    url = "git@bitbucket.org:user/repo.git"
    remote = registry.get_by_url(url, "branch")
    assert isinstance(remote, Bitbucket)
    assert remote.repo == "user/repo"
    assert remote.branch == "branch"


def test_registry_get_by_url__bitbucket_https__detected():
    url = "https://bitbucket.org/user/repo.git"
    remote = registry.get_by_url(url, "branch")
    assert isinstance(remote, Bitbucket)
    assert remote.repo == "user/repo"
    assert remote.branch == "branch"


def test_bitbucket_url__url_without_line__correct_url():
    remote = Bitbucket("user/repo", "branch")
    assert (
        remote.get_url("filename.py")
        == "https://bitbucket.org/user/repo/src/branch/filename.py"
    )


def test_bitbucket_url__url_with_line__correct_url():
    remote = Bitbucket("user/repo", "branch")
    assert (
        remote.get_url("filename.py", 20)
        == "https://bitbucket.org/user/repo/src/branch/filename.py#lines-20"
    )


def test_registry_get_by_url__gitlab_ssh__detected():
    url = "git@gitlab.com:user/repo.git"
    remote = registry.get_by_url(url, "branch")
    assert isinstance(remote, GitLab)
    assert remote.repo == "user/repo"
    assert remote.branch == "branch"


def test_registry_get_by_url__gitlab_https__detected():
    url = "https://gitlab.com/user/repo.git"
    remote = registry.get_by_url(url, "branch")
    assert isinstance(remote, GitLab)
    assert remote.repo == "user/repo"
    assert remote.branch == "branch"


def test_gitlab_url__url_without_line__correct_url():
    remote = GitLab("user/repo", "branch")
    assert (
        remote.get_url("filename.py")
        == "https://gitlab.com/user/repo/blob/branch/filename.py"
    )


def test_gitlab_url__url_with_line__correct_url():
    remote = GitLab("user/repo", "branch")
    assert (
        remote.get_url("filename.py", 20)
        == "https://gitlab.com/user/repo/blob/branch/filename.py#L20"
    )


def test_registry_get_by_url__unknown__raises_error():
    invalid = "https://invalid.example.com/user/repo.git"
    with pytest.raises(ValueError) as e:
        registry.get_by_url(invalid, "branch")
    assert str(e.value) == f"Unable to find a match for {invalid}"


def test_custom_remote__get_by_url__finds():
    class TestRemote(Remote):
        remote_match = re.compile(r"^https://test.example.com/(?P<repo>.+?).git$")

    url = "https://test.example.com/user/repo.git"
    remote = registry.get_by_url(url, "branch")
    assert isinstance(remote, TestRemote)
    assert remote.repo == "user/repo"
    assert remote.branch == "branch"
