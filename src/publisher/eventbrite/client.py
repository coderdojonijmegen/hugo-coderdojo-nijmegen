from dataclasses import dataclass
from datetime import datetime

from requests import get


@dataclass
class FutureEvent:
    url: str
    title: str


@dataclass
class Event:
    id: str
    url: str
    title: str
    picture_url: str
    description: str
    location: str
    start_time: datetime
    end_time: datetime


def get_future_events(api_key: str) -> list[FutureEvent]:
    auth_header = {"Authorization": f"Bearer {api_key}"}
    r = get("https://www.eventbriteapi.com/v3/organizations/187233351803/events/"
            "?order_by=created_desc"
            "&time_filter=current_future"
            "&page=1",
            headers=auth_header)
    r.raise_for_status()
    future_events = r.json()
    if future_events["pagination"]["object_count"] == 0:
        return []
    else:
        return [FutureEvent(url=event["resource_uri"], title=event["name"]["text"]) for event in
                future_events["events"]]


def get_event_details(fevent: FutureEvent, api_key: str) -> Event:
    auth_header = {"Authorization": f"Bearer {api_key}"}
    r = get(f"{fevent.url}?expand=venue", headers=auth_header)
    r.raise_for_status()
    event = r.json()
    rd = get(f"{fevent.url}description", headers=auth_header)
    rd.raise_for_status()
    event["description_ext"] = rd.json()["description"]
    return Event(**{
        "id": event["id"],
        "title": event["name"]["text"].strip().split("#")[1],
        "picture_url": event["logo"]["url"],
        "url": event["url"],
        "description": event["description_ext"],
        "location": "online" if event["online_event"] else event["venue"]["address"]["localized_address_display"],
        "start_time": datetime.strptime(event["start"]["local"], '%Y-%m-%dT%H:%M:%S'),
        "end_time": datetime.strptime(event["end"]["local"], '%Y-%m-%dT%H:%M:%S')
    })
