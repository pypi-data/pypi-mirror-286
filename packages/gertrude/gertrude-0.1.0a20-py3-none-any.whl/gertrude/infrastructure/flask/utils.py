# Gertrude --- GTD done right
# Copyright © 2022-2024 Tanguy Le Carrour <tanguy@bioneland.org>
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

from functools import wraps
from http import HTTPStatus as HTTP
from typing import Any, Callable

from flask import Response

from gertrude.interfaces.to_http import IsPresentable, as_html

from . import services


def presenter_to_response(f: Callable[..., IsPresentable]) -> Callable[[], Response]:
    @wraps(f)
    def decorated_function(*args: Any, **kwargs: Any) -> Response:
        presenter = f(*args, **kwargs)
        return Response(
            status=presenter.headers.status_code,
            headers=presenter.headers.values,
            response=str(presenter.body),
        )

    return decorated_function


def auth_required(f: Callable[..., IsPresentable]) -> Callable[[], IsPresentable]:
    @wraps(f)
    def decorator(*args: Any, **kwargs: Any) -> IsPresentable:
        if not services.user_id():
            return as_html.HtmlPresenter.from_template(
                "error",
                status=HTTP.UNAUTHORIZED,
                message=services.translator()("pages-error-unauthorized"),
                **services.context()
            )
        return f(*args, **kwargs)

    return decorator
