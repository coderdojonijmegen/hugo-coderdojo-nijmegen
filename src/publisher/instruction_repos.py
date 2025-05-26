import logging

from publisher.env import GithubConf
from publisher.git import git

logger = logging.getLogger(__file__)


def clone_instructions(conf: GithubConf) -> None:
    logger.info("loading instructions.txt")
    with open("instructies.txt", "r") as f:
        instruction_repolist = f.readlines()

    for repo, path in [r.strip().split(" ") for r in instruction_repolist]:
        logger.info(f"cloning {repo} to {path}")
        git(f"clone --depth=1 --single-branch https://x-access-tken:{conf.token}@github.com/{repo}.git {path}")
