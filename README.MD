# python gmail relay
Simple python module used to send mails via the Gmail API.

The relay client makes use of Google's own Oauth2 authorization-flow so that a dedicated Google account can send arbitrary emails anywhere, on your behalf.
*I primarily made this module and these instructions with myself in mind*, but If you do happen to try this module, feel free to ask questions or suggest improvements.

## Usage
Initialize virtual environment and install packages:
```bash
$ pipenv --three install
```
Formal runtime invocation of the relay client:
```bash
$ pipenv run python3 relay.py

# or, if you want to avoid the venv, just plain and simple
$ python3 relay.py
```

Command-line options:
```
--subject       subject line
--body          message body
--to            space-separated list of recipients
--alias         name alias for the sender
```
