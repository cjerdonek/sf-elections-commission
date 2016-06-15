
from datetime import date
import os
import re
import shlex

import tweepy

from pycomm import common
from pycomm.config import get_config


# TODO: support https.
URL_PATTERN = re.compile(r"http://\S*")


# All URLs get replaced by 22-character URLs (even if the original is shorter):
# https://support.twitter.com/articles/78124-posting-links-in-a-tweet
def get_length(tweet):
    """Calculate how long the URL will be once Twitter shortens it."""
    new_string, url_count = URL_PATTERN.subn("", tweet)
    return len(new_string) + url_count * 22


def get_raw_oauth(config):
    """Return OAuthHandler without access token."""
    api_key, api_secret = config.get_twitter_consumer_creds()
    auth = tweepy.OAuthHandler(api_key, api_secret)

    return auth


def get_access_token(config):
    """Return an OAuth access token on behalf of a Twitter user.

    The access token never expires, so we can save this value.
    """
    username = config.get_twitter_username('commission')
    auth = get_raw_oauth(config)
    # The return value has the form:
    # https://api.twitter.com/oauth/authorize?oauth_token=TOKEN
    url = auth.get_authorization_url()
    # Make sure we get authorization from the correct user in case a
    # different user is logged in.
    url = "{0}&force_login=1&screen_name={1}".format(url, username)
    cmd = "open {0}".format(shlex.quote(url))
    print("calling: {0}".format(cmd))
    os.system(cmd)
    # Prompt the user for the verifier code supplied by Twitter in the browser.
    verifier = input('Verifier: ').strip()
    access_token = auth.get_access_token(verifier)
    access_token_key, access_token_secret = access_token
    print("twitter_access_token_key: {0}".format(access_token_key))
    print("twitter_access_token_secret: {0}".format(access_token_secret))


def get_oauth(config, username):
    """Return OAuthHandler with access token."""
    auth = get_raw_oauth(config)
    key, secret = config.get_twitter_user_creds(username)
    auth.set_access_token(key, secret)

    return auth


def tweet(config, username, message=None):
    if not message:
        message = input("message: ").strip()
    auth = get_oauth(config, username)
    api = tweepy.API(auth)

    msg = ('Are you sure you want to tweet this?\n'
           'user: {user}\n'
           'text: "{text}"\n'
           'length: {length} chars (reduced from {old_length})\n'
           .format(user=username, text=message, length=get_length(message),
                   old_length=len(message)))
    common.confirm(msg)
    # We need to use a kwarg here because of this issue:
    # https://github.com/tweepy/tweepy/issues/554
    api.update_status(status=message)
