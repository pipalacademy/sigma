# Assignments

One of the important elements of the trainings of Pipal Academy is giving assignments to the students. Sigma CLI provides utilities to create and grade assignments.

## Assignment Format

Each assignment is specified in an YAML file.

```
title: Assignment 01
description: |
    Please solve all the following problems.
    You have 2 days to solve all the problems and submit the assignment.
problems:
    - mean
    - product
    - digit-count
```

The problems are taken from the private repository [python-practice-problems](https://github.com/pipalacademy/python-practice-problems).


## Creating assignments

To create an assignment, create an YAML file for the assignment.

```
$ cat assignment-01.yml
title: Assignment 01
description: |
    Please solve all the following problems.
    You have 2 days to solve all the assignments.
problems:
    - mean
    - product
    - digit-count
```

To generate a notebook for the assignment, run the following command.

```
$ sigma create-assignment assignment-01.yml
created assignment-01.ipynb
```

Please note that the created the notebook file will have the same name as YAML file, but with extension `.ipynb`.

!!! note

    If you want to try creating assignments in your local dev environment,
    you may have to configure the path to the problems directory. By default,
    it is assumed that the problems are at `/opt/problems`.

    You can specify a different path by setting the environment variable
    `SIGMA_PROBLEMS_ROOT`.

        $ export SIGMA_PROBLEMS_ROOT=/home/anand/github/pipalacademy/python-practice-problems/python
        $ sigma create-assignment assignment-01.yml
        created assignment-01.iynb

## Collecting Assignments

After the deadline for an assignment, the instructor need to collect the assignment manually or through a cron job. There is no way for the students to submit their own assignments.

The assignment solutions will be maintaining in the directory `training-data/assignment-submissions`.

To collect an assignment:

```
$ sigma collect-assignment assignment-01
Submitted /home/jupyter-alice/assignment-01.ipynb to training-data/assignment-submissions/assignment-01/alice/assignment-01.ipynb
Submitted /home/jupyter-bob/assignment-01.ipynb to training-data/assignment-submissions/assignment-01/bob/assignment-01.ipynb
```

By default, sigma assumes that the assignment solutions are in the home directory. Sometimes, the assignments are kept in `assignments/` directory. In such a case, pass `--assignment-dir` option to tell sigma to take that into account.

```
$ sigma collect-assignment assignment-01 --assignment-dir assignments
Submitted /home/jupyter-alice/assignments/assignment-01.ipynb to training-data/assignment-submissions/assignment-01/alice/assignment-01.ipynb
Submitted /home/jupyter-bob/assignments/assignment-01.ipynb to training-data/assignment-submissions/assignment-01/bob/assignment-01.ipynb
```