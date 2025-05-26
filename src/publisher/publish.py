import logging
from datetime import datetime

from dotenv import load_dotenv

from publisher.dojo.page_generator import generate_dojo_page
from publisher.env import Environment, GithubConf
from publisher.eventbrite import get_future_events, get_event_details
from publisher.executor import execute
from publisher.git import git, git_configure, git_commit_changes, git_log
from publisher.hugo import download_hugo, run_hugo
from publisher.instruction_repos import clone_instructions
from publisher.notifier import notify
from publisher.og_proxy import stop_og_proxy, start_og_proxy_in_background

GH_PAGES = "gh-pages"
REF_MAIN = "refs/heads/main"

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
        git_configure(env.github.actor)
        clone_instructions(env.github)
        download_hugo(env.hugo)
        clone_site_branch(env.github)
        git_log()
        start_og_proxy_in_background()
        og_proxy_started = True

        future_events = get_future_events(env.eventbrite.api_key)
        for future_event in future_events:
            event = get_event_details(future_event, env.eventbrite.api_key)
            generate_dojo_page(event)

        run_hugo(GH_PAGES)
        add_cname(env.cname)
        git_commit_changes(f"Publishing Site {env.cname} to {GH_PAGES} at {env.github.sha} on {now}.", GH_PAGES)
        git_log(GH_PAGES)
        if env.github.branch == REF_MAIN:
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


def clone_site_branch(conf: GithubConf) -> None:
    logger.info("cloning site branch")
    git(f"clone --depth=1 --single-branch --branch {GH_PAGES} https://x-access-token:{conf.token}@github.com"
        f"/{conf.repository}.git {GH_PAGES}")
    execute(f"rm -rf {GH_PAGES}/*")


def add_cname(cname: str):
    with open(f"{GH_PAGES}/CNAME", "w") as f:
        f.write(cname)


if __name__ == "__main__":
    env = Environment.load()
    exit(publish(env))
