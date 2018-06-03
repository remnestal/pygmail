import httplib2
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage


class Session(object):
    """Handler class for making authenticated calls to the Gmail API"""

    def __init__(self, storage=None, secret=None):
        """Set up the authenticated session with the Gmail API"""
        self.token = Token(storage, secret)
        self.service = self.start_service()

    def start_service(self):
        """Initialize the API connection"""
        http = self.token().authorize(httplib2.Http())
        return discovery.build('gmail', 'v1', http=http)

    def __call__(self):
        """Return the Gmail API handle"""
        return self.service


class Token(Storage):
    """Class for storing and managing an Oauth2 refresh token"""

    oauth_scope = 'https://www.googleapis.com/auth/gmail.compose'
    default_storage = 'storage.json'
    default_secret = 'client_secret.json'

    def __init__(self, storage=None, secret=None, invalidate=False):
        """Read a stored Oauth2 token or generate a new one"""

        self.storage = storage or self.default_storage
        self.secret = secret or self.default_secret

        if invalidate:
            self.refresh_token()
        else:
            stored_token = Storage(self.storage).get()
            if stored_token is None or stored_token.invalid:
                self.refresh_token()
            else:
                self.credentials = stored_token

    def __call__(self):
        """Return the OAuth2Credentials associated with this token"""
        return self.credentials

    def refresh_token(self):
        """Request a new set of credentials via Google's auth-flow

        Raises:
            FileNotFoundError: if client-secret file does not exist
        """

        # check that the specified client secret file exists
        with open(self.secret) as _:
            pass

        flow = client.flow_from_clientsecrets(self.secret, self.oauth_scope)
        self.credentials = tools.run_flow(flow, Storage(self.storage))
