import time
import threading
import logging
from flask import Flask, request

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

def background_process(name):
    logging.info(f"[BG] Start processing {name}")
    sleep_time = 0
    if name.startswith("sleep_1min"):
        sleep_time = 60
    elif name.startswith("sleep_10min"):
        sleep_time = 600
    elif name.startswith("sleep_60min"):
        sleep_time = 3600

    logging.info(f"[BG] Sleeping for {sleep_time} seconds...")
    time.sleep(sleep_time)
    logging.info(f"[BG] Finished processing {name}")

@app.route("/", methods=["POST"])
def handle_event():
    event = request.get_json()
    name = event.get("name")
    bucket = event.get("bucket")
    logging.info(f"Received file: {name} in bucket: {bucket}")

    threading.Thread(target=background_process, args=(name,)).start()

    return "", 204