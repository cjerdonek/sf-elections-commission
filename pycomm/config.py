
"""Exposes config data."""

import os
import yaml


REPO_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

def get_config_file(file_name):
    config_dir = os.path.join(REPO_DIR, 'config')
    config_path = os.path.join(config_dir, file_name)
    with open(config_path) as f:
        data = yaml.load(f)
    return data


def get_config():
    people_data = get_config_file('people.yaml')['people']
    meeting_data = get_config_file('meetings.yaml')['meetings']

    config = Config()
    config.data = get_config_file('data.yaml')
    config.meetings = meeting_data
    config.people = people_data
    config.twitter_secret = get_config_file('twitter.secret.yaml')

    return config


class Config(object):

    def __init__(self):
        pass

    def get_meeting(self, label):
        return self.meetings[label]

    def get_person(self, label):
        return self.people[label]

    def get_google_client_secret_path(self):
        # Path to the client_secret.json file downloaded from the Developer Console
        scripts_dir = get_scripts_dir()
        return os.path.join(scripts_dir, 'google_client_secret.json')

    def get_twitter_consumer_creds(self):
        data = self.twitter_secret
        # The first value is the application's non-secret Consumer Key (API Key).
        # The second is the application's Consumer Secret (API Secret).
        api_key = data['twitter_consumer_api_key']
        api_secret = data['twitter_consumer_api_secret']
        return api_key, api_secret

    def get_twitter_username(self, label):
        person = self.get_person(label)
        return person['twitter_username']

    def get_twitter_user_creds(self, username):
        data = self.twitter_secret
        config = data['users'][username]
        key = config['twitter_access_token_key']
        secret = config['twitter_access_token_secret']
        return key, secret

    def get_email(self, label):
        """Return a realname, email_address 2-tuple."""
        person = self.data['people'][label]
        return person['name'], person['mail']