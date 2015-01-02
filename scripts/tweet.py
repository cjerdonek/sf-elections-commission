
import os
import shlex

import tweepy
import yaml

USERNAME = "SFElectionsComm"

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
    response = input('Are you sure you want to tweet this through '
                     'user: {user}?\n "{text}" [{length} chars]\n(yes/no)? '
                     .format(user=username, length=len(message), text=message))
    if response != 'yes':
        exit('** Aborted.')
    api.update_status(message)


def main():
    tweet()


if __name__ == '__main__':
    main()
