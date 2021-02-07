import flask

__all__ = ["app"]

app = flask.Flask("tts_cache")

app.config.from_json("config.json")
