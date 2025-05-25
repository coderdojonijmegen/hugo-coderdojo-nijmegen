import logging

from requests import post

from .env import NotifyConf

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__file__)

def notify(conf: NotifyConf, title: str, message: str, priority: int = 1) -> None:
    logger.info(f"notify: {title}, {message}, {priority}")
    r = post(conf.url, auth=(conf.user, conf.password), json={
        "topic": "coderdojo_github",
        "title": title,
        "message": message,
        "priority": priority
    })
    r.raise_for_status()
