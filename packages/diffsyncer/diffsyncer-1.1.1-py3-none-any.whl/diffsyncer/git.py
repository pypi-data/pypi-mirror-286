import zipfile
import click
import git
import os
import shutil
from diffsyncer import config


def git_clone(repo_url: str) -> bool:
    """
    Clone the git repository
    """
    # extract repo name from git url
    # remove .git from the end
    repo_name = repo_url.split("/")[-1].replace(".git", "")
    repo_dir = os.path.join(config.REPO_DIR, repo_name)
    git.Repo.clone_from(url=repo_url, to_path=repo_dir)
    click.echo(f"Git clone done for {repo_url}")
    return repo_dir


# shell commant: git archive --format=zip $(git diff --diff-filter=d $prev_commit $curr_commit --name-only) >diff.zip
def git_archive(
    repo_dir: str,
    output_file: str = "diff.zip",
    prev_commit_id: str = None,
    current_commit_id: str = None,
) -> bool:
    """
    Archive the git repository
    """
    repo = git.Repo(repo_dir)

    prev_commit_id = prev_commit_id or repo.git.rev_parse("HEAD^")
    current_commit_id = current_commit_id or repo.git.rev_parse("HEAD")

    diff_files = repo.git.diff(
        "--diff-filter=d", prev_commit_id, current_commit_id, "--name-only"
    ).split("\n")

    diff_files = [file for file in diff_files if file]

    if not diff_files:
        click.echo("No file changes")
        return False

    # Create a zip file
    with zipfile.ZipFile(output_file, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file in diff_files:
            if file:  # Ignore empty strings
                file_path = os.path.join(repo_dir, file)
                if os.path.exists(file_path):
                    zipf.write(file_path, file)

    click.echo("Git archive done")
    return output_file


def git_commit(
    repo_dir: str, diff_dir: str, branch: str = "main", auto_push: bool = False
) -> bool:
    """
    Commit changes to the git repository
    """
    repo = git.Repo(repo_dir)

    # checkout to the branch, if not exists, create a new branch
    click.echo(f"Checking out to branch {branch}")
    if branch not in repo.git.branch():
        repo.git.checkout("-b", branch)
    else:
        repo.git.checkout(branch)

    # copy all files and dir in diff_dir to repo_dir
    for item in os.listdir(diff_dir):
        s = os.path.join(diff_dir, item)
        d = os.path.join(repo_dir, item)
        if os.path.isdir(s):
            shutil.copytree(s, d)
        else:
            shutil.copy2(s, d)

    # add all files
    repo.git.add(".")

    # check if there are any changes
    if not repo.is_dirty():
        click.echo("No changes to commit")
        # return False
    else:
        repo.git.commit("-m", "feat: update code by diffsyncer")
        click.echo(f"Git commit done for {repo_dir}")

    if auto_push:
        click.echo("Git pushing changes")
        repo.git.push("origin", branch)

    return True
