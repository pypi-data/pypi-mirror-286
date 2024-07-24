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

from gertrude.application.use_cases import schedule_task


class ScheduleTask:
    def __init__(self, user_id: str, task_id: str, params: dict[str, str]) -> None:
        # FIXME: format depends on the browser?!
        date_format = "%Y-%m-%d"
        # FIXME: what could be the best default date? UC should handle date in the past!
        date = datetime.date.today()
        try:
            date = datetime.datetime.strptime(params.get("date", ""), date_format).date()
        except ValueError:
            pass

        self.__request = schedule_task.Request(user_id, task_id, date)

    def call(self, interactor: schedule_task.Interactor) -> None:
        interactor.execute(self.__request)
