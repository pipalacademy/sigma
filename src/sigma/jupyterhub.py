"""Jupyterhub interactions.

Includes adding users to jupyter hub.
"""
from __future__ import annotations
from . import settings
from pathlib import Path
import requests
from dataclasses import dataclass

class JupyterHub:
    """Interface to jupyterhub.
    """
    def __init__(self):
        domain = settings.get("domain")
        self.base_url = f"https://{domain}/hub/api"
        self.api_token = settings.get("jupyterhub_token")

        self.headers = {
            "Authorization": f"Token {self.api_token}"
        }

    def _get(self, path, **kwargs):
        url = self.base_url + path
        response = requests.get(url, headers=self.headers, **kwargs)
        response.raise_for_status()
        return response

    def _post(self, path, **kwargs):
        url = self.base_url + path
        response = requests.post(url, headers=self.headers, **kwargs)
        response.raise_for_status()
        return response

    def add_users(self, usernames: list[str]):
        for name in usernames:
            self.create_user(name)

    def create_user(self, name, admin=False):
        print("creating user", name)
        # Add user
        self._post(f"/users/{name}")

        # Start the server. The user is added to the system only when the server is started for the first time.
        self._post(f"/users/{name}/server")

    def get_users(self) -> list[JupyterUser]:
        """Returns all the users in the system.
        """
        response_data = self._get("/users").json()
        users = [JupyterUser.from_response_dict(self, d) for d in response_data]
        return sorted(users, key=lambda u: u.name)

@dataclass
class JupyterUser:
    hub: JupyterHub
    name: str
    admin: bool

    @staticmethod
    def from_response_dict(hub: JupyterHub, d: dict) -> JupyterUser:
        name = d['name']
        admin = d['admin']
        return JupyterUser(hub=hub, name=name, admin=admin)
