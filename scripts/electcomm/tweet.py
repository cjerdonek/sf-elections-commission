
from datetime import date
import os
import re
import shlex

import tweepy
import yaml

USERNAME = "SFElectionsComm"
NAME_BOPEC = "Budget & Oversight of Public Elections Committee (BOPEC)"
NAME_COMMISSION = "Elections Commission"
WEB_SITE_HOME = "http://www.sfgov2.org/index.aspx?page=319"
WEB_SITE_MEETINGS = "http://www.sfgov2.org/index.aspx?page=1382"

BODY_NAMES = {'bopec': NAME_BOPEC, 'commission': NAME_COMMISSION}
URL_PATTERN = re.compile(r"http://\S*")


# All URLs get replaced by 22-character URLs (even if the original is shorter):
# https://support.twitter.com/articles/78124-posting-links-in-a-tweet
def get_length(tweet):
    """Calculate how long the URL will be once Twitter shortens it."""
    new_string, url_count = URL_PATTERN.subn("", tweet)
    return len(new_string) + url_count * 22


def parse_label(label):
    """For example: 2015_01_07_bopec."""
    parts = label.split("_")
    body = parts.pop()
    body_name = BODY_NAMES[body]
    year, month, day = (int(s) for s in parts)
    dt = date(year, month, day)
    return body_name, dt


def make_tweet(format_string, label):
    body, date = parse_label(label)
    return format_string.format(date=date, day=date.day, body=body,
                                home_page=WEB_SITE_HOME)

def get_cancel_tweet(label):
    # Date for example: Wed, January 7, 2015
    format = ("The {0} meeting of the {{body}} will not be held: {{home_page}}"
              .format("{date:%a, %B {day}, %Y}"))
    return make_tweet(format, label)


def get_config():
    repo_root = os.path.join(os.path.dirname(__file__), os.pardir)
    config_path = os.path.join(repo_root, 'temp.yaml')
    with open(config_path) as f:
        config = yaml.load(f)
    return config


def get_raw_oauth():
    """Return OAuthHandler without access token."""
    config = get_config()
    # The first value is the application's non-secret Consumer Key (API Key).
    # The second is the application's Consumer Secret (API Secret).
    api_key = config['twitter_consumer_api_key']
    api_secret = config['twitter_consumer_api_secret']
    auth = tweepy.OAuthHandler(api_key, api_secret)
    return auth


def get_oauth(username):
    """Return OAuthHandler with access token."""
    config = get_config()
    user_config = config['users'][username]
    key = user_config['twitter_access_token_key']
    secret = user_config['twitter_access_token_secret']

    auth = get_raw_oauth()
    auth.set_access_token(key, secret)

    return auth


def get_access_token():
    """Return an OAuth access token on behalf of a Twitter user.

    The access token never expires, so we can save this value.
    """
    auth = get_raw_oauth()
    # The return value has the form:
    # https://api.twitter.com/oauth/authorize?oauth_token=TOKEN
    url = auth.get_authorization_url()
    # Make sure we get authorization from the correct user in case a
    # different user is logged in.
    url = "{0}&force_login=1&screen_name={1}".format(url, USERNAME)
    cmd = "open {0}".format(shlex.quote(url))
    print("calling: {0}".format(cmd))
    os.system(cmd)
    # Prompt the user for the verifier code supplied by Twitter in the browser.
    verifier = input('Verifier: ').strip()
    access_token = auth.get_access_token(verifier)
    access_token_key, access_token_secret = access_token
    print("twitter_access_token_key: {0}".format(access_token_key))
    print("twitter_access_token_secret: {0}".format(access_token_secret))


def tweet(message=None):
    username = USERNAME
    if not message:
        message = input("message: ").strip()
    auth = get_oauth(username)
    api = tweepy.API(auth)
    response = input('Are you sure you want to tweet this?\n'
                     'user: {user}\n'
                     'text: "{text}"\n'
                     'length: {length} chars (reduced from {old_length})\n'
                     '(yes/no)? '
                     .format(user=username, text=message, length=get_length(message),
                             old_length=len(message)))
    if response != 'yes':
        exit('** Aborted.')
    api.update_status(message)


def main():
    label = '2015_01_07_bopec'
    print(get_cancel_tweet(label))
    exit()
    tweet()


if __name__ == '__main__':
    main()
