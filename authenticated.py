from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage


class Token(Storage):
    """ Class for storing and managing an Oauth2 refresh token """

    oauth_scope = 'https://www.googleapis.com/auth/gmail.compose'
    default_storage = 'storage.json'
    default_secret = 'client_secret.json'

    def __init__(self, storage=None, secret=None, invalidate=False):
        """ Read a stored Oauth2 token or generate a new one """

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

    def refresh_token(self):
        """ Request a new set of credentials via Google's auth-flow """

        flow = client.flow_from_clientsecrets(self.secret, self.oauth_scope)
        self.credentials = tools.run_flow(flow, Storage(self.storage))
