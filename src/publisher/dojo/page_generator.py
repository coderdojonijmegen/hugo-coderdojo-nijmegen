import re
from datetime import datetime, timedelta
from pathlib import Path

import frontmatter

from publisher.eventbrite import Event

DOJO_PAGE_TEMPLATE = "./archetypes/dojos-template.md"


def generate_dojo_page(event: Event) -> None:
    template = _load_template()
    created_at = datetime.strftime(datetime.now(), '%Y-%m-%dT00:00:00+0100')
    dojo_file = Path("./content/dojos/").resolve() / f"{event.id}.md"
    if dojo_file.exists():
        created_at = frontmatter.load(dojo_file)["date"]

    page = _parse_to_page(template, event, created_at)
    _write_to_dojo_page(page, dojo_file)


def _load_template() -> str:
    with open(DOJO_PAGE_TEMPLATE, "r") as template_file:
        return template_file.read()


def _parse_to_page(template: str, event: Event, created_at: str) -> str:
    description = _replace_nth(
        event.description,
        "<h2>",
        "\n\n<!--more-->\n\n<h2>",
        2
    )
    description = _replace_nth(
        description,
        "<h3>",
        "\n\n<!--more-->\n\n<h3>",
        2
    )
    description = re.sub(r"<div>.*</div><div.*<h2>", "<h2>", description, 0)
    description = re.sub(r"<div>.*</div><div.*<h3>", "<h3>", description, 0)
    return template \
        .replace("{{title}}", "#" + event.title) \
        .replace("{{date}}", created_at) \
        .replace("{{start_time}}", datetime.strftime(event.start_time,
                                                     '%Y-%m-%dT%H:%M:%S%z')) \
        .replace("{{end_time}}", datetime.strftime(event.end_time,
                                                   '%Y-%m-%dT%H:%M:%S%z')) \
        .replace("{{start_date}}", datetime.strftime(event.start_time,
                                                     '%Y-%m-%d')) \
        .replace("{{latest_signup_datetime}}",
                 datetime.strftime(event.start_time - timedelta(hours=2),
                                   '%Y-%m-%dT%H:%M:%S%z')) \
        .replace("{{earliest_signup_datetime}}",
                 datetime.strftime(event.start_time - timedelta(weeks=4),
                                   '%Y-%m-%dT%H:%M:%S%z')) \
        .replace("{{location}}", event.location) \
        .replace("{{event_url}}", event.url) \
        .replace("{{picture_url}}", event.picture_url) \
        .replace("{{event_description}}", description) \
        .replace("<strong><strong>", "**").replace("</strong></strong>", "**") \
        .replace("<strong>", "**").replace("</strong>", "**") \
        .replace("<h2>", "\n## ").replace("</h2>", "") \
        .replace("<h3>", "\n## ").replace("</h3>", "") \
        .replace("<p>", "\n\n").replace("</p>", "") \
        .replace("<ul>", "").replace("</ul>", "") \
        .replace("<li>", "\n - ").replace("</li>", "") \
        .replace("<br>", "\n").replace("</li>", "") \
        .replace("</div></div>", "")


def _replace_nth(string: str, sub: str, wanted: str, n: int) -> str:
    found_strings = [m.start() for m in re.finditer(sub, string)]
    if found_strings:
        where = found_strings[n - 1]
        before = string[:where]
        after = string[where:]
        after = after.replace(sub, wanted, 1)
        return before + after
    else:
        return string


def _write_to_dojo_page(page: str, dojo_filename: Path) -> None:
    with open(dojo_filename, 'w') as f:
        f.write(page)
