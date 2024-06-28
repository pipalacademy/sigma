"""
sigma.assignments
~~~~~~~~~~~~~~~~~

Module for creating and grading assignments.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import nbformat as nbf
import yaml

from .problems import Problem

@dataclass
class Assignment:
    """Assignment is a set of problems.

    An assignment can be cea
    """
    path: Path
    title: str
    description: str
    problems: list[Problem]

    @staticmethod
    def from_file(path) -> Assignment:
        """Creates an assignment from an YAML file.

        The file should be of the following format.

        """
        path = Path(path)
        d = yaml.safe_load(path.open())
        title = d["title"]
        description = d.get("description", "")
        problems = [Problem.find(p) for p in d["problems"]]
        return Assignment(path=path, title=title, description=description, problems=problems)

    def to_notebook(self, path=None):
        """Writes the assignment as a notebook.
        """
        path = path or self.path.with_suffix(".ipynb")
        nb = self.render_notebook()
        nb.write(path)
        print("created", path)

    def render_notebook(self) -> Notebook:
        """Renders the assignment as a notebook.
        """
        nb = Notebook()

        nb.add_title(self.title)
        nb.add_markdown_cell(self.description)
        for i, p in enumerate(self.problems, start=1):
            self._add_problem(nb, i, p)
        return nb

    def _add_problem(self, nb, index, p):
        nb.add_markdown_cell(f"## Problem {index}: {p.title}")
        nb.add_markdown_cell(
            p.get_description()
            + "\n\n"
            + "You can verify your solution using:<br>\n"
            + f"`%verify_problem {p.name}`"
        )

        if p.problem_type == "script":
           code = f"%%file {p.script_name}\n# your code here"
        else:
            code = p.get_initial_code() or "# your code here\n\n\n\n"
        nb.add_code_cell(code)

        nb.add_code_cell("")
        nb.add_code_cell("")
        nb.add_code_cell(f"%verify_problem {p.name}")

class Notebook:
    def __init__(self):
        self.nb = nbf.v4.new_notebook()

    def add_title(self, title, level=1):
        prefix = "#" * level
        self.add_markdown_cell(f"{prefix} {title}")

    def add_markdown_cell(self, text):
        cell = nbf.v4.new_markdown_cell(text)
        self.nb["cells"].append(cell)

    def add_code_cell(self, code):
        cell = nbf.v4.new_code_cell(code)
        self.nb["cells"].append(cell)

    def write(self, path):
        nbf.write(self.nb, path)
