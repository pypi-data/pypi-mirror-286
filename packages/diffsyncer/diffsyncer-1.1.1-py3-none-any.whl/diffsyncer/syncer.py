import os
import shutil

import click

from diffsyncer import config
from diffsyncer import git


def sync(repo_url: str, diff_dir: str, branch: str = "main"):
    # 1. check if repo clone exists
    repo_name = repo_url.split("/")[-1].replace(".git", "")
    repo_dir = os.path.join(config.REPO_DIR, repo_name)
    click.echo(f"Syncing {diff_dir} to {repo_dir}")

    if not os.path.exists(repo_dir):
        # 2. clone repo
        git.git_clone(repo_url)

    # 3. copy files from diff_dir to repo_dir
    # copy all files and dir in diff_dir to repo_dir
    for item in os.listdir(diff_dir):
        s = os.path.join(diff_dir, item)
        d = os.path.join(repo_dir, item)
        if os.path.isdir(s):
            shutil.copytree(s, d)
        else:
            shutil.copy2(s, d)

    # 4. commit changes
    git.git_commit(repo_dir, diff_dir, branch=branch, auto_push=True)
