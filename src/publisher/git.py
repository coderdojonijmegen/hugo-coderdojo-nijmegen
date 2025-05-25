import logging
from os import chdir, getcwd
from typing import Any, Literal

from publisher.executor import execute

logger = logging.getLogger(__file__)


def git_configure(actor: str) -> None:
    logger.info("configure git repo")
    git(f"config --global user.name {actor}")
    git(f"config --global user.email {actor}@users.noreply.github.com")
    git("config --global --add safe.directory /")


def git(args, message=None, working_dir=None, accept_non_zero_return=False) -> tuple[Literal[0] | int | Any, bytes, bytes]:
    cwd = getcwd()
    if working_dir is not None:
        chdir(working_dir)
    try:
        cmd = f"/usr/bin/git {args}"
        if message is not None:
            cmd += f" {message}"
        return_code, stdout, stderr = execute(cmd)
        if not accept_non_zero_return and return_code != 0:
            raise IOError(stderr)
        return return_code, stdout, stderr
    finally:
        chdir(cwd)
