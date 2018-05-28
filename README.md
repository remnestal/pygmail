# python gmail relay
Simple python module used to send mails via the Gmail API.

The relay script makes use of Google's authorization flow (Oauth2) so that a dedicated Google account can send arbitrary emails anywhere, on your behalf.

> I often use emails as a convenient way for my _less intelligent_ connected devices to send logs, crash reports, etc to myself. Now I've implemented this strategy more times than I care to remember, so it made sense to finally create some reusable piece of code! Thus, I made this module with myself in mind but feel free to use it however you want as per the [licence](https://github.com/remnestal/pygmail/blob/master/LICENSE).

## Requirements
* [pipenv](https://github.com/pypa/pipenv) (for your convenience)
* [python3](https://www.python.org/downloads/) (for my convenience)

## Usage
Initialize virtual environment and install packages:
```bash
$ pipenv --three install
```
Formal command-line invocation of the relay as a standalone module:
```bash
$ pipenv run python3 relay.py

# or, if you want to drop the venv, just plain and simple
$ python3 relay.py
```

Command-line options:
```
--subject       subject line
--body          message body
--to            space-separated list of recipients
--alias         name alias for the sender
```
