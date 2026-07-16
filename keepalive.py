import os
import threading
from flask import Flask

_app = Flask(__name__)


@_app.route("/")
def health():
    return "Vivi is awake.", 200


def start_keepalive_server():
    """Runs a tiny Flask server in a background thread.

    This exists purely so hosting platforms that require an HTTP-bound
    service (like Render's free Web Service tier) see this as a valid
    web service, and so an external uptime pinger (UptimeRobot,
    cron-job.org, etc.) has something to hit every few minutes to keep
    the instance from sleeping.

    The actual bot logic runs separately via Telegram polling — this
    server does nothing bot-related.
    """
    port = int(os.environ.get("PORT", 8080))

    def run():
        _app.run(host="0.0.0.0", port=port)

    thread = threading.Thread(target=run, daemon=True)
    thread.start()