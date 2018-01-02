# python gmail relay

* This relay client requires **python > 3.0**
* **pipenv** is not strictly required but encouraged for package management
    * Otherwise, all special requirements should be listed in the *Packages* section of *pygmail/Pipfile*

## Usage
Initialize virtual environment:
```bash
$ pipenv --three install
```
Formal runtime invocation of the relay client:
```bash
$ pipenv run python3 relay.py

# or, if you want to avoid venv, just plain and simple
$ python3 relay.py
```
However, I recommend either adding the script to PATH or creating a macro as such:
```bash
pygmail() { pipenv run python3 ~/bin/relay.py "$@"; }
```

## First time setup
### Setup Gmail access point
In order to actually use the Gmail API to send mails, you must first register an application that will act on your behalf. To send mails via this interface, the relay must therefore have a so called *client secret* to verify that it is a trusted agent of said application.

1. Register a new application *(project)* in the [Google API Console](https://console.developers.google.com/api)
2. Now from the [api/dashboard tab](console.developers.google.com/apis/dashboard), enable *Gmail API*
3. Then, generate a new **Oauth client ID** from the [api/credentials tab](https://console.developers.google.com/apis/credentials)
4. Click the download-button on the right to download the *client secret* as a JSON file. The relay's default search path for reading the client secret is *"pygmail/client_secret.json"*.  
**This client secret is supposed to be ... secret, so don't share it with anyone**.  

### Authorizing your application
If you have no previous Oauth access token or refresh tokens stored in *pygmail/storage.json*, you first have to authorize your application. This is authorization procedure is run everytime the API is called, however, if you have no valid Oauth tokens then Google will open your default browser and ask you to grant email-composing privileges to the *Google user that owns your application*, i.e. you. When you have accepted and the flow is completed, you will have a valid set of refresh tokens to use.

* Users who have granted access may revoke refresh tokens at any time.
* Refresh tokens may be revoked by Google if, for example, there are too many active refresh tokens in circulation. In that case you'll have to perform this authorization procedure again.

#### For all tin-foil hats
To avoid unnecessary security angst, I recommend that you create a special purpose *"mailbot"* account on Google; both for registering your application **(Gmail access point)** and for sending emails with this relay **(Authorization)**. This way you'd never put any of your real accounts into harms way.

## Gmail API

**Disclaimer!** Before you read the docs, please accept the following terms of agreement:  
- [ ] I hereby release, waive, discharge and covenant no to sue Albin, for any and all harm that may befall me from reading the API documentation.

[I didn't like my good mood anyway](https://developers.google.com/gmail/api/)
