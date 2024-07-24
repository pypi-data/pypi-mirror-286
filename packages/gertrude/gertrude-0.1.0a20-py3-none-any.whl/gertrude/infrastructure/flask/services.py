# Gertrude --- GTD done right
# Copyright © 2023, 2024 Tanguy Le Carrour <tanguy@bioneland.org>
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

import secrets
import time
from importlib.metadata import version
from typing import Any, Optional

from flask import g, request
from flask import session as flask_session
from flask import url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from gertrude import __name__ as PACKAGE_NAME
from gertrude.domain.task_management.repositories import DomainHistory, Tasks, Users
from gertrude.domain.task_management.services import Calendar
from gertrude.infrastructure.requests import HttpEventStore
from gertrude.infrastructure.settings import WsgiSettings
from gertrude.infrastructure.sqlalchemy.projections import Tasks as TaskProjection
from gertrude.infrastructure.sqlalchemy.repositories import Projects
from gertrude.interfaces import l10n

__SESSIONS: list[str] = []
__SETTINGS: Optional[WsgiSettings] = None


def define_settings(settings: WsgiSettings) -> None:
    global __SETTINGS
    __SETTINGS = settings


def get_settings() -> WsgiSettings:
    if not __SETTINGS:
        raise RuntimeError("You must define the settings!")
    return __SETTINGS


def session(nom: str, dsn: str) -> Session:
    attribut = f"session_{nom}"
    if attribut not in g:
        options: dict[str, Any] = {}
        if get_settings().DEBUG_SQL:
            options["echo"] = True
            options["echo_pool"] = "debug"

        engine = create_engine(dsn, **options)
        g.setdefault(attribut, sessionmaker(bind=engine)())
        __SESSIONS.append(attribut)

    return g.get(attribut)  # type: ignore[no-any-return]


def close_sessions(exception: Optional[BaseException]) -> None:
    for name in __SESSIONS:
        if session := g.pop(name, None):
            if exception:
                session.rollback()
            else:
                session.commit()
            session.close()


def users() -> Users:
    if "users" not in g:
        g.users = Users()
    return g.users  # type: ignore[no-any-return]


def history() -> DomainHistory:
    if "history" not in g:
        g.history = DomainHistory(HttpEventStore(get_settings().EVENT_STORE_URL))
    return g.history  # type: ignore[no-any-return]


def tasks() -> Tasks:
    if "tasks" not in g:
        g.tasks = Tasks(history())
    return g.tasks  # type: ignore[no-any-return]


def task_projection() -> TaskProjection:
    if "task_projection" not in g:
        g.task_projection = TaskProjection(
            session("projections", get_settings().PROJECTION_DSN)
        )
    return g.task_projection  # type: ignore[no-any-return]


def projects() -> Projects:
    if "projects" not in g:
        g.projects = Projects(session("data", get_settings().DATA_DSN))
    return g.projects  # type: ignore[no-any-return]


def calendar() -> Calendar:
    return Calendar()


def user_id() -> str:
    return str(flask_session.get("user_id", ""))


def generate_csrf_token() -> str:
    key = "csrf_token"
    key_expiration = key + "_expiration"
    duration = get_settings().CSRF_DURATION * 60

    if token_has_expired(key_expiration):
        set_token(key, key_expiration, duration)
    return str(flask_session[key])


def token_has_expired(key_expiration: str) -> bool:
    expiration = int(flask_session.get(key_expiration, "0"))
    return expiration < int(time.time())


def set_token(key: str, key_expiration: str, duration: int) -> None:
    token = secrets.token_hex()
    flask_session[key] = token
    flask_session[key_expiration] = int(time.time()) + duration


def translator() -> l10n.Translator:
    return l10n.translator_for(
        request.accept_languages.best_match(l10n.LOCALES) or l10n.DEFAULT_LOCALE
    )


def context() -> dict[str, Any]:
    return {
        "version": version(PACKAGE_NAME),
        "current_url": request.url,
        "current_path": request.path,
        "current_args": request.args,
        "is_logged_in": "user_id" in flask_session,
        "url_for": url_for,
        "generate_csrf_token": generate_csrf_token,
        "_": translator(),
    }
