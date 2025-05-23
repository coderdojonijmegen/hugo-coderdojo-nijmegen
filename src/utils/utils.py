import os
import subprocess


def h_message(message):
    print(f"\n\n\033[1;37m{message}\033[0m\n")


def _sub(args, env=None):
    print(args)
    with subprocess.Popen(args, env=env) as proc:
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


def hugo(args, opengraph_io_api_key):
    return _sub(f"./hugo {args}".split(" "), env=os.environ | {"HUGO_PARAMS_opengraphioapikey": opengraph_io_api_key})


def rm_rf(dir_path):
    _sub(f"rm -rf {dir_path}".split(" "))
