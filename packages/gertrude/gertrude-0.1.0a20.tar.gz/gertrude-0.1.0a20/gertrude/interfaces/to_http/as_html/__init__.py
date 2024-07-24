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

import datetime
import logging
from dataclasses import asdict
from http import HTTPStatus as HTTP
from pathlib import Path
from typing import Any, Optional

import bl3d
import markdown
from jinja2 import Environment, FileSystemLoader, select_autoescape
from jinja2_fragments import render_block

from gertrude.application.use_cases import (
    assign_task,
    capture_task,
    create_project,
    delegate_task,
    display_project,
    do_task,
    eliminate_task,
    file_task,
    incubate_task,
    list_next_tasks,
    list_projects,
    list_tasks,
    postpone_task,
    reclaim_task,
    schedule_task,
    update_task,
)
from gertrude.domain.project_management.entities import Project
from gertrude.domain.project_management.value_objects import Name, ProjectId, ShortName
from gertrude.domain.task_management import exceptions
from gertrude.domain.task_management.dto import Task
from gertrude.domain.task_management.entities import POSSIBLE_NEXT_STATES_OF_TASK
from gertrude.domain.task_management.enums import TaskStates
from gertrude.domain.task_management.value_objects import (
    Description,
    Person,
    TaskId,
    Title,
)
from gertrude.interfaces.l10n import Translator
from gertrude.interfaces.to_http import Headers, IsPresentable, MessageBody

ENVIRONMENT = Environment(
    loader=FileSystemLoader([Path(__file__).parent / "templates"]),
    autoescape=select_autoescape(),
    extensions=["pypugjs.ext.jinja.PyPugJSExtension"],
)
DATE_FORMAT = "%Y-%m-%d"


