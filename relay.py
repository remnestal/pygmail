import argparse
import httplib2
import base64

import sys
from pathlib import Path

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

from email.mime.text import MIMEText

OAUTH_SCOPE = 'https://www.googleapis.com/auth/gmail.compose'
CLIENT_SECRET_FILE = 'client_secret.json'
STORAGE_FILE = 'storage.json'

def main():
    """Parse input arguments and send mail

    First test of argparse implementation. default_args contains the default
    values of each input parameter.
    """
    credentials = __get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    profile = service.users().getProfile(userId="me").execute()
    sender = profile['emailAddress']
    default_args = {
        'subject': 'No subject',
        'body': 'Empty message',
        'to': sender,
        'alias': None
    }

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--subject',  default=default_args['subject'],  help='subject line')
    parser.add_argument('-b', '--body',     default=default_args['body'],     help='text body')
    parser.add_argument('-t', '--to',       default=default_args['to'],       help='whitespace-separated list of recipients')
    parser.add_argument('-a', '--alias',    default=default_args['alias'],    help='name alias for the sender')

    args = vars(parser.parse_args())
    args['sender'] = sender

    message = __create_message(args)
    __post_message(service, message)

def __get_credentials():
    """Retrieves valid user credentials

    If no credentials are found, or if they are invalid, the Oauth 2.0
    flow is completed to fetch a new set of valid credentials.

    Returns:
        credentials, a valid set of credentials
    """
    if not Path(CLIENT_SECRET_FILE).is_file():
        print('"%s" is required.' % CLIENT_SECRET_FILE)
        sys.exit(1)

    if not Path(STORAGE_FILE).is_file():
        open(STORAGE_FILE, 'a').close()

    credentials = Storage(STORAGE_FILE).get()
    if credentials is None or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, OAUTH_SCOPE)
        credentials = tools.run_flow(flow, STORAGE)

    return credentials

def __create_message(arguments):
    """Creates a base64 encoded email-message

    Creates a dict containing the body of the email, using 'raw' as the key.
    The message body is converted to a base64 string in order to become
    JSON serializable.

    Returns:
        mail_body, the body part of the email
    """
    message = MIMEText(arguments['body'])
    message['subject'] = arguments['subject']
    message['to'] = ",".join(arguments['to'].split())

    if arguments['alias']:
        message['from'] = "%s <%s>" % (arguments['alias'], arguments['sender'])
    else:
        message['from'] = arguments['sender']

    b64_bytes = base64.urlsafe_b64encode(message.as_bytes())
    b64_string = b64_bytes.decode()
    mail_body = {'raw': b64_string}

    return mail_body


def __post_message(service, mail_body):
    try:
        email = (service.users().messages().send(userId="me", body=mail_body).execute())
        print(email)
    except Exception as e:
        print('Exception: %s' % e)

if __name__ == '__main__':
    main()
