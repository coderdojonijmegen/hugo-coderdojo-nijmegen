#!/usr/bin/env python3

import re
from datetime import datetime, timedelta
from os import path, environ

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
        where = [m.start() for m in re.finditer(sub, string)][n - 1]
        before = string[:where]
        after = string[where:]
        after = after.replace(sub, wanted, 1)
        return before + after

    @staticmethod
    def dojo_page_already_exists(future_dojo_event_info):
        dojo_filename = Dojo.get_dojo_filename(future_dojo_event_info)
        return path.exists(dojo_filename)

    @staticmethod
    def write_dojo_page(future_dojo_event_info, template):
        dojo_filename = Dojo.get_dojo_filename(future_dojo_event_info)

        date_created = datetime.now()
        if Dojo.dojo_page_already_exists(future_dojo_event_info):
            date_created = datetime.strptime(frontmatter.load(dojo_filename)["date"], '%Y-%m-%dT%H:%M:%S%z')

        with open(template, "r") as template_file:
            template = template_file.read()

        with open(dojo_filename, "w") as dojo_file:
            print(f"{dojo_filename} gemaakt")
            dojo_file.write(template
                            .replace("{{title}}", "#" + future_dojo_event_info['event_title'])
                            .replace("{{date}}", datetime.strftime(date_created, '%Y-%m-%dT00:00:00+0100'))
                            .replace("{{start_time}}", datetime.strftime(future_dojo_event_info['start_time'],
                                                                         '%Y-%m-%dT%H:%M:%S%z'))
                            .replace("{{end_time}}", datetime.strftime(future_dojo_event_info['end_time'],
                                                                       '%Y-%m-%dT%H:%M:%S%z'))
                            .replace("{{start_date}}", datetime.strftime(future_dojo_event_info['end_time'],
                                                                         '%Y-%m-%d'))
                            .replace("{{latest_signup_datetime}}",
                                     datetime.strftime(future_dojo_event_info['start_time'] - timedelta(hours=1),
                                                       '%Y-%m-%dT%H:%M:%S%z'))
                            .replace("{{location}}", future_dojo_event_info['location'])
                            .replace("{{event_url}}", future_dojo_event_info['event_url'])
                            .replace("{{picture_url}}", future_dojo_event_info['picture_url'])
                            .replace("{{event_description}}",
                                     re.sub(r"<div>.*<p>",
                                            "<p>",
                                            Dojo.replace_nth(
                                                future_dojo_event_info['event_description'],
                                                "</p>",
                                                "</p>\n\n<!--more-->\n\n",
                                                1
                                            ),
                                            1
                                            )
                                     ).replace("</div></div>", "")
                            .replace("<strong>", "\n** ").replace("</strong>", "**")
                            .replace("<h2>", "\n## ").replace("</h2>", "")
                            .replace("<p>", "\n\n").replace("</p>", "")
                            .replace("<ul>", "").replace("</ul>", "")
                            .replace("<li>", "\n - ").replace("</li>", "")
                            )

    @staticmethod
    def get_dojo_filename(future_dojo_event_info):
        return "content/dojos/" + future_dojo_event_info['event_id'] + ".md"
