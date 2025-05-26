import logging
import os
from time import sleep

from flask import Flask, jsonify, Response
import threading

from requests import get

from publisher.og_proxy import fetch_og_data

logger = logging.getLogger(__file__)

app = Flask(__name__)


@app.get("/url/<path:url>")
def get_og_data(url: str) -> tuple[Response, int]:
    try:
        data = fetch_og_data(url)
        logger.info(f"fetched {url}: {data}")
        return jsonify(data), 200
    except Exception as e:
        error = {
            "error": {
                "url": url,
                "reason": str(e)
            }
        }
        logger.error(f"error fetching {url}: {error}")
        return jsonify(error), 500


@app.get("/health")
def health() -> tuple[str, int]:
    return "it works!", 200


exiting = False


@app.get("/shutdown")
def shutdown() -> tuple[str, int]:
    global exiting
    exiting = True
    logger.info("server shutting down")
    return "Server shutting down...", 200


@app.teardown_request
def teardown(_):
    global exiting
    if exiting:
        os._exit(0)


def start_og_proxy() -> None:
    app.run()


def start_og_proxy_in_background() -> None:
    threading.Thread(target=start_og_proxy).start()
    sleep(5)
    r = get("http://127.0.0.1:5000/health")
    r.raise_for_status()


def stop_og_proxy() -> None:
    logger.info("stopping og proxy")
    r = get("http://127.0.0.1:5000/shutdown")
    r.raise_for_status()


if __name__ == "__main__":
    start_og_proxy_in_background()
    stop_og_proxy()
