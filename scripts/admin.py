
from __future__ import absolute_import

from argparse import ArgumentParser
from datetime import date
import logging
import os
import sys

import set_path
from pycomm.email import send_email
# TODO: rename module to tweeting.
from pycomm import tweet as tweeting
from pycomm.config import get_config
# TODO: rename module to formatting.
from pycomm import formatter as formatting


def get_formatter():
    config = get_config()
    formatter = formatting.Formatter(config)
    return formatter


def next_day(dt, days=1):
    return date(dt.year, dt.month, dt.day + days)

def command_upcoming(ns):
    today = date.today()
    current = date(today.year, today.month, 1)
    while current.weekday() != 2:
        current = next_day(current, 1)
    print current
    print next_day(current, 14)


def show_image_size(ns):
    for x in xrange(56, 64):
        w, h = (16 * x, 9 * x)
        print("{0}:{1}".format(w, h))


def meeting_text(ns):
    meeting_label, text_type = ns.meeting_label, ns.text_type

    formatter = get_formatter()
    text = formatter.make_meeting_text(text_type, meeting_label)
    print(text)


def tweet(ns):
    meeting_label, text_type = ns.meeting_label, ns.text_type

    config = get_config()
    formatter = get_formatter()

    username = config.get_twitter_username('commission')
    text = formatter.make_tweet(text_type, meeting_label)
    tweeting.tweet(username, message=text)


def email(ns):
    config = get_config()
    sender = ("Chris Jerdonek", "foo@example.com")
    to_list = [("Chris Jerdonek", "foo@example.com")]
    path = "temp.txt"
    send_email(config, sender, to_list, subject="test", body="This is a test.",
               attach_paths=[path])

def create_parser():
    """Return an ArgumentParser object."""
    text_choices = sorted(formatting.TEMPLATES.keys())
    tweet_choices = sorted(formatting.TWEET_TEMPLATES.keys())

    root_parser = ArgumentParser(description="command for helping with admin tasks")

    sub = root_parser.add_subparsers(help='sub-command help')

    parser = sub.add_parser("upcoming", help="list labels for the next few regular meetings")
    parser.add_argument('--count', default=3, type=int,
        help=("show the meeting labels for the next COUNT regular meetings."))
    parser.set_defaults(run_command=command_upcoming)

    parser = sub.add_parser("meetingtext", help="generate meeting strings.")
    parser.add_argument('meeting_label', metavar='LABEL',
        help=("meeting label, for example 2015_01_07_bopec or 2015_01_21_commission."))
    parser.add_argument('text_type', metavar='TEXT_TYPE', choices=text_choices,
        help=("what text to generate."))
    parser.set_defaults(run_command=meeting_text)

    parser = sub.add_parser("meetingtweet", help="tweet about a meeting.")
    parser.add_argument('meeting_label', metavar='LABEL',
        help=("meeting label, for example 2015_01_07_bopec or 2015_01_21_commission."))
    parser.add_argument('text_type', metavar='TEXT_TYPE', choices=tweet_choices,
        help=("what text to tweet."))
    parser.set_defaults(run_command=tweet)

    parser = sub.add_parser("meetingemail", help="send an e-mail related to a meeting.")
    parser.add_argument('meeting_label', metavar='LABEL',
        help=("meeting label, for example 2015_01_07_bopec or 2015_01_21_commission."))
    parser.add_argument('email_type', metavar='EMAIL_TYPE', choices=('foo', ),
        help=("what e-mail to send."))
    parser.set_defaults(run_command=email)

    parser = sub.add_parser("imagesizes", help="show 16:9 image sizes to help with screen shots")
    parser.set_defaults(run_command=show_image_size)



    return root_parser


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    logging.basicConfig(level='INFO')
    parser = create_parser()
    ns = parser.parse_args(argv)
    ns.run_command(ns)


if __name__ == '__main__':
    main()
