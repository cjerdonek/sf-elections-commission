
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formataddr
import getpass
import logging
import os
from smtplib import SMTP
import sys
import tarfile

from electcomm.common import confirm
from electcomm.config import get_config


SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587

log = logging.getLogger("fbsubmit")


def add_attachment(mime_multipart, attachment_path):
    """Add an attachment to the given MIMEMultipart instance."""
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(open(attachment_path, 'rb').read())
    Encoders.encode_base64(part)
    part.add_header('Content-Disposition',
                    'attachment; filename="%s"' % os.path.basename(attachment_path))
    mime_multipart.attach(part)


def format_emails(addresses):
    return COMMASPACE.join(formataddr(a) for a in addresses)


def send_email(smtp_host, smtp_port, smtp_user, smtp_pass, from_address,
               to_addresses, cc_addresses, subject, body, attachment_paths):
    """Send an e-mail.

    All e-mail address arguments should be 2-tuples.
    """
    multi = MIMEMultipart()

    multi["From"] = formataddr(from_address)
    multi["To"] = format_emails(to_addresses)
    multi["Cc"] = format_emails(cc_addresses)
    multi["Subject"] = subject

    multi.attach(MIMEText(body))

    confirm("Are you sure you want to send the following?\n{line}\n{email}{line}\n\n".
            format(line=70*'*', email=multi.as_string()))

    for attachment_path in attachment_paths:
        add_attachment(multi, attachment_path)

    log.info("Connecting to: %s:%s..." % (smtp_host, smtp_port))
    smtp_connection = SMTP(smtp_host, smtp_port)
    smtp_connection.ehlo()
    smtp_connection.starttls()
    smtp_connection.ehlo()

    log.info("Logging into STMP server as: {0}...".format(smtp_user))
    smtp_connection.login(smtp_user, smtp_pass)

    recipient_addresses = to_addresses + cc_addresses

    log.info("Sending mail to: {0}...".format_emails(recipient_addresses))
    smtp_connection.sendmail(sender_address, recipient_addresses, multi.as_string())

    smtp_connection.close()


def main():
    config = get_config()
    settings = config.data['settings']

    smtp_host = settings['smtp_host']
    smtp_port = settings['smtp_port']
    smtp_user = settings['smtp_user']
    from_address = config.get_email('chris_gov')
    to_addresses = [config.get_email(label) for label in ('chris_test', )]

    smtp_pass = getpass.getpass(prompt=("Password for {0} ({1}): ".
                                        format(smtp_user, smtp_host)))

    send_email(smtp_host=smtp_host,
               smtp_port=smtp_port,
               smtp_user=smtp_user,
               smtp_pass=smtp_pass,
               from_address=from_address,
               to_addresses=to_addresses,
               cc_addresses=[],  # CC to the sender.
               subject="subject",
               body="body",
               attachment_paths=[])
