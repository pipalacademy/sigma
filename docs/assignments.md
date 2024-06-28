# Assignments

One of the important elements of the trainings of Pipal Academy is giving assignments to the students. Sigma CLI provides utilities to create and grade assignments.

## Assignment Format

Each assignment is specified in an YAML file.

```
title: Assignment 01
description: |
    Please solve all the following problems.
    You have 2 days to solve all the assignments.
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
