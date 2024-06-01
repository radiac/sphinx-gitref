import os
import sys
from pathlib import Path
from subprocess import run

import click


def get_sphinx_dir(ctx, param, dir: str) -> Path:
    """Ensure sure target dir has a conf.py and Makefile"""
    path = Path(dir).absolute()
    if not path.exists():
        raise click.UsageError(f"No dir found at {path}")
    if not (path / "Makefile").exists():
        raise click.UsageError(f"No Makefile found at {path}")
    return path


def make(dir: Path, opts: str):
    env = os.environ.copy()
    env["SPHINXOPTS"] = opts
    run(
        ["make", "null"],
        cwd=dir,
        stdout=sys.stdout,
        stderr=sys.stderr,
        env=env,
    )


@click.group()
def cli():
    """sphinx-gitref"""
    pass


@cli.command()
@click.argument("dir", default=".", required=False, callback=get_sphinx_dir)
def check(dir: Path):
    """Check referenced code hasn't been modified"""
    make(dir, "-E -a")


@cli.command()
@click.argument("dir", default=".", required=False, callback=get_sphinx_dir)
def update(dir: Path):
    """Update hashes for referenced code"""
    make(dir, "-D gitref_updating=True")


def invoke():
    cli()
