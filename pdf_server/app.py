import json

import flask

__all__ = ["app"]

app = flask.Flask("tts_cache")


with open("config.json") as file:
    app.config.update(json.load(file))
