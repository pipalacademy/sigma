from flask import Flask, abort, jsonify, redirect, render_template, request, url_for

from . import preview, settings
from .jupyterhub import JupyterHub

app = Flask(__name__)

preview_manager = preview.PreviewManager()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/settings")
def settings_page():
    _settings = settings.get_all_settings()
    values = settings.get_all()
    return render_template("settings.html", settings=_settings, values=values)


@app.route("/settings", methods=["POST"])
def settings_save():
    settings.save(request.form)
    return redirect(url_for("settings_page"))


@app.route("/users")
def users():
    hub = JupyterHub()
    users = hub.get_users()
    return render_template("users.html", users=users)


@app.route("/users", methods=["POST"])
def users_add():
    usernames = request.form["usernames"].strip().splitlines()
    if usernames:
        hub = JupyterHub()
        hub.add_users(usernames)

    return redirect(url_for("users"))


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
