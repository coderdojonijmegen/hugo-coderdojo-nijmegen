from datetime import datetime

from requests import get


# documentation: https://www.eventbrite.nl/platform/api
# new API key from: https://www.eventbrite.nl/platform/api-keys/
#   note: each visit of this page creates a new API key at https://www.eventbrite.nl/account-settings/apps
# API key stored in Bitwarden vault Bas
auth_header = {"Authorization": "Bearer <api-key>"}

events = []
has_more_items = True
page = 0

while has_more_items:
    page += 1
    r = get(f"https://www.eventbriteapi.com/v3/organizations/187233351803/events/?order_by=created_desc&page={page}&expand=venue", headers=auth_header)
    events_json = r.json()
    for event_json in events_json["events"]:
        start = datetime.strptime(event_json["start"]["local"], "%Y-%m-%dT%H:%M:%S")
        event_json["event_date"] = start
        if start.year == 2022:
            ra = get(f"https://www.eventbriteapi.com/v3/events/{event_json['id']}/attendees", headers=auth_header)
            event_json['attendees'] = ra.json()
            rd = get(f"https://www.eventbriteapi.com/v3/events/{event_json['id']}/description", headers=auth_header)
            event_json['description_ext'] = rd.json()
            events.append(event_json)
    has_more_items = events_json["pagination"]["has_more_items"]


def get_sold_tickets(event):
    return event['attendees']['pagination']['object_count']


def get_checkins(event):
    return len([attendee for attendee in event['attendees']['attendees'] if attendee['checked_in']])


print("|maand | locatie | onderwerp | aantal tickets | gekocht | ingecheckt |")
print("|------|---------|-----------|----------------|---------|------------|")
for event in events:
    print(f"|{datetime.strftime(event['event_date'], '%m')} | {'online' if event['online_event'] else event['venue']['name']} "
          f"| {event['name']['text']} | {event['capacity']}| {get_sold_tickets(event)}| {get_checkins(event)}|")

