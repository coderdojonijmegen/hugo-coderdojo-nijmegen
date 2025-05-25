import logging

from dotenv import load_dotenv

from publisher.hugo import download_hugo
from publisher.instruction_repos import clone_instructions
from publisher.env import Environment
from publisher.notifier import notify

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__file__)
logger.info(f"{__file__} started")

def publish(env: Environment) -> None:
    try:
        clone_instructions(env.github)
        download_hugo(env.hugo)
        notify(env.notify, "successfully published CoderDojo site!")
    except Exception as e:
        notify(env.notify, "error publishing CoderDojo site!", str(e))

if __name__ == "__main__":
    env = Environment.load()
    publish(env)
