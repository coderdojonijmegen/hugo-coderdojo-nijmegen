from utils.dojo import Dojo


def test_get_future_dojo_events():
    dojo_events = Dojo.get_future_dojo_events()

    for dojo_event in dojo_events:
        assert 'https://www.eventbriteapi.com/v3/events/' in dojo_event


def test_get_dojo_info():
    dojo_events = Dojo.get_future_dojo_events()
    if len(dojo_events) > 0:
        dojo_info = Dojo.get_dojo_info(dojo_events[0])
        assert "location" in dojo_info
        assert "event_description" in dojo_info
