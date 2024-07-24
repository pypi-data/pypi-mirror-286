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

from typing import Any

from flask import Blueprint

from gertrude.infrastructure.flask import services
from gertrude.infrastructure.flask.utils import presenter_to_response
from gertrude.interfaces.to_http import as_html

blueprint = Blueprint("root", __name__)


@blueprint.get("")
@presenter_to_response
def index() -> Any:
    return as_html.HtmlPresenter.from_template("root/index", **services.context())
