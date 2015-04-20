
"""Exposes config data."""

import datetime
import os
import yaml

from pycomm import common


REPO_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))


def get_config_file_path(file_name):
    config_dir = os.path.join(REPO_DIR, 'config')
    return os.path.join(config_dir, file_name)


def get_config_file(file_name):
    config_path = get_config_file_path(file_name)
    with open(config_path) as f:
        data = yaml.load(f)
    return data


def get_config():
    people_data = get_config_file('people.secret.yaml')
    meeting_data = get_config_file('meetings.yaml')['meetings']

    config = Config()
    config.meetings = meeting_data
    config.people = people_data
    config.twitter_secret = get_config_file('twitter.secret.yaml')

    return config


class Config(object):

    def __init__(self):
        pass

    def get_meeting(self, label):
        try:
            return self.meetings[label]
        except KeyError:
            labels = sorted(self.meetings.keys())
            msg = "available labels:\n" + "\n".join(labels)
            print(msg)
            raise

    def is_meeting_canceled(self, label):
        data = self.get_meeting(label)
        status = data.get('status')
        return status == 'canceled'

    def get_all_meeting_labels(self):
        return sorted(self.meetings.keys())

    def get_next_meeting_label(self):
        labels = self.get_all_meeting_labels()
        today = datetime.date.today()
        for label in labels:
            body_label, date_ = common.parse_label(label)
            if date_ > today:
                return label
        raise Exception("no next meeting")

    def get_meeting_labels(self, first=0, count=1, suppress_error=False):
        """Return a list of consecutive meeting labels."""
        label = self.get_next_meeting_label()
        labels = self.get_all_meeting_labels()
        index = labels.index(label)
        labels = labels[index + first:index + count]
        if len(labels) < count and not suppress_error:
            raise Exception("config file only contains next {0} meetings: {1}"
                            .format(len(labels), ", ".join(labels)))
        return labels

    def get_entities(self, key):
        """Return a list of labels."""
        return self.people[key]

    def get_person(self, label):
        entities = self.people['entities']
        try:
            person = entities[label]
        except KeyError as err:
            raise Exception("{0} (choose from: {1})".format(err, entities.keys()))
        return person

    def get_google_client_secret_path(self):
        # Path to the client_secret.json file downloaded from the Developer Console
        return get_config_file_path('google_client.secret.json')

    def get_gmail_storage_path(self):
        return get_config_file_path('gmail.storage')

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

    def get_email_address(self, key):
        """
        Arguments:
          key: the key for the entity in the config file.
        """
        person = self.get_person(key)
        return person['mail']

    def get_email(self, value):
        """Return a realname, email_address 2-tuple."""
        # TODO: refactor this type-checking "if" logic away.
        person = self.get_person(value) if isinstance(value, str) else value
        try:
            return person['name'], person['mail']
        except:
            raise Exception("person: {0}".format(person))
