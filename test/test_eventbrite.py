import pytest
from dotenv import load_dotenv

from publisher.env import Environment
from publisher.eventbrite import get_future_events, get_event_details


@pytest.mark.skip("actual API call")
def test_get_future_events():
    load_dotenv()
    env = Environment.load()

    events = get_future_events(env.eventbrite.api_key)
    print(events)
    for event in events:
        event_details = get_event_details(event, env.eventbrite.api_key)
        print(event_details)