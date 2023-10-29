#!/usr/bin/env python3

import re
import tarfile
from datetime import datetime
import requests

from utils.dojo import Dojo
from utils.slack import notify
from utils.utils import h_message, git, hugo, rm_rf
from utils.env import env_var

DEFAULT_HUGO_VERSION = "extended_0.74.3"
HUGO_TAR_GZ = "hugo.tar.gz"
HUGO_DOWNLOAD_URL = "https://github.com/gohugoio/hugo/releases/download/v{hugo_base_version}/" \
                    "hugo_{hugo_version}_Linux-64bit.tar.gz"
DOJO_PAGE_TEMPLATE = "/site/archetypes/dojos-template.md"
REF_MAIN = "refs/heads/main"
GH_PAGES = "gh-pages"
TMP_GH_PAGES = "/tmp/gh-pages"
TMP_MCS = "/tmp/mcs"
MCS = "mcs"

github_server_url = env_var('GITHUB_SERVER_URL')
github_repository = env_var('GITHUB_REPOSITORY')
github_run_id = env_var('GITHUB_RUN_ID')
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
slack_channel = env_var("INPUT_SLACKWEBHOOK")
eventbrite_api_key = env_var("INPUT_EVENTBRITEAPIKEY")

hugo_download_url = HUGO_DOWNLOAD_URL.format(hugo_base_version=hugo_base_version, hugo_version=hugo_version)

dojo = Dojo(eventbrite_api_key)
futureDojoEventUrls = dojo.get_future_dojo_events()
if futureDojoEventUrls:
    for event_url in futureDojoEventUrls:
        dojo_info = dojo.get_dojo_info(event_url)
        Dojo.write_dojo_page(dojo_info, DOJO_PAGE_TEMPLATE)

git(f"config --global user.name {github_actor}")
git(f"config --global user.email {github_actor}@users.noreply.github.com")
git(f"config --global --add safe.directory /github/workspace")

git("add -A")
git("diff --cached")
git("commit -m", message=f"{','.join(futureDojoEventUrls)} toegevoegd/bijgewerkt", accept_git_non_zero_return=True)
if github_branch == REF_MAIN:
    git("push")
else:
    print("=> not pushing when not on main")

with open("instructies.txt", "r") as inst:
    instruction_repos = inst.readlines()

h_message("clone instruction repositories")
for instruction_repo in instruction_repos:
    if len(instruction_repo.strip()) > 0:
        repo, path = instruction_repo.strip().split(" ")
        git(f"clone --depth=1 --single-branch https://x-access-token:{github_token}@github.com/{repo}.git {path}")


def clone_build_push(args, target_branch, target_dir):
    h_message(f"clone, build, commit and push to {target_branch}")
    git(f"clone --depth=1 --single-branch --branch {target_branch} https://x-access-token:{github_token}@github.com"
        f"/{github_repo}.git {target_dir}")
    rm_rf(f"{target_dir}/*")

    ret_code, stdout, stderr = hugo(f"{args} -d {target_dir}/")
    if ret_code != 0:
        notify("Hugo error", f"{stdout}: {stderr}", slack_channel)
        exit(-1)

    with open(f"{target_dir}/CNAME", "w") as cname_file:
        cname_file.write(cname)

    git("add -A", working_dir=target_dir)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return_code, _, _ = git(f"commit -am", message=f"Publishing Site {cname} to {target_branch} at {github_sha} on {now}.",
                            working_dir=target_dir, accept_git_non_zero_return=True)
    if return_code == 0:
        if github_branch == REF_MAIN:
            git("push --force", working_dir=target_dir)
            _, stdout, _ = git("log -1 --pretty=%B")
            message = f"pushed changes from commit '{stdout}' to {target_branch}; see {github_server_url}/" \
                      f"{github_repository}/actions/runs/{github_run_id}"
            print(message)
            notify(target_branch, message, slack_channel)
        else:
            print("=> not pushing when not on main")
    else:
        print("=> no changes")


h_message(f"downloading {hugo_download_url} to {HUGO_TAR_GZ}")
with open(HUGO_TAR_GZ, "wb") as hugo_tar_gz:
    hugo_tar_gz.write(requests.get(hugo_download_url, allow_redirects=True).content)

h_message(f"extracting {HUGO_TAR_GZ}")
with tarfile.open(HUGO_TAR_GZ, "r:gz") as tar:
    tar.extract("hugo")

clone_build_push(hugo_args, GH_PAGES, TMP_GH_PAGES)
clone_build_push(f"{hugo_args} --config config-mcs.toml", MCS, TMP_MCS)
