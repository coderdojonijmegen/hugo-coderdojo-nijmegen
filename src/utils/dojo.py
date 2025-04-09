#!/usr/bin/env python3

import re
from datetime import datetime, timedelta
from os import path

import frontmatter
from requests import get

from utils.utils import h_message


class Dojo:

    def __init__(self, eventbrite_api_key: str):
        self.auth_header = {"Authorization": f"Bearer {eventbrite_api_key}"}

    def get_future_dojo_events(self) -> list:
        r = get(f"https://www.eventbriteapi.com/v3/organizations/187233351803/events/"
                f"?order_by=created_desc"
                f"&time_filter=current_future"
                f"&page=1",
                headers=self.auth_header)
        future_events = r.json()
        if future_events["pagination"]["object_count"] == 0:
            h_message("geen geplande dojo's gevonden")
            return None

        event_shorts = "\n - ".join([f"{future_event['name']['text']}" for future_event in future_events["events"]])
        h_message(f"geplande dojo(s): \n - {event_shorts}")

        return [future_event['resource_uri'] for future_event in future_events['events']]

    def get_dojo_info(self, dojo_event_url):
        r = get(f"{dojo_event_url}?expand=venue", headers=self.auth_header)
        event = r.json()
        rd = get(f"{dojo_event_url}description", headers=self.auth_header)
        event["description_ext"] = rd.json()["description"]

        return {
            "event_id": event["id"],
            "event_title": event["name"]["text"].strip().split("#")[1],
            "picture_url": event["logo"]["url"],
            "event_url": event["url"],
            "event_description": event["description_ext"],
            "location": "online" if event["online_event"] else event["venue"]["address"]["localized_address_display"],
            "start_time": datetime.strptime(event["start"]["local"], '%Y-%m-%dT%H:%M:%S'),
            "end_time": datetime.strptime(event["end"]["local"], '%Y-%m-%dT%H:%M:%S')
        }

    @staticmethod
    def replace_nth(string, sub, wanted, n):
        found_strings = [m.start() for m in re.finditer(sub, string)]
        if found_strings:
            where = found_strings[n - 1]
            before = string[:where]
            after = string[where:]
            after = after.replace(sub, wanted, 1)
            return before + after
        else:
            return string

    @staticmethod
    def dojo_page_already_exists(future_dojo_event_info):
        dojo_filename = Dojo.get_dojo_filename(future_dojo_event_info)
        return path.exists(dojo_filename)

    @staticmethod
    def parse_template(template: str, dojo_event_info: dict, date_created: str) -> str:
        description = Dojo.replace_nth(
            dojo_event_info['event_description'],
            "<h2>",
            "\n\n<!--more-->\n\n<h2>",
            2
        )
        description = Dojo.replace_nth(
            description,
            "<h3>",
            "\n\n<!--more-->\n\n<h3>",
            2
        )
        description = re.sub(r"<div>.*</div><div.*<h2>", "<h2>", description, 0)
        description = re.sub(r"<div>.*</div><div.*<h3>", "<h3>", description, 0)
        return template \
            .replace("{{title}}", "#" + dojo_event_info['event_title']) \
            .replace("{{date}}", date_created) \
            .replace("{{start_time}}", datetime.strftime(dojo_event_info['start_time'],
                                                         '%Y-%m-%dT%H:%M:%S%z')) \
            .replace("{{end_time}}", datetime.strftime(dojo_event_info['end_time'],
                                                       '%Y-%m-%dT%H:%M:%S%z')) \
            .replace("{{start_date}}", datetime.strftime(dojo_event_info['end_time'],
                                                         '%Y-%m-%d')) \
            .replace("{{latest_signup_datetime}}",
                     datetime.strftime(dojo_event_info['start_time'] - timedelta(hours=2),
                                       '%Y-%m-%dT%H:%M:%S%z')) \
            .replace("{{earliest_signup_datetime}}",
                     datetime.strftime(dojo_event_info['start_time'] - timedelta(weeks=4),
                                       '%Y-%m-%dT%H:%M:%S%z')) \
            .replace("{{location}}", dojo_event_info['location']) \
            .replace("{{event_url}}", dojo_event_info['event_url']) \
            .replace("{{picture_url}}", dojo_event_info['picture_url']) \
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

    @staticmethod
    def write_dojo_page(dojo_event_info, template):
        dojo_filename = Dojo.get_dojo_filename(dojo_event_info)

        date_created = datetime.now()
        if Dojo.dojo_page_already_exists(dojo_event_info):
            date_created = datetime.strptime(frontmatter.load(dojo_filename)["date"], '%Y-%m-%dT%H:%M:%S%z')

        with open(template, "r") as template_file:
            template = template_file.read()

        with open(dojo_filename, "w") as dojo_file:
            print(f"{dojo_filename} gemaakt")
            dojo_file.write(Dojo.parse_template(
                template,
                dojo_event_info,
                datetime.strftime(date_created, '%Y-%m-%dT00:00:00+0100')
            ))

    @staticmethod
    def get_dojo_filename(dojo_event_info):
        return "content/dojos/" + dojo_event_info['event_id'] + ".md"
