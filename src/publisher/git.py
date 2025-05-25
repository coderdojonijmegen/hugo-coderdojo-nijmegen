import logging
from os import chdir, getcwd
from subprocess import Popen
from typing import Any, Literal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__file__)


def git_configure(actor: str) -> None:
    logger.info("configure git repo")
    git(f"config --global user.name {actor}")
    git(f"config --global user.email {actor}@users.noreply.github.com")
    git(f"config --global --add safe.directory /")


def git(args, message=None, working_dir=None, accept_git_non_zero_return=False) -> tuple[
    Literal[0] | int | Any, bytes, bytes]:
    cwd = getcwd()
    if working_dir is not None:
        chdir(working_dir)
    try:
        cmd = f"/usr/bin/git {args}".split(" ")
        if message is not None:
            cmd.append(f"{message}")
        return_code, stdout, stderr = _exec(cmd)
        if not accept_git_non_zero_return and return_code != 0:
            raise IOError(stderr)
        return return_code, stdout, stderr
    finally:
        chdir(cwd)


def _exec(args, env=None) -> tuple[int | Any, bytes, bytes]:
    logger.info(f"Executing: {args}")
    with Popen(args, env=env) as proc:
        stdout, stderr = proc.communicate()
        return proc.returncode, stdout, stderr
