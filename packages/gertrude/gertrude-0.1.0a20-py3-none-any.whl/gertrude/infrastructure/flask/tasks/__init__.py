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

from dataclasses import asdict
from typing import Any

from flask import Blueprint, request

from gertrude.application.use_cases import (
    assign_task,
    capture_task,
    delegate_task,
    do_task,
    eliminate_task,
    file_task,
    incubate_task,
    list_next_tasks,
    list_tasks,
    postpone_task,
    reclaim_task,
    schedule_task,
    update_task,
)
from gertrude.infrastructure.flask import services
from gertrude.infrastructure.flask.utils import auth_required, presenter_to_response
from gertrude.interfaces import from_base_types as controllers
from gertrude.interfaces.to_http import as_html

blueprint = Blueprint("tasks", __name__)


@blueprint.get("")
@presenter_to_response
@auth_required
def index() -> Any:
    filters = request.args
    presenter = as_html.ListTasks(
        services.translator(), services.context(), services.projects().all(), filters
    )
    interactor = list_tasks.Interactor(presenter, services.task_projection())
    interactor.execute(list_tasks.Request(services.user_id(), filters.get("state", "")))
    return presenter


@blueprint.get("/__list__")
@presenter_to_response
@auth_required
def index_list() -> Any:
    filters = request.args
    presenter = as_html.ListTasksList(
        services.translator(), services.context(), services.projects().all(), filters
    )
    interactor = list_tasks.Interactor(presenter, services.task_projection())
    interactor.execute(list_tasks.Request(services.user_id(), filters.get("state", "")))
    return presenter


@blueprint.get("/next")
@presenter_to_response
@auth_required
def next() -> Any:
    presenter = as_html.ListNextTasks(
        services.translator(), services.context(), services.projects().all()
    )
    interactor = list_next_tasks.Interactor(
        presenter, services.task_projection(), services.calendar()
    )
    interactor.execute(list_next_tasks.Request(services.user_id()))
    return presenter


@blueprint.get("/next/__list__")
@presenter_to_response
@auth_required
def next_list() -> Any:
    presenter = as_html.ListNextTasksList(
        services.translator(), services.context(), services.projects().all()
    )
    interactor = list_next_tasks.Interactor(
        presenter, services.task_projection(), services.calendar()
    )
    interactor.execute(list_next_tasks.Request(services.user_id()))
    return presenter


@blueprint.get("/__new__")
@presenter_to_response
@auth_required
def capture_form() -> Any:
    return as_html.CaptureTaskForm(
        services.translator(),
        services.context(),
        services.projects().all(),
        {},
    )


@blueprint.post("/__new__")
@presenter_to_response
@auth_required
def capture() -> Any:
    presenter = as_html.CaptureTaskForm(
        services.translator(),
        services.context(),
        services.projects().all(),
        request.form.to_dict(),
    )
    interactor = capture_task.Interactor(
        presenter, services.history(), services.tasks(), services.users()
    )
    interactor.execute(
        capture_task.Request(
            services.user_id(),
            request.form.get("id", ""),
            request.form.get("title", ""),
            request.form.get("description", ""),
            request.form.get("project_id", ""),
        )
    )
    return presenter


@blueprint.get("/<id>")
@presenter_to_response
@auth_required
def display(id: str) -> Any:
    return as_html.DisplayTask(
        services.translator(),
        services.context(),
        services.projects().all(),
        services.task_projection().load(id),
    )


@blueprint.get("/<id>/__details__")
@presenter_to_response
@auth_required
def display_details(id: str) -> Any:
    return as_html.DisplayTaskDetails(
        services.translator(),
        services.context(),
        services.projects().all(),
        services.task_projection().load(id),
    )


@blueprint.get("/<id>/__actions__")
@presenter_to_response
@auth_required
def display_actions(id: str) -> Any:
    return as_html.DisplayTaskActions(
        services.translator(),
        services.context(),
        services.projects().all(),
        services.task_projection().load(id),
    )


@blueprint.get("<id>/__update__")
@presenter_to_response
@auth_required
def update_form(id: str) -> Any:
    if task := services.task_projection().load(id):
        # INFO: Not tested as it would require a populated DB.
        return as_html.UpdateTaskForm(
            services.translator(),
            services.context(),
            asdict(task),
        )
    return as_html.HtmlPresenter.from_template(
        "error", status=404, message="Task not found!", **services.context()
    )


@blueprint.post("<id>/__update__")
@presenter_to_response
@auth_required
def update(id: str) -> Any:
    presenter = as_html.UpdateTaskForm(
        services.translator(), services.context(), {**request.form, "id": id}
    )
    interactor = update_task.Interactor(presenter, services.history(), services.tasks())
    interactor.execute(
        update_task.Request(
            services.user_id(),
            id,
            request.form.get("title", ""),
            request.form.get("description", ""),
        )
    )
    return presenter


