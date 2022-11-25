from git import Repo
import os
import sys
from pathlib import Path


git_url = "https://github.com/terryfera/routing-lab.git"
labs_parent_dir = "/opt/clab/"
repo_dir = "arista-bgp-evpn"

repo_path = Path(labs_parent_dir + repo_dir)
repo_git = Path(labs_parent_dir + repo_dir + ".git")

if repo_path.is_dir():
    print("Warning Path already exists, checking for existing git repo")
    if repo_git.is_file():
        print("Git repo already in this directory, delete it before trying again")
    else:
        print(f"Cloning repo from {git_url}")
        Repo.clone_from(git_url, labs_parent_dir + repo_dir)
else:
    print(f"Making directory {repo_path}")
    os.mkdir(labs_parent_dir + repo_dir)
    print(f"Cloning repo from {git_url}")
    Repo.clone_from(git_url, labs_parent_dir + repo_dir)
