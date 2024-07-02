"""Sigma - CLI interface to Pipal Academy training setup.
"""

import click
from .assignments import Assignment, AssignmentSolution
from . import config

@click.group()
def app():
    """Sigma - CLI interface to Pipal Academy training setup."""


@app.command()
def list_users():
    """List the current users in the system."""
    print("Not yet implemented")

@app.command()
@click.argument("assignment_file")
@click.option("-o", "--output", "output_path", help="path to the output file (default: assignment file with .ipynb extension)")
def create_assignment(assignment_file, output_path=None):
    """Creates a new assignment."""
    a = Assignment.from_file(assignment_file)
    a.to_notebook(path=output_path)

@app.command()
@click.argument("assignment_name")
@click.option("--assignment-dir",
              help="Path to the directory where assignments are available relative to the home dir of each student",
              default=".")
def collect_assignment(assignment_name, assignment_dir):
    """Collect assignment of all students given the assignment name.

    Asssignment name is the name of the assignment notebook without the extension.

    Collected assignments will be stored at training-data/assignment-submissions/<assignment-name>/<username>/<assignment-name>.ipynb
    """
    assignment = Assignment.from_name(assignment_name)
    assignment.collect(assignment_dir=assignment_dir)

@app.command()
@click.argument("assignment_name")
def grade_assignment(assignment_name):
    assignment = Assignment.from_name(assignment_name)
    assignment.grade_all()

@app.command()
@click.argument("assignment_name")
@click.argument("notebook_path")
def grade_assignment_notebook(assignment_name, notebook_path):
    """Grades a single assignment notebook.

    This is meant for internal use only.
    """
    assignment = Assignment.from_name(assignment_name)
    assignment.grade_notebook(notebook_path)

if __name__ == "__main__":
    app()
