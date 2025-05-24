from time import sleep

from flask import Flask, jsonify, Response
import threading

from requests import get

from og_proxy.og_client import fetch_og_data

app = Flask(__name__)


@app.get("/url/<path:url>")
def get_og_data(url: str) -> tuple[Response, int]:
    try:
        return jsonify(fetch_og_data(url)), 200
    except Exception as e:
        return jsonify({
            "error": {
                "url": url,
                "reason": str(e)
            }}), 500


@app.get("/health")
def health() -> tuple[str, int]:
    return "it works!", 200


def start_og_proxy() -> None:
    app.run()


def start_og_proxy_in_background() -> None:
    threading.Thread(target=start_og_proxy).start()
    sleep(5)
    r = get("http://127.0.0.1:5000/health")
    r.raise_for_status()


if __name__ == "__main__":
    start_og_proxy()
