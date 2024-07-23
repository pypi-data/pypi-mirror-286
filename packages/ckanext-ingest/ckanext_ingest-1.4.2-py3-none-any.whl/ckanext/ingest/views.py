from __future__ import annotations

from typing import Any

from flask import Blueprint
from flask.views import MethodView

import ckan.plugins.toolkit as tk
from ckan.lib import base
from ckan.logic import parse_params

from . import config

ingest = Blueprint("ingest", __name__)


class IngestView(MethodView):
    def _check_access(self):
        try:
            tk.check_access("ingest_web_ui", {"user": tk.g.user})
        except tk.NotAuthorized:
            tk.abort(401, tk._("Unauthorized to ingest data"))

    def _render(self, errors: dict[str, Any] | None = None):
        data: dict[str, Any] = {
            "user_dict": tk.g.userobj,
            "errors": errors,
            "base_template": config.base_template(),
        }
        return base.render("ingest/index.html", extra_vars=data)

    def get(self):
        self._check_access()
        return self._render()

    def post(self):
        self._check_access()

        try:
            data = parse_params(tk.request.form)
            data.update(parse_params(tk.request.files))
            result = tk.get_action("ingest_import_records")({}, data)

            for id_ in result:
                pkg = tk.get_action("package_show")({}, {"id": id_})
                tk.h.flash_success(
                    "Success: <a href='{url}'>{title}</a>".format(
                        title=pkg["title"],
                        url=tk.h.url_for(pkg["type"] + ".read", id=pkg["name"]),
                    ),
                    True,
                )

            return tk.redirect_to("ingest.index")

        except tk.ValidationError as e:
            errors = e.error_summary

        return self._render(errors), 409


ingest.add_url_rule("/ingest/from-source", view_func=IngestView.as_view("index"))
