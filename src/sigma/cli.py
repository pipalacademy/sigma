"""Sigma - CLI interface to Pipal Academy training setup.
"""

import click
from .assignments import Assignment

@click.group()
def app():
    """Sigma - CLI interface to Pipal Academy training setup."""


@app.command()
def list_users():
    """List the current users in the system."""
    print("Not yet implemented")

@app.command()
@click.argument("assignment_file")
@click.option("-o", "--output", help="path to the output file (default: assignment file with .ipynb extension)")
def create_assignment(assignment_file, output):
    """Creates a new assignment."""
    a = Assignment.from_file(assignment_file)
    a.to_notebook()

if __name__ == "__main__":
    app()
