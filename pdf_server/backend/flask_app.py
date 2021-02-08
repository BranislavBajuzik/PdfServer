import json
from pathlib import Path

import flask

__all__ = ["app"]

app = flask.Flask("tts_cache")

root_path = Path(__file__).absolute().parent.parent

app.config.update(json.loads(root_path.joinpath("config.json").read_text()))
