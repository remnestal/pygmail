# python gmail relay
Simple python module used to send mails via the Gmail API.

The relay script makes use of Google's authorization flow (Oauth2) so that a dedicated Google account can send arbitrary emails anywhere, on your behalf.

> I often use emails as a convenient way for my _less intelligent_ connected devices to send logs, crash reports, etc to myself. Now I've implemented this strategy more times than I care to remember, so it made sense to finally create some reusable piece of code! Thus, I made this module with myself in mind but feel free to use it however you want as per the **[Good Boy Licence](https://icons8.com/good-boy-license/)**.

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
$ pipenv run python3 pygmail.py

# e.g.
$ pipenv run python3 pygmail.py --auth --token "new_token.json"
$ pipenv run python3 pygmail.py --send --token "johndoe.json" -s "Mr. Edwards from First National Bank" -b "I am writing you based on the need of you or your company to assist me with a fund transfer."
```

Command-line options:
```
# control flow options
--auth          run the authorization flow for a Google account
--send          send a mail via the standalone main module
-t, --token         (optional) custom location of the token storage
-c, --credentials   (optional) custom location of the client secret

# mail options
-s, --subject       subject line
-b, --body          message body
-r, --recipents     space-separated list of recipients
```

* **token** defaults to `repo/storage.json`
* **credentials** defaults to `repo/client_secret.json`
