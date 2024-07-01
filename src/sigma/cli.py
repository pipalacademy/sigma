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
@click.option("--data-dir", help="Path to the directory where the training data is stored (default: training-data)")
def collect_assignment(assignment_name, assignment_dir, data_dir):
    """Collect assignment of all students given the assignment name.

    Asssignment name is the name of the assignment notebook without the extension.

    Collected assignments will be stored at training-data/assignment-submissions/<assignment-name>/<username>/<assignment-name>.ipynb
    """
    data_dir = data_dir or config.training_data_dir
    solutions = AssignmentSolution.find_all(assignment_name, assignment_dir=assignment_dir)
    for s in solutions:
        s.submit(data_dir=data_dir)

if __name__ == "__main__":
    app()
