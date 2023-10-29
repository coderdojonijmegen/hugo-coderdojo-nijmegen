from utils.dojo import Dojo


def test_dojo():
    dojo_event = Dojo.get_future_dojo_event()
    print(dojo_event)
