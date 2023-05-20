#!/usr/bin/env python3

import re
from datetime import datetime, timedelta
from os import path, environ

from requests import get

from utils.utils import h_message

API_KEY = environ["INPUT_EVENTBRITEAPIKEY"]

auth_header = {"Authorization": f"Bearer {API_KEY}"}


class Dojo:

    @staticmethod
    def get_future_dojo_event():
        r = get(f"https://www.eventbriteapi.com/v3/organizations/187233351803/events/"
                f"?order_by=created_desc"
                f"&time_filter=current_future"
                f"&page=1",
                headers=auth_header)
        future_events = r.json()
        if future_events["pagination"]["object_count"] == 0:
            h_message("geen geplande dojo's gevonden")
            return None

        event_shorts = "\n - ".join([f"{future_event['name']['text']}" for future_event in future_events["events"]])
        h_message(f"geplande dojo(s): \n - {event_shorts}")
        latest_event = future_events["events"][0]
        return latest_event["resource_uri"] if latest_event["status"] == "live" else None

    @staticmethod
    def get_dojo_info(dojo_event_url):
        r = get(f"{dojo_event_url}?expand=venue", headers=auth_header)
        event = r.json()
        rd = get(f"{dojo_event_url}description", headers=auth_header)
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
        with open(template, "r") as template_file:
            template = template_file.read()

        dojo_filename = Dojo.get_dojo_filename(future_dojo_event_info)
        with open(dojo_filename, "w") as dojo_file:
            print(f"{dojo_filename} gemaakt")
            dojo_file.write(template
                            .replace("{{title}}", "#" + future_dojo_event_info['event_title'])
                            .replace("{{date}}", datetime.strftime(datetime.now(), '%Y-%m-%dT00:00:00+0100'))
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
                            .replace("<p><strong>", "\n## ").replace("</strong></p>", "")
                            .replace("<h2>", "\n## ").replace("</h2>", "")
                            .replace("<p>", "\n\n").replace("</p>", "")
                            .replace("<ul>", "").replace("</ul>", "")
                            .replace("<li>", "\n - ").replace("</li>", "")
                            )

    @staticmethod
    def get_dojo_filename(future_dojo_event_info):
        return "content/dojos/" + future_dojo_event_info['event_id'] + ".md"


if __name__ == "__main__":
    futureDojoEventUrl = Dojo.get_future_dojo_event()
    if futureDojoEventUrl is not None:
        dojo_info = Dojo.get_dojo_info(futureDojoEventUrl)
        if not Dojo.dojo_page_already_exists(dojo_info):
            Dojo.write_dojo_page(dojo_info, "archetypes/dojos-template.md")
