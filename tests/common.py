GIT_CONFIG = """[core]
        repositoryformatversion = 0
        filemode = true
        bare = false
        logallrefupdates = true
[remote "origin"]
        fetch = +refs/heads/*:refs/remotes/origin/*
        url = git@github.com:wildfish/sphinx_gitref.git
[branch "master"]
        remote = origin
        merge = refs/heads/master
"""
