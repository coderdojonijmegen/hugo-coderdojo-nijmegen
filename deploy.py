#!/usr/bin/env python3

import os
import re
import tarfile
import subprocess
from datetime import datetime
import requests

from dojo import Dojo

DEFAULT_HUGO_VERSION = "extended_0.74.3"
HUGO_TAR_GZ = "hugo.tar.gz"
HUGO_DOWNLOAD_URL = "https://github.com/gohugoio/hugo/releases/download/v{hugo_base_version}/" \
                    "hugo_{hugo_version}_Linux-64bit.tar.gz"
REF_MASTER = "refs/heads/master"
GH_PAGES = "gh-pages"
TMP_GH_PAGES = "/tmp/gh-pages"
TMP_MCS = "/tmp/mcs"
MCS = "mcs"


def env_var(var_name, default_value=None):
    if var_name in os.environ:
        value = os.environ[var_name]
    elif default_value is not None:
        value = default_value
    else:
        raise EnvironmentError(var_name + " not found!")
    if var_name != "INPUT_GITHUBTOKEN":
        print(f"var_name={value}")
    return value


github_event_name = env_var("GITHUB_EVENT_NAME")
github_branch = env_var("GITHUB_REF")
github_repo = env_var("GITHUB_REPOSITORY")
github_actor = env_var("GITHUB_ACTOR")
github_sha = env_var("GITHUB_SHA")
github_token = env_var("INPUT_GITHUBTOKEN")
hugo_version = env_var("INPUT_HUGOVERSION", DEFAULT_HUGO_VERSION)
hugo_base_version = re.compile(r"(\d+.\d+.\d+)").search(hugo_version).group(0)
hugo_args = env_var("INPUT_ARGS", "")
cname = env_var("INPUT_CNAME", github_repo)


url = HUGO_DOWNLOAD_URL.format(hugo_base_version=hugo_base_version, hugo_version=hugo_version)


def h(message):
    print(f"\n\n\033[1;37m{message}\033[0m\n")


futureDojoEventUrl = Dojo.get_future_dojo_event()
if futureDojoEventUrl is not None:
    dojo_info = Dojo.get_dojo_info(futureDojoEventUrl)
    if not Dojo.dojo_page_already_exists(dojo_info):
        Dojo.write_dojo_page(dojo_info)
    elif github_event_name == "schedule" and datetime.now().hour != 1:
        h("publiceer alleen als er een nieuwe dojo is gepland of 's nachts om 1 uur")
        exit(0)


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
            cmd.append(f"\"{message}\"")
        return _sub(cmd)
    finally:
        os.chdir(cwd)


def hugo(args):
    if _sub(f"./hugo {args}".split(" ")) != 0:
        exit(-1)


def rm_rf(dir_path):
    _sub(f"rm -rf {dir_path}".split(" "))


git(f"config --global user.name {github_actor}")
git(f"config --global user.email {github_actor}@users.noreply.github.com")

git("add -A")
git("diff --cached")
git("commit -m", message=f"{futureDojoEventUrl} toegevoegd")
if github_branch == REF_MASTER:
    git("push")
else:
    print("=> not pushing when not on master")

with open("instructies.txt", "r") as inst:
    instruction_repos = inst.readlines()

h("clone instruction repositories")
for instruction_repo in instruction_repos:
    if len(instruction_repo.strip()) > 0:
        repo, path = instruction_repo.strip().split(" ")
        git(f"clone --depth=1 --single-branch https://x-access-token:{github_token}@github.com/{repo}.git {path}")


def clone_build_push(branch, target_dir):
    h(f"clone, build, commit and push to {branch}")
    git(f"clone --depth=1 --single-branch --branch {branch} https://x-access-token:{github_token}@github.com"
        f"/{github_repo}.git {target_dir}")
    rm_rf(f"{target_dir}/*")

    hugo(f"{hugo_args} -d {target_dir}/")

    with open(f"{target_dir}/CNAME", "w") as cname_file:
        cname_file.write(cname)

    git("add -A", working_dir=target_dir)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    git(f"commit --allow-empty -am", message=f"Publishing Site {branch} at {github_sha } on {now}.", working_dir=target_dir)
    if github_branch == REF_MASTER:
        git("push --force", working_dir=target_dir)
    else:
        print("=> not pushing when not on master")


h(f"downloading {url} to {HUGO_TAR_GZ}")
with open(HUGO_TAR_GZ, "wb") as hugo_tar_gz:
    hugo_tar_gz.write(requests.get(url, allow_redirects=True).content)

h(f"extracting {HUGO_TAR_GZ}")
with tarfile.open(HUGO_TAR_GZ, "r:gz") as tar:
    tar.extract("hugo")

clone_build_push(GH_PAGES, TMP_GH_PAGES)
clone_build_push(MCS, TMP_MCS)