class PugBody(MessageBody):
    def __init__(self, template: str, context: dict[str, Any]) -> None:
        self.__template, self.__fragment = self.__template_parts(template)
        self.__context = {**context}

    def __template_parts(self, template: str) -> tuple[str, str]:
        fragment = ""
        if "#" in template:
            template, fragment = template.split("#", 2)
        return f"{template}.pug" if template else "", fragment

    def __getitem__(self, key: str) -> Any:
        return self.__context[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.__context[key] = value

    def __str__(self) -> str:
        if self.__fragment:
            return render_block(
                ENVIRONMENT, self.__template, self.__fragment, **self.__context
            )
        if self.__template:
            return ENVIRONMENT.get_template(self.__template).render(**self.__context)
        return ""

    def __repr__(self) -> str:
        return str(self.__context)

    def change_template(self, template: str) -> None:
        self.__template, self.__fragment = self.__template_parts(template)


class HtmlPresenter(IsPresentable):
    @classmethod
    def from_template(
        cls, template: str, /, *, status: int = HTTP.OK, **kwargs: Any
    ) -> "HtmlPresenter":
        return cls(
            Headers(status, {"Content-Type": "text/html"}), PugBody(template, kwargs)
        )

    def __init__(self, headers: Headers, body: PugBody) -> None:
        self.headers = headers
        self.body = body


class ListProjects(list_projects.Presenter, IsPresentable):
    TEMPLATE = "projects/list"

    def __init__(self, context: dict[str, Any]) -> None:
        self.headers = Headers(HTTP.OK, {"Content-Type": "text/html"})
        self.body = PugBody(self.TEMPLATE, context)
        self.body["projects"] = []

    def projects(self, projects: list[Project]) -> None:
        self.body["projects"] = sorted(projects, key=lambda p: str(p.name))


class ListProjectsList(ListProjects):
    TEMPLATE = "projects/list#list"


class CreateProjectForm(create_project.Presenter, IsPresentable):
    def __init__(
        self,
        translator: Translator,
        context: dict[str, Any],
        values: dict[str, Any],
    ) -> None:
        self._ = translator
        self.__context = context
        self.headers = Headers(HTTP.OK, {"Content-Type": "text/html"})
        self.body = PugBody("projects/creation_form", context)
        self.body["values"] = values or {"id": str(ProjectId.create())}
        self.body["errors"] = {}
        self.body["short_name_max"] = ShortName.MAX
        self.body["name_max"] = Name.MAX

    def missing_id(self) -> None:
        self.body["errors"]["id"] = self._("pages-projects-create-missing-id")

    def missing_name(self) -> None:
        self.body["errors"]["name"] = self._("pages-projects-create-missing-name")

    def missing_short_name(self) -> None:
        self.body["errors"]["short_name"] = self._(
            "pages-projects-create-missing-short-name"
        )

    def project_already_exists(self) -> None:
        self.body["errors"]["name"] = self._(
            "pages-projects-create-project-already-exists"
        )

    def project_created(self) -> None:
        self.headers.set("HX-Trigger", "ProjectCreated")
        self.body.change_template("empty")


class DisplayProject(display_project.Presenter, IsPresentable):
    TEMPLATE = "projects/display"

    def __init__(self, translator: Translator, context: dict[str, Any]) -> None:
        self._ = translator
        self.headers = Headers(HTTP.OK, {"Content-Type": "text/html"})
        self.body = PugBody(self.TEMPLATE, context)
        self.body["project"] = {}
        self.body["tasks"] = []
        self.body["actionable_tasks"] = []
        self.body["incubated_tasks"] = []
        self.body["done_tasks"] = []

    def project_not_found(self, id: str) -> None:
        # TODO: redirect to list of project… + message ?
        logging.error(self._("pages-projects-display-project-not-found"))

    def project(self, project: Project) -> None:
        self.body["project"] = project

    def task(self, task: Task) -> None:
        if task.state == TaskStates.ACTIONABLE.value:
            self.body["tasks"].append(task)
            self.body["actionable_tasks"].append(task)
        elif task.state == TaskStates.INCUBATED.value:
            self.body["tasks"].append(task)
            self.body["incubated_tasks"].append(task)
        elif task.state == TaskStates.DONE.value:
            self.body["done_tasks"].append(task)


class DisplayProjectTasks(DisplayProject):
    TEMPLATE = "projects/display#tasks"


class ListTasks(list_tasks.Presenter, IsPresentable):
    TEMPLATE = "tasks/list"

    def __init__(
        self,
        translator: Translator,
        context: dict[str, Any],
        projects: list[Project],
        filters: dict[str, str],
    ) -> None:
        self._ = translator
        self.__filters = filters
        self.headers = Headers(HTTP.OK, {"Content-Type": "text/html"})
        self.body = PugBody(self.TEMPLATE, context)
        self.body["projects_by_id"] = {str(p.id): p for p in projects}
        self.body["tasks"] = []
        self.body["title"] = self.__title_for_state(self.__filters.get("state", ""))
        self.body["message"] = self.__message_when_empty(self.__filters.get("state", ""))

    def __title_for_state(self, state: str) -> str:
        if state:
            return f"pages-tasks-list-{state}-title"
        return "pages-tasks-list-title"

    def __message_when_empty(self, state: str) -> str:
        if state:
            return f"pages-tasks-list-{state}-empty-html"
        return "pages-tasks-list-empty-html"

    def unknown_state(self, name: str) -> None:
        # FIXME: handle unknown states!
        raise NotImplementedError()

    def tasks(self, tasks: list[Task]) -> None:
        self.body["tasks"].extend([format_task(t) for t in tasks])


class ListTasksList(ListTasks):
    TEMPLATE = "tasks/list#list"


class ListNextTasks(ListTasks, list_next_tasks.Presenter):
    def __init__(
        self, translator: Translator, context: dict[str, Any], projects: list[Project]
    ) -> None:
        super().__init__(translator, context, projects, {})
        self.body["title"] = "pages-tasks-list-actionable-title"
        self.body["message"] = "pages-tasks-list-actionable-empty-html"


class ListNextTasksList(ListNextTasks):
    TEMPLATE = "tasks/list#list"


class CaptureTaskForm(capture_task.Presenter, IsPresentable):
    def __init__(
        self,
        translator: Translator,
        context: dict[str, Any],
        projects: list[Project],
        data: dict[str, Any],
    ) -> None:
        self._ = translator
        self.__context = context
        self.__data = data
        self.headers = Headers(HTTP.OK, {"Content-Type": "text/html"})
        self.body = PugBody("tasks/capture_form", context)
        self.body["values"] = data or {"id": str(TaskId.create())}
        self.body["errors"] = {}
        self.body["max"] = {"title": Title.MAX, "description": Description.MAX}
        self.body["projects"] = sorted(projects, key=lambda p: str(p.name))

    def validation_error(self, attribute: str, exception: Exception) -> None:
        self.body["errors"][attribute] = translate_exception(exception, self._)

    def task_id_already_used(self) -> None:
        self.body["errors"]["task_id"] = self._(
            "pages-tasks-capture-task-id-already-used"
        )

    def task_captured(self) -> None:
        self.headers.set("HX-Trigger", "TaskCaptured")
        self.body.change_template("empty")


class UpdateTaskForm(update_task.Presenter, IsPresentable):
    def __init__(
        self,
        translator: Translator,
        context: dict[str, Any],
        values: dict[str, Any],
    ) -> None:
        self._ = translator
        self.__context = context
        self.headers = Headers(HTTP.OK, {"Content-Type": "text/html"})
        self.body = PugBody("tasks/update_form", context)
        self.body["values"] = values
        self.body["errors"] = {}
        self.body["max"] = {"title": Title.MAX, "description": Description.MAX}

    def validation_error(self, attribute: str, exception: Exception) -> None:
        self.body["errors"][attribute] = translate_exception(exception, self._)

    def task_not_found(self) -> None:
        self.headers = Headers(HTTP.NOT_FOUND, {"Content-Type": "text/html"})
        self.body = PugBody("empty", {})

    def task_updated(self) -> None:
        self.headers.set("HX-Trigger", "TaskUpdated")
        self.body.change_template("tasks/display#details")
        self.body["task"] = self.body["values"]
        self.body["task"]["description"] = format_task_description(
            self.body["task"].get("description", "")
        )


class DisplayTask(IsPresentable):
    TEMPLATE = "tasks/display"

    def __init__(
        self,
        translator: Translator,
        context: dict[str, Any],
        projects: list[Project],
        task: Optional[Task] = None,
    ) -> None:
        self._ = translator
        if task:
            self.headers = Headers(HTTP.OK, {"Content-Type": "text/html"})
            self.body = PugBody(self.TEMPLATE, context)
            self.body["projects"] = format_projects(projects)
            self.body["project"] = format_project(find_project(projects, task))
            self.body["task"] = format_task(task) if task else {}
            self.body["next_states"] = next_states(task.state)
        else:
            self.headers = Headers(HTTP.NOT_FOUND, {"Content-Type": "text/html"})
            self.body = PugBody("empty", {})


class DisplayTaskDetails(DisplayTask):
    TEMPLATE = "tasks/display#details"


class DisplayTaskActions(DisplayTask):
    TEMPLATE = "tasks/display#actions"


class ActionMixin(DisplayTask):
    TEMPLATE = "tasks/display#actions"

    def __init__(
        self,
        translator: Translator,
        context: dict[str, Any],
        projects: list[Project],
        task: Optional[Task] = None,
        values: Optional[dict[str, str]] = None,
    ) -> None:
        self._ = translator

        if not task:
            self.headers = Headers(HTTP.NOT_FOUND, {"Content-Type": "text/html"})
            self.body = PugBody("empty", context)
        else:
            self.headers = Headers(HTTP.OK, {"Content-Type": "text/html"})
            self.body = PugBody(self.TEMPLATE, context)
            self.body["projects"] = format_projects(projects)
            self.body["project"] = format_project(find_project(projects, task))
            self.body["task"] = format_task(task)
            self.body["next_states"] = next_states(task.state)
            self.body["values"] = values or {}

        self.body["errors"] = {}

    def validation_error(self, attribute: str, exception: Exception) -> None:
        self.body["errors"][attribute] = translate_exception(exception, self._)

    def task_not_found(self) -> None:
        self.body["errors"]["task_id"] = self._("pages-tasks-errors-task-not-found")

    def transition_not_allowed(self, current: TaskStates, next: TaskStates) -> None:
        self.body["errors"]["task_id"] = self._(
            "pages-tasks-errors-transition-not-allowed"
        )

    def update_state(self, state: TaskStates) -> None:
        # To prevent matching `task.state == "captured"`
        self.body["task"]["state"] = state.value
        self.body["next_states"] = next_states(state.value)


class DoTask(ActionMixin, do_task.Presenter):
    def task_done(self) -> None:
        self.update_state(TaskStates.DONE)


class EliminateTask(ActionMixin, eliminate_task.Presenter):
    def task_eliminated(self) -> None:
        self.update_state(TaskStates.ELIMINATED)


class FileTask(ActionMixin, file_task.Presenter):
    def task_filed(self) -> None:
        self.update_state(TaskStates.FILED)


class IncubateTask(ActionMixin, incubate_task.Presenter):
    def task_incubated(self) -> None:
        self.update_state(TaskStates.INCUBATED)


class PostponeTask(ActionMixin, postpone_task.Presenter):
    def task_postponed(self) -> None:
        self.update_state(TaskStates.ACTIONABLE)


class ReclaimTask(ActionMixin, reclaim_task.Presenter):
    def task_reclaimed(self) -> None:
        self.update_state(TaskStates.ACTIONABLE)
        self.body["task"]["delegated_to"] = ""


class AssignTaskForm(ActionMixin, assign_task.Presenter):
    TEMPLATE = "tasks/assign_form"

    def __init__(
        self,
        translator: Translator,
        context: dict[str, Any],
        projects: list[Project],
        task: Optional[Task] = None,
        values: Optional[dict[str, str]] = None,
    ) -> None:
        values = values or {}
        if task and "project_id" not in values:
            values["project_id"] = task.assigned_to

        super().__init__(translator, context, projects, task, values)

    def project_not_found(self) -> None:
        self.body["errors"]["project_id"] = self._(
            "pages-tasks-assign-incorrect-project-id"
        )

    def task_assigned(self) -> None:
        # FIXME: Assigned is not a state so we don’t need to `update_state`,
        # but… if it’s the first task of a project it becomes actionable
        # and becomes incubated if not!!
        self.body.change_template("tasks/display#actions")
        # Update value so we don’t have to query the new value.
        projects = (
            p
            for p in self.body["projects"]
            if p["id"] == self.body["values"]["project_id"]
        )
        self.body["project"] = next(projects, {})


class DelegateTaskForm(ActionMixin, delegate_task.Presenter):
    TEMPLATE = "tasks/delegate_form"

    def __init__(
        self,
        translator: Translator,
        context: dict[str, Any],
        projects: list[Project],
        task: Optional[Task] = None,
        values: Optional[dict[str, str]] = None,
    ) -> None:
        values = values or {}
        if task and "person" not in values:
            values["person"] = task.delegated_to

        super().__init__(translator, context, projects, task, values)
        self.body["max"] = {"person": Person.MAX}

    def task_delegated(self) -> None:
        self.update_state(TaskStates.DELEGATED)
        self.body.change_template("tasks/display#actions")
        self.body["task"]["delegated_to"] = self.body["values"]["person"]


class ScheduleTaskForm(ActionMixin, schedule_task.Presenter):
    TEMPLATE = "tasks/schedule_form"

    def __init__(
        self,
        translator: Translator,
        context: dict[str, Any],
        projects: list[Project],
        task: Optional[Task] = None,
        values: Optional[dict[str, str]] = None,
    ) -> None:
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        next_week = datetime.date.today() + datetime.timedelta(days=7)
        next_month = datetime.date.today() + datetime.timedelta(days=7 * 4)
        values = values or {}
        if "date" not in values:
            date = task.scheduled_on if task and task.scheduled_on else tomorrow
            values["date"] = date.strftime(DATE_FORMAT)

        super().__init__(translator, context, projects, task, values)

        self.body["min_date"] = tomorrow.strftime(DATE_FORMAT)
        self.body["next_week"] = next_week.strftime(DATE_FORMAT)
        self.body["next_month"] = next_month.strftime(DATE_FORMAT)

    def task_scheduled(self) -> None:
        self.update_state(TaskStates.SCHEDULED)
        self.body.change_template("tasks/display#actions")
        self.body["task"]["scheduled_on"] = self.body["values"]["date"]


def next_states(state: str) -> list[str]:
    try:
        if current_state := TaskStates(state):
            return [s.name for s in POSSIBLE_NEXT_STATES_OF_TASK[current_state]]
    except ValueError as exc:
        logging.exception(exc)
    return []


def find_project(projects: list[Project], task: Task) -> Optional[Project]:
    return next((p for p in projects if str(p.id) == task.assigned_to), None)


def format_projects(projects: list[Project]) -> list[dict[str, Any]]:
    return [format_project(p) for p in projects]


def format_project(project: Optional[Project]) -> dict[str, Any]:
    if project:
        return {
            "id": str(project.id),
            "name": str(project.name),
            "short_name": str(project.short_name),
        }
    return {}


def format_task(task: Task) -> dict[str, Any]:
    today = datetime.date.today()
    data = asdict(task)

    if task.scheduled_on:
        data["scheduled_on"] = task.scheduled_on.strftime(DATE_FORMAT)
        if task.scheduled_on < today:
            data["is_due"] = True

    data["description"] = format_task_description(task.description or "")

    return data


def format_task_description(text: str) -> str:
    # INFO: allows for script injection! … but Gertrude is single-user!
    return markdown.markdown(text)


# TODO: use me to translate execptions!
def translate_exception(exception: Exception, translator: Translator) -> str:
    if isinstance(exception, exceptions.MissingValue):
        return translator("exceptions-missing-value")
    if isinstance(exception, exceptions.TransitionNotAllowed):
        return translator(
            "exceptions-transition-not-allowed",
            current=exception.current.value,
            next=exception.next.value,
        )
    if isinstance(exception, exceptions.DateInThePast):
        return translator(
            "exceptions-date-in-the-past",
            current=exception.current,
            target=exception.target,
        )
    if isinstance(exception, bl3d.StringTooShort):
        return translator("exceptions-string-too-short", min=exception.MIN)
    if isinstance(exception, bl3d.StringTooLong):
        return translator("exceptions-string-too-long", max=exception.MAX)

    logging.debug(f"Unhandled exception cannot be translated! [{type(exception)}]")
    return translator("exceptions-unknown-exception", name=exception.__class__.__name__)
