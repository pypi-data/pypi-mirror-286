# Gertrude --- GTD done right
# Copyright © 2020-2023 Tanguy Le Carrour <tanguy@bioneland.org>
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

from dataclasses import dataclass
from typing import Optional

import bl_seth


@dataclass(frozen=True)
class TotpSettings(bl_seth.Settings):
    SECRET: str
    """The secret key.
    It can be generated with `pyotp.random_base32()`.
    The CLI program `qrencode` can be used to generate a QR-Code to easily configure 2FA
    applications: `qrencode -t UTF8 "otpauth://totp/USER?secret=SECRET&issuer=ISSUER"`.
    """


@dataclass(frozen=True)
class MandatorySettings(bl_seth.Settings):
    DATA_DSN: str
    """The data source name to access the database that stores the important data.
    See: <https://docs.sqlalchemy.org/en/20/core/engines.html#database-urls>."""

    PROJECTION_DSN: str
    """The data source name to access the database that stores the projections.
    See: <https://docs.sqlalchemy.org/en/20/core/engines.html#database-urls>."""

    EVENT_STORE_URL: str
    """The URL to access the Scrypture event store."""


@dataclass(frozen=True)
class OptionalSettings(bl_seth.Settings):
    DEBUG: bool = False
    """To enable general debugging logging."""

    DEBUG_SQL: bool = False
    """To enable SqlAlchemy logging.
    See: <https://docs.sqlalchemy.org/en/20/core/engines.html#configuring-logging>."""


@dataclass(frozen=True)
class CliSettings(OptionalSettings, MandatorySettings):
    pass


@dataclass(frozen=True)
class WsgiMandatorySettings(MandatorySettings):
    SECRET_KEY: str
    """The secret key for Flask sessions.
    See: <https://flask.palletsprojects.com/en/2.3.x/quickstart/#sessions>."""


@dataclass(frozen=True)
class WsgiOptionalSettings(OptionalSettings):
    PROXIED: bool = False
    """To let Flask know that it runs behind a proxy.
    See: <https://flask.palletsprojects.com/en/2.3.x/deploying/proxy_fix/>."""

    AUTHORIZED_IP: str = ""
    """The trusted IP address for which the user is automatically authentified.
    A subnetwork can be authorized using a single `*`, for instance `192.168.0.*`."""

    TOTP: Optional[TotpSettings] = None
    """To configure time-based one-time password.
    Extra dependencies must be installed: `bl-hector[totp]`."""

    COOKIE_NAME: str = "session-gertrude"
    """The name of the session cookie.
    See: <https://flask.palletsprojects.com/en/2.3.x/config/#SESSION_COOKIE_NAME>."""

    CSRF_DURATION: int = 60
    """The duration of the CSRF token in minutes."""


@dataclass(frozen=True)
class WsgiSettings(WsgiOptionalSettings, WsgiMandatorySettings):
    pass