@blueprint.get("/<id>/__assign__")
@presenter_to_response
@auth_required
def assign_form(id: str) -> Any:
    return as_html.AssignTaskForm(
        services.translator(),
        services.context(),
        services.projects().all(),
        services.task_projection().load(id),
    )


@blueprint.post("/<id>/__assign__")
@presenter_to_response
@auth_required
def assign(id: str) -> Any:
    presenter = as_html.AssignTaskForm(
        services.translator(),
        services.context(),
        services.projects().all(),
        services.task_projection().load(id),
        request.form,
    )
    interactor = assign_task.Interactor(
        presenter, services.history(), services.tasks(), services.projects()
    )
    interactor.execute(
        assign_task.Request(services.user_id(), id, request.form.get("project_id", ""))
    )
    return presenter


@blueprint.get("/<id>/__delegate__")
@presenter_to_response
@auth_required
def delegate_form(id: str) -> Any:
    return as_html.DelegateTaskForm(
        services.translator(),
        services.context(),
        services.projects().all(),
        services.task_projection().load(id),
    )


@blueprint.post("/<id>/__delegate__")
@presenter_to_response
@auth_required
def delegate(id: str) -> Any:
    presenter = as_html.DelegateTaskForm(
        services.translator(),
        services.context(),
        services.projects().all(),
        services.task_projection().load(id),
        request.form,
    )
    interactor = delegate_task.Interactor(
        presenter, services.history(), services.tasks()
    )
    interactor.execute(
        delegate_task.Request(services.user_id(), id, request.form.get("person", ""))
    )
    return presenter


@blueprint.post("/<id>/__do__")
@presenter_to_response
@auth_required
def do(id: str) -> Any:
    presenter = as_html.DoTask(
        services.translator(),
        services.context(),
        services.projects().all(),
        services.task_projection().load(id),
    )
    interactor = do_task.Interactor(presenter, services.history(), services.tasks())
    interactor.execute(do_task.Request(services.user_id(), id))
    return presenter


@blueprint.post("/<id>/__eliminate__")
@presenter_to_response
@auth_required
def eliminate(id: str) -> Any:
    presenter = as_html.EliminateTask(
        services.translator(),
        services.context(),
        services.projects().all(),
        services.task_projection().load(id),
    )
    interactor = eliminate_task.Interactor(
        presenter, services.history(), services.tasks()
    )
    interactor.execute(eliminate_task.Request(services.user_id(), id))
    return presenter


@blueprint.post("/<id>/__file__")
@presenter_to_response
@auth_required
def file(id: str) -> Any:
    presenter = as_html.FileTask(
        services.translator(),
        services.context(),
        services.projects().all(),
        services.task_projection().load(id),
    )
    interactor = file_task.Interactor(presenter, services.history(), services.tasks())
    interactor.execute(file_task.Request(services.user_id(), id))
    return presenter


@blueprint.post("/<id>/__incubate__")
@presenter_to_response
@auth_required
def incubate(id: str) -> Any:
    presenter = as_html.IncubateTask(
        services.translator(),
        services.context(),
        services.projects().all(),
        services.task_projection().load(id),
    )
    interactor = incubate_task.Interactor(
        presenter, services.history(), services.tasks()
    )
    interactor.execute(incubate_task.Request(services.user_id(), id))
    return presenter


@blueprint.post("/<id>/__postpone__")
@presenter_to_response
@auth_required
def postpone(id: str) -> Any:
    presenter = as_html.PostponeTask(
        services.translator(),
        services.context(),
        services.projects().all(),
        services.task_projection().load(id),
    )
    interactor = postpone_task.Interactor(
        presenter, services.history(), services.tasks()
    )
    interactor.execute(postpone_task.Request(services.user_id(), id))
    return presenter


@blueprint.post("/<id>/__reclaim__")
@presenter_to_response
@auth_required
def reclaim(id: str) -> Any:
    presenter = as_html.ReclaimTask(
        services.translator(),
        services.context(),
        services.projects().all(),
        services.task_projection().load(id),
    )
    interactor = reclaim_task.Interactor(presenter, services.history(), services.tasks())
    interactor.execute(reclaim_task.Request(services.user_id(), id))
    return presenter


@blueprint.get("/<id>/__schedule__")
@presenter_to_response
@auth_required
def schedule_form(id: str) -> Any:
    return as_html.ScheduleTaskForm(
        services.translator(),
        services.context(),
        services.projects().all(),
        services.task_projection().load(id),
    )


@blueprint.post("/<id>/__schedule__")
@presenter_to_response
@auth_required
def schedule(id: str) -> Any:
    presenter = as_html.ScheduleTaskForm(
        services.translator(),
        services.context(),
        services.projects().all(),
        services.task_projection().load(id),
        request.form,
    )

    interactor = schedule_task.Interactor(
        presenter, services.history(), services.tasks(), services.calendar()
    )

    controller = controllers.ScheduleTask(services.user_id(), id, request.form)
    controller.call(interactor)
    return presenter
