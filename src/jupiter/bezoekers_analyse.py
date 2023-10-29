import json
from pathlib import Path
from requests import get
from datetime import datetime

class Events:

    def __init__(self, api_key: str, known_locations: list, event_ids_to_remove: list) -> None:
        self.known_locations = known_locations
        self.events = self.load_dojo_data(api_key)
        self.events = self.get_filtered_events(event_ids_to_remove, self.events)

    def load_dojo_data(self, api_key):
        if not Path("events.json").is_file():

            auth_header = {"Authorization": f"Bearer {api_key}"}

            events = []
            has_more_items = True
            page = 0

            while has_more_items:
                page += 1
                r = get(f"https://www.eventbriteapi.com/v3/organizations/187233351803/events/?order_by=created_asc&page={page}&expand=venue", headers=auth_header)
                events_json = r.json()
                for event_json in events_json["events"]:
                    event_json["event_date"] = event_json["start"]["local"]
                    ra = get(f"https://www.eventbriteapi.com/v3/events/{event_json['id']}/attendees", headers=auth_header)
                    event_json['attendees'] = ra.json()
                    rd = get(f"https://www.eventbriteapi.com/v3/events/{event_json['id']}/description", headers=auth_header)
                    event_json['description_ext'] = rd.json()
                    events.append(event_json)
                has_more_items = events_json["pagination"]["has_more_items"]

            with open("events.json", 'w') as events_file:
                events_file.write(json.dumps(events))
        else:
            with open("events.json", 'r') as events_file:
                events = json.load(events_file)
        return events

    def location(self, event: dict) -> str:
        loc = 'online' if event['online_event'] else event['venue']['name']
        for known_location in self.known_locations:
            if known_location in loc.lower():
                return known_location
        return loc

    def get_filtered_events(self, event_ids_to_remove: list, events: list) -> list:
        for event in list(events):
            if int(event['id']) in event_ids_to_remove:
                events.remove(event)
        return events
    
    def get_dojos(self) -> tuple:
        columns = ["maand", "datum", "locatie", "onderwerp", "aantal tickets", "gekocht", "ingecheckt"]
        dojos = []
        for event in self.events:
            dojos.append([
                as_month(event), 
                as_date(event), 
                'online' if event['online_event'] else event['venue']['name'], 
                event['name']['text'], 
                event['capacity'], 
                get_sold_tickets(event), 
                get_checkins(event)
            ])
        return columns, dojos
    
    def get_checkins_over_time(self) -> tuple:
        axes = {
            'x': 'datum',
            'y': ['checkins', 'online checkins']
        }
        checkins_over_time = {
            'datum': [as_date(event) for event in self.events],
            'checkins': [get_checkins(event) if not event['online_event'] else 0 for event in self.events],
            'online checkins': [get_checkins(event) if event['online_event'] else 0  for event in self.events],
        }
        return axes, checkins_over_time
    
    def get_checkins_per_location_over_time(self) -> tuple:
        locations = list(set([self.location(event) for event in self.events]))

        checkins = {
            'datum': [as_date(event) for event in self.events],
        }
        for loc in locations:
            checkins[loc] = [get_checkins(event) if self.location(event) == loc else 0 for event in self.events]

        return locations, checkins

    def get_checkins_per_month_of_the_year(self) -> tuple:
        columns = ['maand', 'min', 'gemiddeld', 'max']
        axes = {
            'x': 'maand',
            'y': ['min', 'gemiddeld', 'max']
        }
        months = {}
        for event in self.events:
            if not event['online_event']:
                month = as_month(event)
                if not month in months:
                    months[month] = {}
                months[month][as_date(event)] = get_checkins(event)

        monthly = []
        for month in sorted(months):
            total = 0
            min = 100
            max = 0
            for datum in months[month]:
                checkins = months[month][datum]
                total += checkins
                if checkins < min:
                    min = checkins
                if checkins > max:
                    max = checkins
            avg = total/len(months[month])
            monthly.append([month, min, avg, max])
        return columns, axes, monthly
    
def get_sold_tickets(event):
    return event['attendees']['pagination']['object_count']


def get_checkins(event):
    return len([attendee for attendee in event['attendees']['attendees'] if attendee['checked_in']])

def as_datetime(event):
    return datetime.strptime(event["event_date"], "%Y-%m-%dT%H:%M:%S")

def as_month(event):
    return datetime.strftime(as_datetime(event), '%m')

def as_date(event):
    return datetime.strftime(as_datetime(event), '%Y-%m-%d')
