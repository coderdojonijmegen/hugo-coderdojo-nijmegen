from pathlib import Path

from dotenv import load_dotenv

from publisher.env import Environment


def test_load():
    load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env-test")

    env = Environment.load()
    assert env.github is not None
