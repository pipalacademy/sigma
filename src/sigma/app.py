from flask import Flask, render_template, abort, jsonify

from . import preview

app = Flask(__name__)

preview_manager = preview.PreviewManager()


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/users")
def users():
    return render_template("users.html")

@app.route("/preview")
def preview_index():
    preview_manager.scan()
    collections = preview_manager.get_collections()
    print("collections", collections)
    return render_template("preview/index.html", collections=collections)

@app.route("/preview/<name>")
def preview_collection(name):
    collection = preview_manager.get_collection(name)
    if not collection:
        abort(404)
    print("collection", collection)
    return render_template("preview/collection.html", collection=collection)


@app.route("/preview/_tail/<owner>/<name>.ipynb")
def preview_tail(owner, name):
    collection = preview_manager.get_collection(name)
    nb = collection and collection.get_notebook(owner)
    if not nb:
        abort(404)

    return jsonify(nb.tail())
