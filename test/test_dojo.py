from os import environ

import pytest

from utils.dojo import Dojo


@pytest.mark.skip("actual API call")
def test_get_future_dojo_events():
    eventbrite_api_key = environ["INPUT_EVENTBRITEAPIKEY"]
    dojo_events = Dojo(eventbrite_api_key).get_future_dojo_events()

    for dojo_event in dojo_events:
        assert 'https://www.eventbriteapi.com/v3/events/' in dojo_event


@pytest.mark.skip("actual API call")
def test_get_dojo_info():
    eventbrite_api_key = environ["INPUT_EVENTBRITEAPIKEY"]
    with open("./archetypes/dojos-template.md", "r") as template_file:
        template = template_file.read()

    dojo = Dojo(eventbrite_api_key)
    dojo_events = dojo.get_future_dojo_events()
    for dojo_event in dojo_events:
        dojo_info = dojo.get_dojo_info(dojo_event)
        page = Dojo.parse_template(template, dojo_info, "2024-04-21")
        print(page)
        Dojo.write_dojo_page(dojo_info, "./archetypes/dojos-template.md")
