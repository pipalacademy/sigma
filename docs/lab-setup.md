# Lab Setup

The lab server provides a jupyter lab instance for every participant using JupyterHub.

## Services

The services that run on the server are:

* The Little Jupyter Hub (TLJH)
* live-notes
* sigma (the dashboard)

## Paths

Most of the files used by the setup are in /opt.

```
files - sample files used by the problems
problems - all the problems available via the magic command %load_problem
python-practice-problems - the repository having the problems
sigma - the sigma repository
tljh - TLJH main directory
training - the repository of training notes
```

Some of these paths are symlinks to other directories.

## The URLs

The lab server is typically setup at <https://lab.pipal.in/>. Sometimes, we use the client name as a prefix (for example `arcesium-lab`).

The live-notes service is available at <https://live.lab.pipal.in> and the dashboard is available at <https://dashboard.lab.pipal.in>.

The routing of all these domains is done by the Traefik router which comes as part of TLJH setup. Custom configuration is placed in `/opt/tljh/state/rules` to enable that.

## Restarting Services

Restart JupyterHub:

```
$ sudo tljh-config reload
```

Restart Traefik proxy:

```
$ sudo tljh-config reload proxy
```

Restart Live Notes:

```
$ sudo systemctl restart live-notes
```

Restart dashboard:

```
$ sudo systemctl restart sigma
```

## Logs

Logs can be viewed using `journalctl` command by passing the service name.

To see the last 50 entries of the log:

```
$ sudo journalctl -n 50 -u $APP_NAME
```

To follow the logs (show new messages as they come):

```
$ sudo journalctl -n 50 -f -u $APP_NAME
```

### JupyterHub Logs

```
$ sudo journalctl -u jupyterhub
```

### Traefik Proxy Logs

```
$ sudo journalctl -u traefik
```

### User Server Logs

```
$ sudo journalctl -u jupyter-<username>
```

### Live Notes Logs

```
$ sudo journalctl -u live-notes
```

### Dashboard Logs

```
$ sudo journalctl -u sigma
```

### journalctl tips

Pass `-n N` to see last `N` entries. For example:

```
$ sudo journalctl -u live-notes -n 50
```

Pass `-f` to follow the logs to see the live output. For, example:

```
$ sudo journalctl -u live-notes -n 50 -f
```

## Troubleshooting

### `%%load_problem` and `%%verify_problem` not working

This can happen when the juputer startup script is not properly installed for a user.

Sigma install startup script at `~/.ipython/profile_default/startup/startup.py`.
You can check if that file is missing by running the following command. If the file is missing, it will give an error.

```
$ sudo ls -l /home/jupyter-<username>/.ipython/profile_default/startup/startup.py
-rw-r--r-- 1 jupyter-xxx jupyter-xxx 42 Jun 18 18:39 /home/jupyter-xxx/.ipython/profile_default/startup/startup.py
```

If the file is missing, do the following to create it.

```
$ sudo su jupyter-<username>
$ cd
$ mkdir -p ~/.ipython/profile_default/startup
$ cd  ~/.ipython/profile_default/startup
$ echo 'from sigma import magic; magic.register()' > startup.py
```

Restart the kernel of the notebook to load the magic commands.