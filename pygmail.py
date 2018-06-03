from authenticated import Session
from message import Mail


class Pygmail(object):
    """Send e-mails via the Gmail API

    Currently; only mail composition is supported but other features are
    possible as well and may be added in the future.

    Args:
        storage (str, optional): path to Oauth2 token storage
        secret (str, optional): path to Google Oauth2 client secret
        oauth_scope (str, optional): specification of authenticated privileges
    """
    def __init__(self, storage=None, secret=None, oauth_scope=None):
        self.api = Session(storage, secret, oauth_scope)

    def send(self, mail:Mail):
        """Send the passed mail object via the Gmail API

        Returns:
            dict containing sent mail-id, thread-id and label ids.
        """
        endpoint = self.api().users().messages()
        return endpoint.send(userId="me", body=mail.assemble()).execute()
