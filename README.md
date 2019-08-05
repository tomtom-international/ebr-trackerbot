# ebr-trackerbot

[![Build Status](https://dev.azure.com/tomtomweb/tomtomweb/_apis/build/status/GitHub-TomTom-International/?branchName=master)](https://dev.azure.com/tomtomweb/GitHub-TomTom-International/_build/latest?definitionId=5&branchName=master)

[![PyPI - Version](https://img.shields.io/pypi/v/ebr-trackerbot.svg)](https://pypi.org/project/ebr-trackerbot/)
[![PyPI - License](https://img.shields.io/pypi/l/ebr-trackerbot.svg)](https://pypi.org/project/ebr-trackerbot/)
[![PyPI - Python Versions](https://img.shields.io/pypi/pyversions/ebr-trackerbot.svg)](https://pypi.org/project/ebr-trackerbot/)
[![PyPI - Format](https://img.shields.io/pypi/format/ebr-trackerbot.svg)](https://pypi.org/project/ebr-trackerbot/)
[![PyPI - Status](https://img.shields.io/pypi/status/ebr-trackerbot.svg)](https://pypi.org/project/ebr-trackerbot/)
[![PyUp - Updates](https://pyup.io/repos/github/tomtom-international/ebr-trackerbot/shield.svg)](https://pyup.io/repos/github/tomtom-international/ebr-trackerbot/)
ebr tracker bot

## Features


**Tracker bot use configuration provided via environment variables**

* `SLACK_TOKEN` - (required) slack token which is used to connect slack server
* `API_URL` - (required) url to br board api endpoint. Used for periodical checks for failed tests.
* `BACKEND` - (optional) backend storage specification (memory or sqlite). Default is memory.
* `SQLITE_FILENAME` - (optional) sqlite filename path. Default is data.db
* `SLACK_MESSAGE_TEMPLATE` - (optional) custom slack message when test failed. Can contain these placeholders: {{test}} - test name, {{count}} - number of failures, {{period}} - time period


**How to run:**

`
docker run -e BR_URL=<br board url> -e API_URL=<api url> -e SLACK_TOKEN=<token> -e BACKEND=<memory|sqlite> -e SQLITE_FILENAME=<filename> tomtom-docker-registry.bintray.io/python/ebr_trackerbot python ebr-trackerbot
`


## Requirements

* [python3](https://www.python.org/downloads)
* [pip3](https://pip.pypa.io/en/stable/installing)
* [virtualenv >= 16.6.0](https://virtualenv.pypa.io/en/latest/installation/)

## Credits

This package was created with [Cookiecutter](https://github.com/cookiecutter/cookiecutter) and the [tomtom-international/cookiecutter-python](https://github.com/tomtom-international/cookiecutter-python) project template.
