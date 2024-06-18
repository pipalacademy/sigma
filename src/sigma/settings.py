"""Configuration Settings for the system.
"""

import json
import textwrap
from dataclasses import dataclass
from pathlib import Path


@dataclass
class _Setting:
    name: str
    label: str
    description: str
    default_value: str


def get_all_settings():
    return _settings


def get_all() -> dict:
    """Returns values of all settings."""
    path = Path("_settings.json")
    values = get_default_values()

    if not path.exists():
        return values

    new_values = json.load(path.open())
    values.update(new_values)
    return values


def get_default_values():
    return {s.name: s.default_value for s in _settings}


def get(name: str) -> str:
    """Returns value of a setting specified the name."""
    values = get_all()
    return values[name]


def save(values):
    text = json.dumps(dict(values))
    path = Path("_settings.json")
    path.write_text(text)


_settings = []


def add_setting(name, label, description, default_value):
    description = textwrap.dedent(description)
    s = _Setting(name=name, label=label, description=description, default_value=default_value)
    _settings.append(s)


add_setting(
    "domain",
    label="Jupyerhub Domain",
    description="""
            The top-level domain of the jupyterhub server.
            """,
    default_value="lab.pipal.in",
)

add_setting(
    "jupyterhub_token",
    label="Jupyerhub Token",
    description="""
            The API token to interact with the jupyterhub.

            You can generate one by visiting /hub/token endpoint on the jupyterhub server.
            """,
    default_value="",
)

add_setting(
    "user_password",
    label="Password for Jupyterlab Users",
    description="""
            This password is used to set password for all new users created using jupyterhub.
            """,
    default_value="",
)
