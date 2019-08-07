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


## Configuration

Configure the vault authentication and vault credentials as described here: https://github.com/tomtom-international/vault-anyconfig#files-and-formatting
Provide an empty file for both if you will not be using Vault.

Provide the following required configuration via a YAML file:

```yaml
ebr-trackerbot:
    slack_token: slack API token (a secret value, should be stored in Vault)
    apiurl: url to ebr board api endpoint
```

Optional settings (also to be included in the ebr-trackerbot section):

* `init_channel`: a message will be posted in this channel at startup, must be set to an existing channel. Default is `#test-slackbot`.
* `storage_backend`: backend storage medium (memory or sqlite). Default is memory.
* `sqlite_filename`: sqlite filename path. Default is data.db
* `slack_message_template`: custom slack message when test failed. Can contain these placeholders: {{test}} - test name, {{count}} - number of failures, {{period}} - time period. Default is an empty string.
* `check_tests_delay`: frequency in which to check for test failures, specified in seconds. Default is 8600 seconds (one day).
* `log_level`: sets the logging level. See https://docs.python.org/3/library/logging.html#logging-levels for the level options. Default is `ERROR`.

**Note** any entry can be stored in Hashicorp Vault using vault-anyconfig. See https://github.com/tomtom-international/vault-anyconfig#main-configuration-file
for details.


## Run with Docker:

By default, the Docker image assumes a combine vault configuration and credentials file named `vault.yaml`. If you are not using Vault, this can be an
empty  file, otherwise see the configuration section above.

`docker run -e BR_URL=<br board url> -v ${pwd}/config.yaml:/etc/ebr-trackerbot/config.yaml -v ${pwd}/vault.yaml:/etc/ebr-trackerbot/vault.yaml tomtom-docker-registry.bintray.io/python/ebr_trackerbot python ebr-trackerbot`


## Requirements

* [python3](https://www.python.org/downloads)
* [pip3](https://pip.pypa.io/en/stable/installing)
* [virtualenv >= 16.6.0](https://virtualenv.pypa.io/en/latest/installation/)

## Credits

This package was created with [Cookiecutter](https://github.com/cookiecutter/cookiecutter) and the [tomtom-international/cookiecutter-python](https://github.com/tomtom-international/cookiecutter-python) project template.
