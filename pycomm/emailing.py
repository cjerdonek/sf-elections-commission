
from __future__ import absolute_import

import argparse
import base64
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import email.utils as email_utils
import getpass
import httplib2
import logging
import mimetypes
import os
import sys
import textwrap

from apiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client import tools

from pycomm import common
from pycomm import formatting


def get_email_info(formatter, email_choice, meeting_label):
    """Return an EmailInfo object."""
    config = formatter.config
    # Calling this method also checks that the meeting label is valid.
    body, date, data = formatting.get_meeting_info(config, meeting_label)

    sender = body.sender
    to_list = []
    cc_list = []
    bcc_list = []
    if email_choice == 'public_notice':
        to_list += [sender]
        bcc_list = config.get_entities('distribution')
        if body.public_bcc is not None:
            bcc_list += body.public_bcc
    elif email_choice == 'body_notice':
        to_list += body.body_to
        cc_list += body.body_cc
    else:
        raise Exception("invalid email args: {0}".format((email_choice, meeting_label)))

    subject, body = formatter.get_email_texts(email_choice=email_choice, meeting_label=meeting_label)

    sender = config.get_email(sender)
    to_list = [config.get_email(val) for val in to_list]
    cc_list = [config.get_email(val) for val in cc_list]
    bcc_list = [config.get_email(val) for val in bcc_list]

    info = EmailInfo(subject=subject, body=body, sender=sender, to_list=to_list,
                     cc_list=cc_list, bcc_list=bcc_list)
    return info


def format_email(address):
    """Format an e-mail.

    Arguments:
      address: an e-mail address as a string or as a 2-tuple of the form
      (realname, email_address).
    """
    if isinstance(address, basestring):
        address = (False, address)
    return email_utils.formataddr(address)


def format_emails(addresses):
    return email_utils.COMMASPACE.join(format_email(a) for a in addresses)


def _add_email_info(mime, from_address, to_addresses, subject, cc_list=None, bcc_list=None):
    """
    In this function, each e-mail address should be a 2-tuple of the form:
    realname, email_address.  If there is no realname, then make it something
    that evaluates to false.

    Arguments:
      message: a MIMEText or MIMEMultipart object, for example
        MIMEText(message_text) or MIMEMultipart().
    """
    mime["From"] = format_email(from_address)
    mime["To"] = format_emails(to_addresses)
    if cc_list:
        mime["Cc"] = format_emails(cc_list)
    if bcc_list:
        mime["Bcc"] = format_emails(bcc_list)
    mime["Subject"] = subject


# TODO: allow a filename different from the filename used on disk.
def _add_attachment(mime, path):
    content_type, encoding = mimetypes.guess_type(path)
    if content_type is None or encoding is not None:
        content_type = 'application/octet-stream'
    main_type, sub_type = content_type.split('/', 1)

    with open(path, 'rb') as f:
        contents = f.read()

    if main_type == 'text':
        mime_cls = MIMEText
    elif main_type == 'image':
        mime_cls = MIMEImage
    elif main_type == 'audio':
        mime_cls = MIMEAudio
    else:
        mime_cls = MIMEBase

    if mime_cls is MIMEBase:
        msg = mime_cls(main_type, sub_type)
        msg.set_payload(contents)
    else:
        msg = mime_cls(contents, _subtype=sub_type)

    filename = os.path.basename(path)
    msg.add_header('Content-Disposition', 'attachment', filename=filename)
    mime.attach(msg)


# This function was copied and modified from here:
# https://developers.google.com/gmail/api/guides/sending
def create_message(sender, to_list, subject, body, cc_list=None, bcc_list=None,
                   attach_paths=None):
    """Create an email message for the Google Gmail API.

    Arguments:
      message: a MIMEText or MIMEMultipart object.

    Returns:
      An object containing a base64url encoded email object.
    """
    message = MIMEText(body)
    mime = MIMEMultipart() if attach_paths else message
    _add_email_info(mime, sender, to_list, subject, cc_list=cc_list, bcc_list=bcc_list)

    if attach_paths:
        mime.attach(message)

    printable = mime.as_string()

    if attach_paths:
        for path in attach_paths:
            _add_attachment(mime, path)

        printable += "\n**Attachment paths:\n\n"
        for i, path in enumerate(attach_paths, start=1):
            printable += "{0}. {1}\n".format(i, os.path.abspath(path))

    return {'raw': base64.urlsafe_b64encode(mime.as_string())}, printable


def get_email_service(config):
    """Return an authorized Gmail API service instance."""
    google_client_secret_path = config.get_google_client_secret_path()
    # The "scope" scope allows--
    #   "Create, read, update, and delete drafts. Send messages and drafts."
    # Check https://developers.google.com/gmail/api/auth/scopes for all
    # available scopes
    OAUTH_SCOPE = 'https://www.googleapis.com/auth/gmail.compose'
    # Start the OAuth flow to retrieve credentials
    flow = flow_from_clientsecrets(google_client_secret_path, scope=OAUTH_SCOPE)

    http = httplib2.Http()
    # Get default flags.
    parser = argparse.ArgumentParser(parents=[tools.argparser])
    flags = parser.parse_args([])
    print("debug: flags: {0!r}".format(flags))
    # Location of the credentials storage file
    storage_path = config.get_gmail_storage_path()
    storage = Storage(storage_path)
    # Try to retrieve credentials from storage or run the flow to generate them
    credentials = storage.get()
    if credentials is None or credentials.invalid:
        credentials = tools.run_flow(flow, storage, flags=flags, http=http)

    # Authorize the httplib2.Http object with our credentials
    http = credentials.authorize(http)

    # Build the Gmail service from discovery
    gmail_service = build('gmail', 'v1', http=http)

    return gmail_service


def send_message(service, message):
    """Send an email message.

    Args:
      service: Authorized Gmail API service instance.
      message: Message to be sent.

    Returns:
      Sent Message.
    """
    messages = service.users().messages()
    # userId should be the user's email address.  The special value "me" can
    # be used to indicate the authenticated user.
    message = messages.send(userId='me', body=message).execute()
    print("e-mail sent: Gmail API: message_id={0}".format(message['id']))
    return message


def raw_send_email(config, sender, to_list, subject, body, cc_list=None,
                   bcc_list=None, attach_paths=None):
    """Send an email message.

    Each e-mail address in the arguments should be a 2-tuple of the form:
    (realname, email_address).  If there is no realname, then make it
    something that evaluates to false.
    """
    message, printable = create_message(sender, to_list, subject, body,
                                        cc_list=cc_list, bcc_list=bcc_list,
                                        attach_paths=attach_paths)
    confirm_text = textwrap.dedent("""\
    Are you sure you want to send the following?
    {line}
    {email}
    {line}
    """).format(line=70*'*', email=printable)
    common.confirm(confirm_text)
    service = get_email_service(config)
    send_message(service, message)


def send_email(formatter, email_choice, meeting_label, attach_paths=None):
    info = get_email_info(formatter, email_choice, meeting_label=meeting_label)
    raw_send_email(config=formatter.config, subject=info.subject, body=info.body,
                   sender=info.sender, to_list=info.to_list,
                   cc_list=info.cc_list, bcc_list=info.bcc_list,
                   attach_paths=attach_paths)


class EmailInfo(object):

    def __init__(self, sender, to_list, cc_list, bcc_list, subject, body):
        self.sender = sender
        self.to_list = to_list
        self.cc_list = cc_list
        self.bcc_list = bcc_list
        self.subject = subject
        self.body = body
