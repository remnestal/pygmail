from authenticated import Session
from message import Mail
import argparse
import sys


class Pygmail(object):
    """Send e-mails via the Gmail API

    Currently; only mail composition is supported but other features are
    possible as well and may be added in the future.

    Args:
        storage (str, optional): path to Oauth2 token storage
        secret (str, optional): path to Google Oauth2 client secret
        oauth_scope (str, optional): specification of authenticated privileges
    """
    def __init__(self, storage=None, secret=None, oauth_scope=None,
                 invalidate=False):
        self.api = Session(storage, secret, oauth_scope, invalidate)

    def authorized_address(self):
        """Return the email-address of the user authorized in this session"""
        profile = self.api().users().getProfile(userId="me").execute()
        return profile['emailAddress']

    def send(self, mail:Mail):
        """Send the passed mail object via the Gmail API

        Returns:
            dict containing sent mail-id, thread-id and label ids.
        """
        endpoint = self.api().users().messages()
        return endpoint.send(userId="me", body=mail.assemble()).execute()

def main():
    """Run pygmail as a standalone module"""
    args = parse_arguments()
    if args.auth:
        # run authorization flow anew
        pyg = Pygmail(args.token, args.credentials, invalidate=True)
    elif args.send:
        pyg = Pygmail(args.token, args.credentials)
        mail = Mail(args.recipients,
                    pyg.authorized_address(),
                    subject=args.subject,
                    body=args.body)
        print(pyg.send(mail))

def parse_arguments():
    """Parses input arguments and options"""
    parser = argparse.ArgumentParser()

    group = parser.add_mutually_exclusive_group()
    group.add_argument('--auth', action='store_true',
                       help='authorize pygmail to send emails from your account.')
    group.add_argument('--send', action='store_true',
                       help='send an email through pygmail.')
    parser.add_argument('-c', '--credentials',
                        help='location of client-secret file')
    parser.add_argument('-t', '--token',
                        help='location of token-storage file')

    # email message configuration
    parser.add_argument('-s', '--subject',
                        help='subject line of the email')
    parser.add_argument('-b', '--body',
                        help='text body of the email')
    parser.add_argument('-r', '--recipients',
                        help='space-separated list of recipients\' email addresses')

    args = parser.parse_args()
    sys.argv = [sys.argv[0]]
    return args

if __name__ == '__main__':
    main()
