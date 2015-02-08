
from __future__ import absolute_import

from argparse import ArgumentParser
from datetime import date
import logging
import os
import sys

import set_path
from pycomm import common
from pycomm import emailing
# TODO: rename module to tweeting.
from pycomm import tweet as tweeting
from pycomm.config import get_config
from pycomm import formatting


def display(text):
    print(60 * "-")
    print(text)


def get_formatter():
    config = get_config()
    formatter = formatting.Formatter(config)
    return formatter


def command_labels(ns, formatter):
    labels = common.next_meeting_labels(month_count=3)
    for label in labels:
        print(label)


def command_text(ns, formatter):
    meeting_label, text_type = ns.meeting_label, ns.text_type
    text = formatter.get_meeting_text(text_type, meeting_label)
    display(text)


def command_index_html(ns, formatter):
    config = formatter.config
    text_type = "html_index"
    label = ns.meeting_label

    labels = config.get_next_meeting_labels(label)
    text = ""
    for label in labels:
        text += formatter.get_meeting_text(text_type, label)
    display(text)


def command_tweet(ns, formatter):
    config = formatter.config
    meeting_label, text_type = ns.meeting_label, ns.text_type

    username = config.get_twitter_username('commission')
    text = formatter.make_tweet(text_type, meeting_label)
    tweeting.tweet(config=config, username=username, message=text)


def email(ns, formatter):
    emailing.send_email(formatter=formatter, meeting=ns.meeting_label,
                        email_type=ns.email_type, attach_paths=ns.attach_paths)


def command_image_sizes(ns, formatter):
    for x in xrange(56, 64):
        w, h = (16 * x, 9 * x)
        print("{0}:{1}".format(w, h))


def add_meeting_label_argument(parser):
    parser.add_argument('meeting_label', metavar='MEETING',
        help=('meeting label, for example "20150107_bopec" or "20150121_commission".'))


def create_parser():
    """Return an ArgumentParser object."""
    email_choices = sorted(formatting.EMAIL_TEMPLATES.keys())
    text_choices = sorted(formatting.GENERAL_TEMPLATES.keys())
    tweet_choices = sorted(formatting.TWEET_TEMPLATES.keys())

    root_parser = ArgumentParser(description="command for helping with admin tasks")

    sub = root_parser.add_subparsers(help='sub-command help')

    parser = sub.add_parser("labels", help="list labels for the next few regular meetings")
    parser.add_argument('--count', default=3, type=int,
        help=("show the meeting labels for the next COUNT regular meetings."))
    parser.set_defaults(run_command=command_labels)

    parser = sub.add_parser("text", help="generate text blocks for meetings.")
    add_meeting_label_argument(parser)
    parser.add_argument('text_type', metavar='TEXT_TYPE', choices=text_choices,
        help=("what text to generate."))
    parser.set_defaults(run_command=command_text)

    parser = sub.add_parser("index_html", help="make the meeting index HTML "
                            "for the home page.")
    add_meeting_label_argument(parser)
    parser.add_argument('--count', default=3, type=int,
        help=("include the next COUNT meetings."))
    parser.set_defaults(run_command=command_index_html)

    parser = sub.add_parser("tweet", help="tweet about a meeting.")
    add_meeting_label_argument(parser)
    parser.add_argument('text_type', metavar='TEXT_TYPE', choices=tweet_choices,
        help=("what text to tweet."))
    parser.set_defaults(run_command=command_tweet)

    parser = sub.add_parser("email", help="send an e-mail related to a meeting.")
    add_meeting_label_argument(parser)
    parser.add_argument('email_type', metavar='EMAIL_TYPE', choices=email_choices,
        help=("what e-mail to send."))
    parser.add_argument('--attach', dest='attach_paths', metavar='PATH', nargs="*",
        help=("paths of any attachments."))
    parser.set_defaults(run_command=email)

    parser = sub.add_parser("imagesizes", help="show 16:9 image sizes to help with screen shots")
    parser.set_defaults(run_command=command_image_sizes)

    return root_parser


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    logging.basicConfig(level='INFO')
    parser = create_parser()
    ns = parser.parse_args(argv)
    formatter = get_formatter()
    ns.run_command(ns, formatter=formatter)


if __name__ == '__main__':
    main()
