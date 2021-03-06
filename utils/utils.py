import subprocess
import os


def h_message(message):
    print(f"\n\n\033[1;37m{message}\033[0m\n")


def env_var(var_name, default_value=None):
    if var_name in os.environ:
        value = os.environ[var_name]
    elif default_value is not None:
        value = default_value
    else:
        raise EnvironmentError(f"{var_name} not found!")
    if var_name != "INPUT_GITHUBTOKEN":
        print(f"{var_name}={value}")
    return value


def _sub(args):
    print(args)
    with subprocess.Popen(args) as proc:
        proc.communicate()
        return proc.returncode


def git(args, message=None, working_dir=None):
    cwd = os.getcwd()
    if working_dir is not None:
        os.chdir(working_dir)
    try:
        cmd = f"/usr/bin/git {args}".split(" ")
        if message is not None:
            cmd.append(f"{message}")
        return _sub(cmd)
    finally:
        os.chdir(cwd)


def hugo(args):
    if _sub(f"./hugo {args}".split(" ")) != 0:
        exit(-1)


def rm_rf(dir_path):
    _sub(f"rm -rf {dir_path}".split(" "))
