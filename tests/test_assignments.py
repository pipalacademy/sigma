from sigma.assignments import AssignmentSolution
from sigma import config
from pathlib import Path

class TestAssignmentSolution:
    def test_find_username(self):
        assert AssignmentSolution.find_username("/home/jupyter-alice/assignment-01.ipynb") == "alice"
        assert AssignmentSolution.find_username("/home/jupyter-alice/assignments/assignment-01.ipynb") == "alice"

    def test_find_username_with_custom_home(self, monkeypatch):
        monkeypatch.setattr(config, "home_path", "/test/home")
        assert AssignmentSolution.find_username("/test/home/jupyter-alice/assignment-01.ipynb") == "alice"
        assert AssignmentSolution.find_username("/test/home/jupyter-alice/assignments/assignment-01.ipynb") == "alice"

    def test_from_path(self):
        path = "/home/jupyter-alice/assignment-01.ipynb"
        solution = AssignmentSolution.from_path("assignment-01", path)
        assert solution.assignment_name == "assignment-01"
        assert solution.username == "alice"
        assert solution.notebook_path == Path(path)

    def test_find_all(self, tmp_path, monkeypatch):
        home = tmp_path / "home"
        monkeypatch.setattr(config, "home_path", str(home))

        def make_notenook(username, filename):
            path = home / username / filename
            path.parent.mkdir(parents=True)
            path.write_text("foo bar")

        make_notenook("jupyter-alice", "assignment-01.ipynb")
        make_notenook("jupyter-bob", "assignment-01.ipynb")
        make_notenook("jupyter-charle", "hello-world.ipynb") # not submission

        solutions = AssignmentSolution.find_all("assignment-01")
        assert [s.username for s in solutions] == ["alice", "bob"]

    def test_submit(self, tmp_path, monkeypatch):
        home = tmp_path / "home"
        monkeypatch.setattr(config, "home_path", str(home))

        data_dir = tmp_path / "training-data"

        path = home / "jupyter-alice" / "assignment-01.ipynb"
        path.parent.mkdir(parents=True)
        path.write_text("hello-world")

        solution = AssignmentSolution.from_path("assignment-01", path)
        solution.submit(data_dir=data_dir)

        submission_path = data_dir / "assignment-submissions" / "assignment-01" / "alice" / "assignment-01.ipynb"

        assert submission_path.exists()
        assert submission_path.read_text() == path.read_text()
