import os
import subprocess

from utils import slack


def h_message(message):
    print(f"\n\n\033[1;37m{message}\033[0m\n")


def _sub(args):
    print(args)
    with subprocess.Popen(args) as proc:
        stdout, stderr = proc.communicate()
        return proc.returncode, stdout, stderr


def git(args, message=None, working_dir=None, accept_git_non_zero_return=False):
    cwd = os.getcwd()
    if working_dir is not None:
        os.chdir(working_dir)
    try:
        cmd = f"/usr/bin/git {args}".split(" ")
        if message is not None:
            cmd.append(f"{message}")
        return_code, stdout, stderr = _sub(cmd)
        if not accept_git_non_zero_return and return_code != 0:
            raise IOError(stderr)
        return return_code, stdout, stderr
    finally:
        os.chdir(cwd)


def hugo(args):
    return _sub(f"./hugo {args}".split(" "))


def rm_rf(dir_path):
    _sub(f"rm -rf {dir_path}".split(" "))
