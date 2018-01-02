# python gmail relay
Simple python module used to send mails via the Gmail API.

The relay client makes use of Google's own Oauth2 authorization-flow so that a dedicated Google account can send arbitrary emails anywhere, on your behalf.
*I primarily made this module and these instructions with myself in mind*, but If you do happen to try this module, feel free to ask questions or suggest improvements.

#### Why
I wanted a simple way to send emails from python, or anything that can invoke python for that matter. Obviously I don't want to set up a personal mailserver on every device I use, so I settled to using Gmail for convenient abstraction of the problem.

Storing and passing your Google account's *username* and *password* with each POST request seems like a **very bad** way of doing it (even if you're using an expendable account for sending emails) and the right way of authenticating on the web is obviously Oauth. As it happens, this approach is not entirely straight forward and can at some points be fairly difficult to grasp. I for one often make use of email-notifications in my projects; to issue warnings or to make me more aware using periodic status reports, and you quickly get tired of reinventing the wheel every time you just want to send a lousy email.

Therefore, I made this simple Python module to make my life a whole lot easier.

#### Requirements
* The relay client has some components that require **python version > 3.0**
* **pipenv** is used for package management, and is not a strict requirement but encouraged for your convenience.
* Required packages are listed in the *"packages"* section of **pygmail/Pipfile** (installed automatically by *pipenv*)

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
However, for using this module as a quick and dirty standalone way of passing around files and information, I recommend either simply adding the script to PATH or creating a simple macro.

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
