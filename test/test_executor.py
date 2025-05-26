from publisher.executor import execute


def test_execute():
    i, out, err = execute("ps")

    assert i == 0
    assert "PID" in out
