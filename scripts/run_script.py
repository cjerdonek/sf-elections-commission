
from __future__ import absolute_import

import logging

from electcomm import email, tweet
from electcomm.config import get_config
from electcomm.formatter import Formatter


if __name__ == '__main__':
    logging.basicConfig(level='INFO')
    config = get_config()
    formatter = Formatter('2015_01_07_bopec')
    username = config.get_twitter_username('commission')
    text = formatter.make_tweet_announce()
    tweet.tweet(username, message=text)
