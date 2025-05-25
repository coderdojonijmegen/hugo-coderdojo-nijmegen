import logging
from os import chdir, getcwd

from publisher.executor import execute, execute_args

logger = logging.getLogger(__file__)


def git_configure(actor: str) -> None:
    logger.info("configure git repo")
    git(f"config --global user.name {actor}")
    git(f"config --global user.email {actor}@users.noreply.github.com")
    git("config --global --add safe.directory /")


def git(cmd, message=None, working_dir=None, accept_non_zero_return=False) -> tuple[int, str, str]:
    cwd = getcwd()
    if working_dir is not None:
        chdir(working_dir)
    try:
        args = f"/usr/bin/git {cmd}".split(" ")
        if message is not None:
            args.append(message)
        return_code, stdout, stderr = execute_args(args)
        if return_code != 0:
            if accept_non_zero_return:
                if "fatal" in stderr:
                    raise IOError(stderr)
            else:
                raise IOError(stderr)
        return return_code, stdout, stderr
    finally:
        chdir(cwd)
