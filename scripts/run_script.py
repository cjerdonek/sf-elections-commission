
from __future__ import absolute_import

import logging

import set_path
from pycomm import email, tweet
from pycomm.config import get_config
from pycomm.formatter import Formatter


if __name__ == '__main__':
    logging.basicConfig(level='INFO')
    config = get_config()
    formatter = Formatter(config)
    print(formatter.make_html_past_meeting('2014_12_17_commission'))
    # username = config.get_twitter_username('commission')
    # text = formatter.make_tweet_agenda_posted('2015_01_21_commission')
    # tweet.tweet(username, message=text)
