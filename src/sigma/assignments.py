"""
sigma.assignments
~~~~~~~~~~~~~~~~~

Module for creating and grading assignments.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import shutil
import tempfile

import nbformat as nbf
from nbconvert.preprocessors import ExecutePreprocessor
import yaml

from .problems import Problem
from . import config

@dataclass
class Assignment:
    """Assignment is a set of problems.

    An assignment can be cea
    """
    name: str
    path: Path
    title: str
    description: str
    problems: list[Problem]

    @classmethod
    def from_name(cls, name) -> Assignment:
        """Creates an assignment from its name.

        It expects that the YAML file for that assignment exists in the current directory.
        The name of the YAML file is expected to be {name}.yml
        """
        path = Path(config.training_data_dir) / "assignments" / (name + ".yml")
        return cls.from_file(path)

    @staticmethod
    def from_file(path) -> Assignment:
        """Creates an assignment from an YAML file.

        The file should be of the following format.

        """
        path = Path(path)
        d = yaml.safe_load(path.open())
        name = path.stem
        title = d["title"]
        description = d.get("description", "")
        problems = [Problem.find(p) for p in d["problems"]]
        return Assignment(name=name, path=path, title=title, description=description, problems=problems)

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

    def collect(self, assignment_dir="."):
        """Collect the solutions of all users for this assignment and submit them.
        """
        pattern = f"jupyter-*/{assignment_dir}/{self.name}.ipynb"
        paths = Path(config.home_path).glob(pattern)
        paths = list(paths)
        for path in sorted(paths):
            solution = AssignmentSolution.from_path(self.name, path)
            solution.submit()

    def grade_all(self):
        """Grade all the submissions of this assignment.
        """
        submissions = AssignmentSubmission.load_all(assignment=self)
        for s in submissions:
            s.grade()

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

@dataclass
class AssignmentSolution:
    assignment_name: str
    username: str
    notebook_path: Path

    def submit(self):
        """Submit the assignment solution.

        On submit, the assignment solution will be copied to:
        {training_data_dir}/assignment-submissions/{assignment_name}/{username}/{assignment_name}.ipynb
        """
        filename = self.assignment_name + ".ipynb"
        submit_path = Path(config.training_data_dir) / "assignment-submissions" / self.assignment_name / self.username / filename
        submit_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(self.notebook_path, submit_path)
        print(f"Submitted {self.notebook_path} to {submit_path}")

    @classmethod
    def find_all(cls, assignment_name, assignment_dir=".") -> list[AssignmentSolution]:
        """Finds solutions for given assignment from all users.

        It is expected that the solution notebook will be at {assignment_dir}/{assignment_name}.ipynb
        in the home directory of every user.
        """
        pattern = f"jupyter-*/{assignment_dir}/{assignment_name}.ipynb"
        paths = Path(config.home_path).glob(pattern)
        paths = list(paths)
        return [cls.from_path(assignment_name, path) for path in sorted(paths)]

    @classmethod
    def from_path(cls, assignment_name, notebook_path) -> AssignmentSolution:
        notebook_path = Path(notebook_path)
        username = cls.find_username(notebook_path)
        return cls(assignment_name=assignment_name, username=username, notebook_path=notebook_path)

    @staticmethod
    def find_username(path):
        """Finds the username from the path.

            >>> AssignmentSolution.find_username("/home/jupyter-alice/assignments/assignment-01.ipynb")
            'alice'
        """
        path = Path(path)
        p = path.absolute().relative_to(config.home_path)
        # parents[-1] is "." and
        username = p.parents[-2].name
        return username.replace("jupyter-", "")

@dataclass
class AssignmentSubmission:
    """AssignmentSubmission class provide functionality to manage the solution of a user after it has been submitted.
    """
    assignment: Assignment
    username: username
    submission_dir: Path

    @staticmethod
    def load(assignment, username):
        submission_dir = Path(config.training_data_dir) / "assignment-submissions" / assignment.name / username
        if not submission_dir.exists():
            return None
        return AssignmentSubmission(assignment=assignment, username=username, submission_dir=submission_dir)

    @staticmethod
    def load_all(assignment):
        root = Path(config.training_data_dir) / "assignment-submissions" / assignment.name
        usernames = [f.name for f in root.iterdir() if f.is_dir()]
        return [AssignmentSubmission.load(assignment=assignment, username=username) for username in usernames]

    def get_notebook_path(self) -> Path:
        filename = self.assignment.name + ".ipynb"
        return self.submission_dir / filename

    def grade(self):
        """Grade the assignment submission.
        """
        path = self.get_notebook_path()
        grader = AssignmentGrader(self.assignment, path)
        grader.grade()

class AssignmentGrader:
    def __init__(self, assignment: Assignment, notebook_path: Path):
        self.assignment = assignment
        self.notebook_path = notebook_path
        self.grade_path = notebook_path.parent / "grades.json"

    def grade(self):
        nb = nbf.read(self.notebook_path.open(), as_version=4)
        self.add_verify_cells(nb)
        self.execute(nb)

    def add_verify_cells(self, nb):
        """Add %verify_problem cells at the end for every problem.
        """
        def add_code_cell(code):
            cell = nbf.v4.new_code_cell(code)
            nb['cells'].append(cell)

        def add_verify_cell(problem):
            code = f"%verify_problem {problem.name}"
            add_code_cell(code)

        add_code_cell("import sigma.magic")
        add_code_cell("sigma.magic.register()")

        add_code_cell("import sigma.problems")
        add_code_cell("sigma.problems.reset_grades()")
        for p in self.assignment.problems:
            add_verify_cell(p)

        add_code_cell(f"_grade_path = '{self.grade_path}'")
        add_code_cell("sigma.problems.save_grades(_grade_path)")

    def execute(self, nb):
        """Executes the notebook.
        """
        p = ExecutePreprocessor(timeout=600, kernel_name='python3', allow_errors=True)
        with tempfile.TemporaryDirectory() as tmp:
            nb, _ = p.preprocess(nb, {'metadata': {'path': tmp}})

        path = self.notebook_path.parent / "graded.ipynb"
        nbf.write(nb, path)
        print("saved the graded notebook to", path)

        print("saved the grades to", self.grade_path)
