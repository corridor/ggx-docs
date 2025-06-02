from __future__ import annotations

import pathlib

from flask import Flask


DOCS_DIR: pathlib.Path = pathlib.Path(__file__).parent / "site"

##########################################################


def create_app() -> Flask:
    from corridor_docs.user_manual import user_manual_view

    flask_app = Flask(__name__, static_folder=None)
    flask_app.url_map.strict_slashes = False
    flask_app.config.from_mapping({"DEBUG": True, "PORT": 5005})

    flask_app.add_url_rule("/", view_func=user_manual_view)
    flask_app.add_url_rule("/<path:path>", view_func=user_manual_view)

    return flask_app
