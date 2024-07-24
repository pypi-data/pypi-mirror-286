# Gertrude --- GTD done right
# Copyright © 2023, 2024 Bioneland
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

from http import HTTPStatus as HTTP
from typing import Any, cast

import pyotp
from flask import Blueprint, request, session, url_for

from gertrude.infrastructure.flask import services
from gertrude.infrastructure.flask.utils import presenter_to_response
from gertrude.infrastructure.settings import TotpSettings
from gertrude.interfaces.to_http import Redirection, as_html

blueprint = Blueprint("totp", __name__)


@blueprint.get("/login")
@presenter_to_response
def login() -> Any:
    return as_html.HtmlPresenter.from_template("totp/login", **services.context())


@blueprint.post("/login")
@presenter_to_response
def login_POST() -> Any:
    # TOTP settings must be defined for this route to be accessible.
    # Other alternatives: 1) check presence with `if` or 2) ignore type.
    TOTP = cast(TotpSettings, services.get_settings().TOTP)

    totp = pyotp.TOTP(TOTP.SECRET)
    if not totp.verify(request.form.get("password", "")):
        return as_html.HtmlPresenter.from_template(
            "error",
            status=HTTP.UNAUTHORIZED,
            message=services.translator()("pages-auth-totp-error"),
            **services.context()
        )

    # TODO: find the actual user ID.
    session["user_id"] = "00000000-0000-0000-0000-000000000000"
    return Redirection(url_for("auth.redirect"))
