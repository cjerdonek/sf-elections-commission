
from __future__ import absolute_import

from argparse import ArgumentParser
import logging
import sys

import set_path
from pycomm import email, tweet
from pycomm.config import get_config
# TODO: rename module to formatting.
from pycomm import formatter


def get_formatter():
    config = get_config()
    formatter_ = formatter.Formatter(config)
    return formatter_


def command_upcoming(ns):
    print ns


def command_tweet(ns):
    # config = get_config()
    # formatter = Formatter(config)
    # print(formatter.make_html_past_meeting('2014_12_17_commission'))
    # username = config.get_twitter_username('commission')
    # text = formatter.make_tweet_agenda_posted('2015_01_21_commission')
    # tweet.tweet(username, message=text)
    pass


def show_image_size(ns):
    for x in xrange(56, 64):
        w, h = (16 * x, 9 * x)
        print("{0}:{1}".format(w, h))


def meeting_text(ns):
    meeting_label = ns.meeting_label
    formatter = get_formatter()
    text = formatter.make_meeting_text('audio', meeting_label)
    print(text)


def create_parser():
    """Return an ArgumentParser object."""
    root_parser = ArgumentParser(description="command for helping with admin tasks")

    sub = root_parser.add_subparsers(help='sub-command help')

    parser = sub.add_parser("listupcoming", help="list labels for the next few regular meetings")
    parser.set_defaults(run_command=command_upcoming)

    parser = sub.add_parser("meetingtext", help="generate meeting strings.")
    parser.add_argument('meeting_label', metavar='LABEL',
        help=("meeting label, for example 2015_01_07_bopec or 2015_01_21_commission."))
    text_choices = sorted(formatter.TEMPLATES.keys())
    parser.add_argument('text_type', metavar='TEXT_TYPE', choices=text_choices,
        help=("what text to generate."))
    parser.set_defaults(run_command=meeting_text)

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
