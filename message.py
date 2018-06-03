import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Mail(object):
    """Class for representing e-mail messages

    Attributes:
        data (dict): structure for storing email content and metadata
    """

    def __init__(self, toaddr, fromaddr, subject, body):
        """Instantiate the e-mail massage with the passed data

        Args:
            toaddr (str): space separated string of recipient-addresses
            fromaddr (str): email-address of sender
            subject (str): subject-line of the mail
            body (str): message to be sent
        """
        self.data = {
            'toaddr': toaddr,
            'fromaddr': fromaddr,
            'subject': subject,
            'body': body
        }

    def assemble(self):
        """Returns a JSON serializable MIMEMultipart object"""
        msg = MIMEMultipart()

        msg.attach(MIMEText(self.data['body'], 'plain'))
        msg['subject'] = self.data['subject']
        msg['from'] = self.data['fromaddr']
        msg['to'] = self.data['toaddr']

        # make the mail-content JSON serializable
        b64_bytes = base64.urlsafe_b64encode(msg.as_bytes())
        b64_string = b64_bytes.decode()
        return {'raw': b64_string}

    def alias(name, mailaddr):
        """Returns the passed mailaddr labeled with the specified name"""
        return '{} <{}>'.format(name, mailaddr)
