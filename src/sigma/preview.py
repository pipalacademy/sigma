"""
Module to preview last few entries of a notebook for all students.


The goal of this module is to preview the a notebook by given name for all users in a single place.

Consider the following notebooks:

    /home/jupyter-alpha/session1.ipynb
    /home/jupyter-alpha/session2.ipynb
    /home/jupyter-alpha/session3.ipynb
    /home/jupyter-beta/session1.ipynb
    /home/jupyter-beta/session2.ipynb
    /home/jupyter-gamma/session2.ipynb
    /home/jupyter-gamma/session3.ipynb


There are 7 notebooks, but with 3 distinct names.

This module uses the following terminology.

Collection:
    A collection of notebooks with the same name, owned by multiple users.

    There are three collections in the above example:

    /home/jupyter-alpha/session1.ipynb
    /home/jupyter-beta/session1.ipynb

    /home/jupyter-alpha/session2.ipynb
    /home/jupyter-beta/session2.ipynb
    /home/jupyter-gamma/session2.ipynb

    /home/jupyter-beta/session3.ipynb
    /home/jupyter-gamma/session3.ipynb

Notebook:
    Represents one individual notebook file. It has the following fields:
    - name
    - owner
    - filename
    - path

"""

from __future__ import annotations

import itertools
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional
import json

from . import config

notebook_pattern = "/home/jupyter-*/*.ipynb"


class PreviewManager:
    def __init__(self, home_path=None):
        self.home_path = Path(home_path or config.home_path)

        print("PreviewManager", self.home_path)

        self._collections: dict[str, Collection] = self._scan()

    def get_collections(self) -> list[Collection]:
        return self._collections.values()

    def get_collection(self, name: str) -> Optional[Collection]:
        return self._collections.get(name)

    def _scan(self) -> dict[str, Collection]:
        """Scans the paths to update the collections."""
        path_pattern = "jupyter-*/*.ipynb"
        paths = self.home_path.glob(path_pattern)
        paths = sorted(paths, key=lambda p: p.stem)

        collections = [
            Collection.from_paths(name, paths_chunk) for name, paths_chunk in itertools.groupby(paths, key=lambda p: p.stem)
        ]
        return {c.name: c for c in collections}


@dataclass
class Collection:
    name: str
    notebooks: list[Notebook]

    @property
    def size(self):
        return len(self.notebooks)

    def get_notebook(self, owner):
        # TODO: improve this
        for nb in self.notebooks:
            if nb.owner == owner:
                return nb

    @staticmethod
    def from_paths(name, paths: list[Path]) -> Collection:
        print("from_paths", name, paths)
        return Collection(name, [Notebook.from_path(p) for p in paths])


@dataclass
class Notebook:
    name: str
    owner: str
    filename: str
    path: Path

    def tail(self, n=10):
        ipynb = json.load(self.path.open())
        cells = ipynb["cells"][-n:]
        return dict(ipynb, cells=cells)

    @staticmethod
    def from_path(path: Path) -> Notebook:
        name = path.stem
        owner = path.parent.name.replace("jupyter-", "")
        filename = path.name

        return Notebook(name=name, owner=owner, filename=filename, path=path)
