from dataclasses import dataclass
from os import environ


@dataclass
class GithubConf:
    server_url: str
    repository: str
    run_id: str
    event_name: str
    branch: str
    actor: str
    sha: str
    token: str


@dataclass
class HugoConf:
    version: str


@dataclass
class NotifyConf:
    url: str
    user: str
    password: str


@dataclass
class EventbriteConf:
    api_key: str


@dataclass
class Environment:
    github: GithubConf
    hugo: HugoConf
    notify: NotifyConf
    eventbrite: EventbriteConf
    cname: str

    def __post_init__(self):
        self.github = GithubConf(**self.github)
        self.hugo = HugoConf(**self.hugo)
        self.notify = NotifyConf(**self.notify)
        self.eventbrite = EventbriteConf(**self.eventbrite)

    @staticmethod
    def load():
        try:
            return Environment(**{
                "github": {
                    "server_url": environ["GITHUB_SERVER_URL"],
                    "repository": environ["GITHUB_REPOSITORY"],
                    "run_id": environ["GITHUB_RUN_ID"],
                    "event_name": environ["GITHUB_EVENT_NAME"],
                    "branch": environ["GITHUB_REF"],
                    "actor": environ["GITHUB_ACTOR"],
                    "sha": environ["GITHUB_SHA"],
                    "token": environ["VAR_GITHUB_TOKEN"],
                },
                "hugo": {
                    "version": environ["VAR_HUGO_VERSION"]
                },
                "notify": {
                    "url": environ["VAR_NOTIFY_URL"],
                    "user": environ["VAR_NOTIFY_USER"],
                    "password": environ["VAR_NOTIFY_PASS"],
                },
                "eventbrite": {
                    "api_key": environ["VAR_EVENTBRITE_API_KEY"],
                },
                "cname": environ["VAR_CNAME"]
            })
        except KeyError as e:
            e.add_note("Did you set the environment variables?")
            raise e
