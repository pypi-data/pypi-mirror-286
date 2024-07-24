# Gertrude --- GTD done right
# Copyright © 2020-2024 Tanguy Le Carrour <tanguy@bioneland.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import logging
from http import HTTPStatus as HTTP

from flask import Flask, request, session
from flask_cors import CORS
from werkzeug.exceptions import Forbidden, NotFound
from werkzeug.middleware.proxy_fix import ProxyFix

from gertrude.infrastructure.flask import services
from gertrude.infrastructure.flask.auth import blueprint as auth
from gertrude.infrastructure.flask.projects import blueprint as projects
from gertrude.infrastructure.flask.root import blueprint as root
from gertrude.infrastructure.flask.tasks import blueprint as tasks
from gertrude.infrastructure.settings import WsgiSettings
from gertrude.interfaces.to_http import as_html


def build_app(settings: WsgiSettings) -> Flask:
    services.define_settings(settings)

    configure_logging(settings)

    app = Flask(
        __name__,
        static_folder="./static/",
        static_url_path="/resources",
        template_folder="./templates/",
    )

    CORS(app)
    app.config.update(
        SECRET_KEY=settings.SECRET_KEY,
        DEBUG_SQL=settings.DEBUG_SQL,
        SESSION_COOKIE_NAME=settings.COOKIE_NAME,
        SESSION_COOKIE_SECURE=not app.config["DEBUG"],
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
    )

    if settings.PROXIED:
        app.wsgi_app = ProxyFix(  # type: ignore[method-assign]
            app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
        )

    app.teardown_appcontext(services.close_sessions)

    app.register_error_handler(HTTP.NOT_FOUND, handle_missing_routes)
    app.register_error_handler(HTTP.FORBIDDEN, handle_forbidden)

    app.register_blueprint(root, url_prefix="/")
    app.register_blueprint(tasks, url_prefix="/tasks")
    app.register_blueprint(projects, url_prefix="/projects")

    app.auth_links = []  # type: ignore[attr-defined]
    app.register_blueprint(auth, url_prefix="/auth")

    if settings.AUTHORIZED_IP:
        from gertrude.infrastructure.flask.ip import blueprint as ip

        app.register_blueprint(ip, url_prefix="/auth/ip")
        app.auth_links.append(  # type: ignore[attr-defined]
            {"route": "ip.login", "label": "IP", "icon": "network-wired"}
        )

    if settings.TOTP:
        from gertrude.infrastructure.flask.totp import blueprint as totp

        app.register_blueprint(totp, url_prefix="/auth/totp")
        app.auth_links.append(  # type: ignore[attr-defined]
            {"route": "totp.login", "label": "TOTP", "icon": "clock"}
        )

    @app.before_request
    def check_csrf_token() -> None:
        # Only check CRSF token if a form has been submitted.
        # POST is also used on "magic" URL, i.e. `/__do__`.
        if request.method == "POST" and request.form:
            if session.get("csrf_token", "") != request.form.get("csrf_token", ""):
                raise Forbidden("pages-error-csrf-expired")

    return app


def configure_logging(settings: WsgiSettings) -> None:
    logging.basicConfig(
        format="[%(asctime)s] [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S %z",
        level=logging.DEBUG if settings.DEBUG else logging.WARNING,
    )


def handle_missing_routes(exc: NotFound) -> tuple[str, HTTP]:
    presenter = as_html.HtmlPresenter.from_template(
        "error",
        message=services.translator()("exceptions-not-found"),
        **services.context()
    )
    return str(presenter.body), HTTP.UNAUTHORIZED


def handle_forbidden(exc: Forbidden) -> tuple[str, HTTP]:
    presenter = as_html.HtmlPresenter.from_template(
        "error#message", message=services.translator()(exc.description)
    )
    return str(presenter.body), HTTP.OK
