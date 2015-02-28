
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


def command_upcoming(ns, formatter):
    labels = common.next_meeting_labels(count=ns.count)
    for label in labels:
        print(label)


def command_text(ns, formatter):
    meeting_label, text_type = ns.meeting_label, ns.text_type
    text = formatter.get_meeting_text(text_type, meeting_label)
    display(text)


def command_index_html(ns, formatter):
    config = formatter.config
    text_type = "html_index"
    labels = config.get_next_meeting_labels(count=ns.count)
    text = ""
    for label in labels:
        text += formatter.get_meeting_text(text_type, label)
    display(text)


def command_tweet(ns, formatter):
    config = formatter.config
    username = config.get_twitter_username('commission')
    tweeting.tweet(config=config, username=username, message=None)


def command_tweet_meeting(ns, formatter):
    config = formatter.config
    meeting_label, text_type = ns.meeting_label, ns.text_type

    username = config.get_twitter_username('commission')
    text = formatter.make_tweet(text_type, meeting_label)
    tweeting.tweet(config=config, username=username, message=text)


def command_email(ns, formatter):
    emailing.send_email(formatter=formatter, meeting_label=ns.meeting_label,
                        email_choice=ns.email_type, attach_paths=ns.attach_paths)


def command_image_sizes(ns, formatter):
    for x in xrange(56, 64):
        w, h = (16 * x, 9 * x)
        print("{0}:{1}".format(w, h))


def add_count_argument(parser, default=None):
    if default is None:
        default = 3
    parser.add_argument('--count', default=default, type=int,
        help=("include the next COUNT meetings.  Defaults to {0}".format(default)))

def add_meeting_label_argument(parser):
    parser.add_argument('meeting_label', metavar='MEETING',
        help=('meeting label, for example "20150107_bopec" or "20150121_commission".'))


def make_subparser(sub, command_name, desc=None, **kwargs):
    # Capitalize the first letter for the long description.
    capitalized = desc[0].upper() + desc[1:]
    parser = sub.add_parser(command_name, help=desc, description=capitalized, **kwargs)
    return parser


def create_parser():
    """Return an ArgumentParser object."""
    email_choices = sorted(formatting.EMAIL_CHOICES)
    text_choices = sorted(formatting.GENERAL_TEMPLATES.keys())
    tweet_choices = sorted(formatting.TWEET_CHOICES)

    root_parser = ArgumentParser(description="command for helping with admin tasks")

    sub = root_parser.add_subparsers(help='sub-command help')

    parser = make_subparser(sub, "upcoming",
                desc="generate the labels for the upcoming regular meetings.")
    add_count_argument(parser)
    parser.set_defaults(run_command=command_upcoming)

    parser = sub.add_parser("text", help="generate text blocks for meetings.")
    add_meeting_label_argument(parser)
    parser.add_argument('text_type', metavar='TEXT_TYPE', choices=text_choices,
        help=("what text to generate."))
    parser.set_defaults(run_command=command_text)

    parser = make_subparser(sub, "index_html", desc="make the meeting index HTML for the home page.")
    add_count_argument(parser)
    parser.set_defaults(run_command=command_index_html)

    parser = make_subparser(sub, "email", desc="send an e-mail related to a meeting.")
    add_meeting_label_argument(parser)
    parser.add_argument('email_type', metavar='EMAIL_TYPE', choices=email_choices,
        help=("what e-mail to send."))
    parser.add_argument('--attach', dest='attach_paths', metavar='PATH', nargs="*",
        help=("paths of any attachments."))
    parser.set_defaults(run_command=command_email)

    parser = make_subparser(sub, "tweet", desc="send a tweet.")
    parser.set_defaults(run_command=command_tweet)

    parser = sub.add_parser("tweet_meeting", help="send a tweet related to a meeting.")
    add_meeting_label_argument(parser)
    parser.add_argument('text_type', metavar='TEXT_TYPE', choices=tweet_choices,
        help=("what text to tweet."))
    parser.set_defaults(run_command=command_tweet_meeting)

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
