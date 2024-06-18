from pathlib import Path

from sigma.preview import Collection, Notebook, PreviewManager


class TestNotebook:
    def test_from_path(self):
        path = Path("/home/jupyter-alpha/session1.ipynb")
        nb = Notebook.from_path(path)
        assert nb.name == "session1"
        assert nb.filename == "session1.ipynb"
        assert nb.owner == "alpha"
        assert nb.path == path


class TestCollection:
    def test_from_paths(self):
        path1 = Path("/home/jupyter-alpha/session1.ipynb")
        path2 = Path("/home/jupyter-beta/session1.ipynb")

        c = Collection.from_paths("session1", [path1, path2])
        assert c.name == "session1"
        assert c.size == 2
        assert [nb.owner for nb in c.notebooks] == ["alpha", "beta"]


class TestPreviewManager:
    def test_scan(self, tmp_path):
        home = tmp_path / "home"
        home.mkdir(exist_ok=True)

        p1 = home / "jupyter-alpha" / "session1.ipynb"
        p2 = home / "jupyter-alpha" / "session2.ipynb"
        p3 = home / "jupyter-beta" / "session1.ipynb"
        p4 = home / "jupyter-beta" / "session2.ipynb"
        p5 = home / "jupyter-gamma" / "session1.ipynb"

        paths = [p1, p2, p3, p4, p5]
        for p in paths:
            p.parent.mkdir(exist_ok=True)
            p.touch()

        p = PreviewManager(home)
        assert len(p.get_collections()) == 2
        assert [c.name for c in p.get_collections()] == ["session1", "session2"]

        c = p.get_collection("session1")
        assert c.name == "session1"
        assert c.size == 3
        assert [nb.owner for nb in c.notebooks] == ["alpha", "beta", "gamma"]

        c = p.get_collection("session2")
        assert c.name == "session2"
        assert c.size == 2
        assert [nb.owner for nb in c.notebooks] == ["alpha", "beta"]
