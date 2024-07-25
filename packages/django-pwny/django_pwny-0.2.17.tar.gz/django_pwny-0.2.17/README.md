# `django-pwny`

*Have I Been Pwned?* password validator. Inspired by a
[blog post](https://www.thedatashed.co.uk/2019/02/07/django-pwny/) on
the subject.

## Quickstart

Install django-pwny:

```sh
pip install django-pwny
```

Add it to your `AUTH_PASSWORD_VALIDATORS`:

``` python
AUTH_PASSWORD_VALIDATORS = [
    ...
    "pwny.validation.HaveIBeenPwnedValidator",
    ...
]
```

## Features

- TODO

## Running Tests

Does the code actually work?

```sh
source <YOURVIRTUALENV>/bin/activate
(myenv) $ pip install Django requirements/test.txt
(myenv) $ tox
```

## Credits

Tools used in rendering this package:

- [Cookiecutter](https://github.com/audreyr/cookiecutter)
- [cookiecutter-djangopackage](https://github.com/pydanny/cookiecutter-djangopackage)
