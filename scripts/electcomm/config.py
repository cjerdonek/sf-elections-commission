
"""Exposes config data."""

import os
import yaml


def get_scripts_dir():
    return os.path.join(os.path.dirname(__file__), os.pardir)


def get_config():
    scripts_dir = get_scripts_dir()
    config_path = os.path.join(scripts_dir, 'data.yaml')
    with open(config_path) as f:
        data = yaml.load(f)
    twitter_path = os.path.join(scripts_dir, 'twitter.secret.yaml')
    with open(twitter_path) as f:
        twitter_data = yaml.load(f)

    return Config(data, twitter_data=twitter_data)


class Config(object):

    def __init__(self, data, twitter_data):
        self.data = data
        self.twitter_data = twitter_data

    def get_person(self, label):
        return self.data['people'][label]

    def get_google_client_secret_path(self):
        # Path to the client_secret.json file downloaded from the Developer Console
        scripts_dir = get_scripts_dir()
        return os.path.join(scripts_dir, 'google_client_secret.json')

    def get_twitter_consumer_creds(self):
        data = self.twitter_data
        # The first value is the application's non-secret Consumer Key (API Key).
        # The second is the application's Consumer Secret (API Secret).
        api_key = data['twitter_consumer_api_key']
        api_secret = data['twitter_consumer_api_secret']
        return api_key, api_secret

    def get_twitter_username(self, label):
        person = self.get_person(label)
        return person['twitter_username']

    def get_twitter_user_creds(self, username):
        data = self.twitter_data
        config = data['users'][username]
        key = config['twitter_access_token_key']
        secret = config['twitter_access_token_secret']
        return key, secret

    def get_email(self, label):
        """Return a realname, email_address 2-tuple."""
        person = self.data['people'][label]
        return person['name'], person['mail']
