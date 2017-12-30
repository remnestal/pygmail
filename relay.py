import httplib2
import base64

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

from email.mime.text import MIMEText

import requests
import json

OAUTH_SCOPE = 'https://www.googleapis.com/auth/gmail.compose'
CLIENT_SECRET_FILE = 'client_secret.json'
STORAGE = Storage('storage.json')

BACKUP_JOKE = 'It was supposed to be a joke here, but the API key has probably expired, so..\n\nI guess the joke is on me, Hahahahahaha!'

def main():
    """Hello, World!

    First test implementation of the Gmail-API
    Request a joke from webknox.com and send it to your mail
    """
    subject = 'Hello, World!'
    recipients = ['albin.remnestal@gmail.com']
    sender = 'authorized.sender@gmail.com'
    sender_alias = 'Funniest guy alive'

    # this is my idea of how to be funny
    try:
        response = requests.get('http://webknox.com/api/jokes/oneLiner?apiKey=bfbegfeaejnvrtohfkelpzaxzdxeqyh')
        fact = json.loads(response.text)['text']
    except:
        fact = BACKUP_JOKE

    __post_message(
        __get_credentials(),
        __create_message(subject, fact, recipients, sender, sender_alias))

def __get_credentials():
    """Retrieves valid user credentials

    If no credentials are found, or if they are invalid, the Oauth 2.0
    flow is completed to fetch a new set of valid credentials.

    Returns:
        credentials, a valid set of credentials
    """
    credentials = STORAGE.get()
    if credentials is None or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, OAUTH_SCOPE)
        credentials = tools.run_flow(flow, STORAGE)

    return credentials

def __create_message(subject, text, recipients, sender, sender_alias=None):
    """Creates a base64 encoded email-message

    Creates a dict containing the body of the email, using 'raw' as the key.
    The message body is converted to a base64 string in order to become
    JSON serializable.

    Returns:
        mail_body, the body part of the email
    """
    msg = MIMEText(text)
    msg['subject'] = subject
    msg['to'] = ",".join(recipients)
    if sender_alias:
        msg['from'] = "%s <%s>" % (sender_alias, sender)
    else:
        msg['from'] = sender

    b64_bytes = base64.urlsafe_b64encode(msg.as_bytes())
    b64_string = b64_bytes.decode()
    mail_body = {'raw': b64_string}

    return mail_body


def __post_message(credentials, mail_body):
    auth_http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=auth_http)
    try:
        email = (service.users().messages().send(userId="me", body=mail_body).execute())
        print(email)
    except Exception as e:
        print('Exception: %s' % e)

if __name__ == '__main__':
    main()
