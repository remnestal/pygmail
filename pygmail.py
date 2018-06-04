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

    if args.auth:
        pyg = Pygmail(args.token, args.credentials, invalidate=True)

def parse_arguments():
    """Parses input arguments and options"""
    parser = argparse.ArgumentParser()

    group = parser.add_mutually_exclusive_group()
    group.add_argument("--auth", action="store_true")
    parser.add_argument("-c", "--credentials", help="client-secret file")
    parser.add_argument("-t", "--token", help="token-storage file")

    args = parser.parse_args()
    sys.argv = [sys.argv[0]]
    return args

if __name__ == '__main__':
    main()
