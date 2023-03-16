import subprocess
import os

from utils import slack


def h_message(message):
    print(f"\n\n\033[1;37m{message}\033[0m\n")


def _sub(args):
    print(args)
    with subprocess.Popen(args) as proc:
        stdout, stderr = proc.communicate()
        return proc.returncode, stdout, stderr


def git(args, message=None, working_dir=None):
    cwd = os.getcwd()
    if working_dir is not None:
        os.chdir(working_dir)
    try:
        cmd = f"/usr/bin/git {args}".split(" ")
        if message is not None:
            cmd.append(f"{message}")
        return_code, stdout, stderr = _sub(cmd)
        if return_code != 0:
            raise IOError(stderr)
        return return_code, stdout, stderr
    finally:
        os.chdir(cwd)


def hugo(args):
    ret_code, stdout, stderr = _sub(f"./hugo {args}".split(" "))
    if ret_code != 0:
        slack.notify("Hugo error", f"{stdout}: {stderr}")
        exit(-1)


def rm_rf(dir_path):
    _sub(f"rm -rf {dir_path}".split(" "))
