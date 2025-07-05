import logging
import shutil
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

from publisher.dojo.page_generator import generate_dojo_page
from publisher.env import Environment, GithubConf
from publisher.eventbrite import get_future_events, get_event_details
from publisher.executor import execute
from publisher.git import git, git_configure, git_commit_changes, git_log, git_add_all_files
from publisher.hugo import download_hugo, run_hugo
from publisher.instruction_repos import clone_instructions
from publisher.notifier import notify
from publisher.og_proxy import stop_og_proxy, start_og_proxy_in_background

GH_PAGES = "gh-pages"
REF_MAIN = "refs/heads/main"
ROOT_DIR = Path(__file__).resolve().parent.parent.parent

load_dotenv()

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s:%(lineno)d %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M')
logger = logging.getLogger(__file__)
logger.info("start publish.py")

now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def publish(env: Environment) -> int:
    og_proxy_started = False
    try:
        cleanup_previous_if_local(env)

        logger.info("prepare publishing")
        git_configure(env.github.actor)
        download_hugo(env.hugo)
        create_prod_hugo_config()
        clone_instructions(env.github)
        clone_site_branch(env.github)
        git_log()
        start_og_proxy_in_background()
        og_proxy_started = True

        logger.info("generate dojo pages")
        generate_dojo_pages_for_future_events(env.eventbrite.api_key)
        git_commit_changes("Site update", None)
        if env.github.branch == REF_MAIN:
            logger.info("push changes to main")
            git("push")

        logger.info("publish to gh-pages")
        run_hugo(GH_PAGES)
        add_cname(env.cname)
        git_add_all_files(GH_PAGES)
        git_commit_changes(f"Publishing Site {env.cname} to {GH_PAGES} at {env.github.sha} on {now}.", GH_PAGES)
        git_log(GH_PAGES)
        if env.github.branch == REF_MAIN:
            logger.info(f"push to {GH_PAGES}")
            git("push --force", working_dir=GH_PAGES)
            notify(env.notify, "success!", "successfully published CoderDojo site!")
        else:
            notify(env.notify, "success - but not on main", "successfully built CoderDojo site!")
        return 0
    except Exception as e:
        logger.error(e)
        notify(env.notify, "error publishing CoderDojo site!", str(e))
        return -1
    finally:
        if og_proxy_started:
            stop_og_proxy()


def cleanup_previous_if_local(env: Environment):
    if env.github.branch == "refs/heads/local":
        logger.info("clean up old files")
        remove_instruction_directories()
        remove_gh_pages_directory()


def remove_instruction_directories():
    instructions_dir = ROOT_DIR / "content" / "instructies"
    if instructions_dir.exists():
        for instr_dir in instructions_dir.iterdir():
            if instr_dir.is_dir():
                logger.info(f"remove {instr_dir}")
                shutil.rmtree(instr_dir)


def remove_gh_pages_directory():
    gh_pages_dir = ROOT_DIR / GH_PAGES
    if gh_pages_dir.exists():
        shutil.rmtree(gh_pages_dir)

def create_prod_hugo_config():
    with open(ROOT_DIR / "config.toml", "r") as f:
        config = f.read()
    prod_config = config.replace("'error-remote-getjson'", "")
    with open(ROOT_DIR / "prod.toml", "w") as f:
        f.write(prod_config)

def clone_site_branch(conf: GithubConf) -> None:
    logger.info("cloning site branch")
    git(f"clone --depth=1 --single-branch --branch {GH_PAGES} https://x-access-token:{conf.token}@github.com"
        f"/{conf.repository}.git {GH_PAGES}")
    execute(f"rm -rf {GH_PAGES}/*")


def generate_dojo_pages_for_future_events(api_key) -> None:
    future_events = get_future_events(api_key)
    logger.info(f"found {len(future_events)} future events")
    for future_event in future_events:
        logger.info(f"getting more details for {future_event.title}")
        event = get_event_details(future_event, api_key)
        logger.info(f"generate dojo page for {event.title}")
        git(f"add {generate_dojo_page(event)}")


def add_cname(cname: str):
    with open(f"{GH_PAGES}/CNAME", "w") as f:
        f.write(cname)


if __name__ == "__main__":
    env = Environment.load()
    exit(publish(env))
