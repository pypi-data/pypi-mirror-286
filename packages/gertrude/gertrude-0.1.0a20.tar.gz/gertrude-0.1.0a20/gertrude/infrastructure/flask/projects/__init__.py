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

from typing import Any

from flask import Blueprint, request

from gertrude.application.use_cases import (
    create_project,
    display_project,
    list_projects,
)
from gertrude.infrastructure.flask import services
from gertrude.infrastructure.flask.utils import auth_required, presenter_to_response
from gertrude.interfaces.to_http import as_html

blueprint = Blueprint("projects", __name__)


@blueprint.get("")
@presenter_to_response
@auth_required
def index() -> Any:
    presenter = as_html.ListProjects(services.context())
    interactor = list_projects.Interactor(presenter, services.projects())
    interactor.execute()
    return presenter


@blueprint.get("/__list__")
@presenter_to_response
@auth_required
def index_list() -> Any:
    presenter = as_html.ListProjectsList(services.context())
    interactor = list_projects.Interactor(presenter, services.projects())
    interactor.execute()
    return presenter


@blueprint.get("/__new__")
@presenter_to_response
@auth_required
def create_form() -> Any:
    return as_html.CreateProjectForm(services.translator(), services.context(), {})


@blueprint.post("/__new__")
@presenter_to_response
@auth_required
def create() -> Any:
    presenter = as_html.CreateProjectForm(
        services.translator(), services.context(), request.form.to_dict()
    )
    interactor = create_project.Interactor(presenter, services.projects())
    interactor.execute(
        create_project.Request(
            request.form.get("id", ""),
            request.form.get("name", ""),
            request.form.get("short_name", ""),
        )
    )
    return presenter


@blueprint.get("/<id>")
@presenter_to_response
@auth_required
def display(id: str) -> Any:
    presenter = as_html.DisplayProject(services.translator(), services.context())
    interactor = display_project.Interactor(
        presenter, services.projects(), services.task_projection()
    )
    interactor.execute(display_project.Request(id))
    return presenter


@blueprint.get("/<id>/__tasks__")
@presenter_to_response
@auth_required
def display_tasks(id: str) -> Any:
    presenter = as_html.DisplayProjectTasks(services.translator(), services.context())
    interactor = display_project.Interactor(
        presenter, services.projects(), services.task_projection()
    )
    interactor.execute(display_project.Request(id))
    return presenter
