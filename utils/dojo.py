#!/usr/bin/env python3

import requests
import re
import os.path
from datetime import datetime
from bs4 import BeautifulSoup

CODER_DOJO_NIJMEGEN_EVENTS_PAGE_URL = "https://www.eventbrite.nl/o/stichting-coderdojo-nijmegen-12043791497"


class Dojo:

    @staticmethod
    def get_future_dojo_event():
        events_page = requests.get(CODER_DOJO_NIJMEGEN_EVENTS_PAGE_URL).text
        events_page_soup = BeautifulSoup(events_page, 'html.parser')

        future_event_cards = events_page_soup.find_all("div", "eds-event-card--consumer")
        future_event_urls = []
        for future_event_card in future_event_cards:
            future_event_urls.append(future_event_card
                                     .find("a", "eds-event-card-content__action-link")
                                     .attrs['href']
                                     .split('?')[0]
                                     )

        future_event_urls_formatted_list = "\n - " + "\n - ".join(future_event_urls) \
            if len(future_event_urls) > 1 else "\n - " + future_event_urls[0]
        print(f"found future event urls: {future_event_urls_formatted_list}")
        return future_event_urls[0] if len(future_event_urls) == 1 else None

    @staticmethod
    def get_dojo_info(dojo_event_url):
        dojo_event = requests.get(dojo_event_url).text
        dojo_event_soup = BeautifulSoup(dojo_event, 'html.parser')

        dojo_event_title = dojo_event_soup.find_all("div", {"data-automation": "listing-event-description"})[0].text
        dojo_event_hero_picture_url = dojo_event_soup.find_all("div", "listing-hero")[0].find_all("picture")[0].attrs['content']
        dojo_event_html = "\n".join([str(item) for item in dojo_event_soup.find_all("div", "structured-content-rich-text")[0].contents])
        dojo_event_details_soup = dojo_event_soup.find_all("div", "event-details hide-small")[0]
        dojo_event_details_date_text = dojo_event_details_soup.find_all("p", "js-date-time-first-line")[0].text
        dojo_event_details_time_start, dojo_event_details_time_end = [item['content'] for item in dojo_event_details_soup.find_all("div", "event-details__data")[0].find_all("meta")]
        dojo_event_details_location = dojo_event_details_soup.find_all("div", "event-details__data")[1].text
        return {
            "event_title": dojo_event_title.strip().split("#")[1],
            "picture_url": dojo_event_hero_picture_url,
            "event_url": dojo_event_url,
            "event_description": dojo_event_html,
            "event_date": dojo_event_details_date_text,
            "location": dojo_event_details_location.strip(),
            "start_time": datetime.strptime(dojo_event_details_time_start, '%Y-%m-%dT%H:%M:%S%z'),
            "end_time": datetime.strptime(dojo_event_details_time_end, '%Y-%m-%dT%H:%M:%S%z')
        }

    @staticmethod
    def replace_nth(string, sub, wanted, n):
        where = [m.start() for m in re.finditer(sub, string)][n-1]
        before = string[:where]
        after = string[where:]
        after = after.replace(sub, wanted, 1)
        return before + after

    @staticmethod
    def dojo_page_already_exists(future_dojo_event_info):
        dojo_filename = "content/dojos/" + future_dojo_event_info['event_title'].replace(":", "").replace(" ", "-").lower() + ".md"
        return os.path.exists(dojo_filename)

    @staticmethod
    def write_dojo_page(future_dojo_event_info):
        with open("../archetypes/dojos-template.md", "r") as template_file:
            template = template_file.read()

        dojo_filename = "content/dojos/" + future_dojo_event_info['event_title'].replace(":", "").replace(" ", "-").lower() + ".md"
        with open(dojo_filename, "w") as dojo_file:
            dojo_file.write(template
                            .replace("{{title}}", "#" + future_dojo_event_info['event_title'])
                            .replace("{{date}}", datetime.strftime(datetime.now(), '%Y-%m-%dT00:00:00+0100'))
                            .replace("{{start_time}}", datetime.strftime(future_dojo_event_info['start_time'], '%Y-%m-%dT%H:%M:%S%z'))
                            .replace("{{end_time}}", datetime.strftime(future_dojo_event_info['end_time'], '%Y-%m-%dT%H:%M:%S%z'))
                            .replace("{{start_date}}", datetime.strftime(future_dojo_event_info['end_time'], '%Y-%m-%d'))
                            .replace("{{location}}", future_dojo_event_info['location'])
                            .replace("{{event_url}}", future_dojo_event_info['event_url'])
                            .replace("{{picture_url}}", future_dojo_event_info['picture_url'])
                            .replace("{{event_description}}", Dojo.replace_nth(future_dojo_event_info['event_description'], "</p>\n<p>", "</p>\n\n<!--more-->\n\n<p>", 2))
                            .replace("<p><strong>", "\n## ").replace("</strong></p>", "")
                            .replace("<p>", "\n\n").replace("</p>", "")
                            .replace("<ul>", "").replace("</ul>", "")
                            .replace("<li>", "\n - ").replace("</li>", "")
                            )
            print("created " + dojo_filename)


if __name__ == "__main__":
    futureDojoEventUrl = Dojo.get_future_dojo_event()
    if futureDojoEventUrl is not None:
        dojo_info = Dojo.get_dojo_info(futureDojoEventUrl)
        if not Dojo.dojo_page_already_exists(dojo_info):
            Dojo.write_dojo_page(dojo_info)
