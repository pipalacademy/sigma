# sigma

Sigma is a collection of tools to streamline the trainings for Pipal Academy.

Documentation: https://pipalacademy.github.io/sigma/

## Overview

One of the main components of sigma is the dashboard webapp. The dashboard webapp is planned to have the following features.

* Preview - preview the notebooks of students
* User Management - Add/Remove users from JupyterHub
* Sharing Files - Share/distribute files with every participant
* Solution Tracker - Track the problems solved
* Grader - Grade Assignments

## The Setup

Sigma uses python packaging tool [hatch]][] for developement.

[hatch]: https://hatch.pypa.io/latest/


Install Hatch by running:

```
$ pip install hatch
```

Please note that it is suggested that you run this not in a virtualenv, so that you continue to access it even when you switch to a diffent virtualenv.

While the project uses hatch, a Makefile has been added to make it easier to run all the tasks.

## Run dashboard app

```
$ make run
hatch run app
 * Serving Flask app 'sigma.dashboard.app'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with watchdog (inotify)
```

You can visit the app at `http://127.0.0.1:5000/`.

## Docs

Sigma uses [mkdocs-material][] for documentation.

[mkdocs-material]: https://squidfunk.github.io/mkdocs-material/

The source files for the docs are in `docs/` directory.

To build docs locally, run `make docs` and to serve docs with live reload, run `make serve-docs`.

## License

Sigma is licensed under MIT License.