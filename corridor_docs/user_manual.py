from __future__ import annotations

from flask import Response, redirect, request, send_from_directory
from werkzeug.exceptions import NotFound

from corridor_docs import DOCS_DIR


def user_manual_view(path: str | None = None, url_prefix: str = "/") -> Response:
    """
    :param path:       The path to fetch from the docs folder
    :param url_prefix: Prefix for the URL endpoint to use
    """
    url_prefix = f"/{url_prefix.strip('/')}/" if url_prefix.strip("/") else "/"
    if path is None and not request.url.endswith("/"):
        return redirect(url_prefix)
    path = path if path else "index.html"

    if not DOCS_DIR.exists():
        return NotFound("Documentation not found at the expected location.")

    full_path = DOCS_DIR / path
    if full_path.is_dir():
        return send_from_directory(DOCS_DIR, path + "/index.html")
    if full_path.is_file():
        return send_from_directory(DOCS_DIR, path)

    # 404 - page not found => redirect to home page
    return redirect(url_prefix)
