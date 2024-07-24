import os
import click
from diffsyncer import auth, config, decoder, encoder, git, server


def init_key(keyfile: str):
    aes_key = os.urandom(32)
    with open(keyfile, "wb") as file:
        file.write(aes_key)


@click.group()
def cli():
    pass


@click.command(name="aeskey", help="Generate AES key")
@click.option(
    "--keyfile",
    help="Output file to save the AES key",
    default="aes_key.bin",
)
def aeskey(keyfile: str):
    if not os.path.exists(keyfile):
        init_key(keyfile)


@click.command(name="serve", help="Run the DiffSyncer server")
@click.option(
    "--host",
    help="Host to run the server on",
    default="0.0.0.0",
)
@click.option(
    "--port",
    help="Port to run the server on",
    default=3000,
)
@click.option(
    "--log-level",
    help="Log level",
    default="info",
)
def serve(
    host: str,
    port: int,
    log_level: str,
):
    import uvicorn

    uvicorn.run(
        server.app,
        host=host,
        port=port,
        log_level=log_level,
    )


@click.command(name="encode", help="Generate QR codes for git diff patch data")
@click.option("--input", help="Input file to encode", required=False, default=None)
@click.option(
    "--output",
    help="Output directory to save QR codes",
    default="output",
)
@click.option(
    "--repo-dir",
    help="Path to the git repository",
    default=os.getcwd(),
)
@click.option(
    "--prev-commit-id",
    help="Previous commit id",
    default=None,
)
@click.option(
    "--current-commit-id",
    help="Current commit id",
    default=None,
)
def encode(
    input: str, output: str, repo_dir: str, prev_commit_id: str, current_commit_id: str
):
    # if aes key file does not exist, generate a new one
    if not os.path.exists(config.ASE_KEY_FILE):
        click.echo("AES key file does not exist, generating a new one", color="yellow")
        init_key(config.ASE_KEY_FILE)

    click.echo(f"Generating QR codes for: {input}")
    if not input:
        # execute git_archive to get diff file
        diff_file = os.path.join(os.getcwd(), "diff.zip")
        git.git_archive(
            repo_dir=repo_dir,
            output_file=diff_file,
            prev_commit_id=prev_commit_id,
            current_commit_id=current_commit_id,
        )
    else:
        diff_file = os.path.join(os.getcwd(), input)

    output_dir = os.path.join(os.getcwd(), output)
    encoder.execute(diff_file, output_dir)
    click.echo(f"Generated QR codes to: {output_dir}")


@click.command(name="decode", help="Decode QR codes to get git diff patch data")
@click.option(
    "--qrdir",
    help="Directory containing QR codes to decode",
    default="output",
)
def decode(qrdir: str):
    qrcode_dir = os.path.join(os.getcwd(), qrdir)
    unzip_dir = decoder.execute(qrcode_dir)
    click.echo(f"Decoded QR codes to: {unzip_dir}")


def gitsync(
    repo_dir: str = config.REPO_DIR,
    diff_dir: str = config.DIFF_DIR,
    auto_push: bool = False,
):
    git.git_commit(repo_dir=repo_dir, diff_dir=diff_dir, auto_push=auto_push)


@click.command(name="sync", help="Sync git repository with the decode diff patch data")
@click.option(
    "--repo-dir",
    help="Path to the git repository",
    default=config.REPO_DIR,
)
@click.option(
    "--diff-dir",
    help="Path to the diff directory",
    default=config.DIFF_DIR,
)
@click.option(
    "--auto-push",
    help="Automatically push changes to the remote repository",
    is_flag=True,
)
def sync(repo_dir: str, diff_dir: str, auto_push: bool):
    # if diff dir does not exist, decode the diff zip file first
    if not os.path.exists(diff_dir):
        click.echo("Decoding QR codes", color="yellow")
        decode.callback(qrdir="output")

    gitsync(repo_dir, diff_dir, auto_push)


@click.command(name="pass")
@click.argument("password")
def pwd(password: str):
    """Generate password hash

    PASSWORD is the password to hash.
    """
    pwd_hash = auth.get_password_hash(password)
    click.echo(f"Password hash generated: {pwd_hash}", color="green")


cli.add_command(aeskey)
cli.add_command(serve)
cli.add_command(encode)
cli.add_command(decode)
cli.add_command(sync)
cli.add_command(pwd)

if __name__ == "__main__":
    cli()
