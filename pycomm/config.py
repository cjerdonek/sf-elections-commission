
"""Exposes config data."""

import datetime
import os
import yaml

from pycomm import common


REPO_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))


def read_yaml(path):
    with open(path) as f:
        data = yaml.load(f)
    return data


def get_config_file_path(file_name, dir_path=None):
    if dir_path is None:
        config_dir = os.path.join(REPO_DIR, 'config')
    else:
        config_dir = dir_path
    return os.path.join(config_dir, file_name)


def get_config_file(file_name, dir_path=None):
    config_path = get_config_file_path(file_name, dir_path=dir_path)
    data = read_yaml(config_path)
    return data


def get_config():
    people_data = get_config_file('people.secret.yaml')
    meeting_data = get_config_file('meetings.yaml', dir_path=REPO_DIR)['meetings']

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

    def get_cms_info(self, data, key):
        """
        Read a document ID from the meeting config, and return a document
        address of the form (cms_id, cms_type).
        """
        value = data.get(key)
        if not value:
            return None
        if isinstance(value, str) and (value.startswith("http:") or value.startswith("https:")):
            # Then the document ID is an URL.
            return (value, common.CMS_ID_TYPE_URL)
        try:
            try:
                prefix, cms_id = value.split("_")
            except ValueError:
                cms_id = value
                raise Exception("value: {0!r}".format(value))
            except AttributeError:
                cms_id = value
                cms_type = common.CMS_ID_TYPE_PDF
            else:
                if prefix == "page":
                    cms_type = common.CMS_ID_TYPE_PAGE
                else:
                    raise Exception("unknown prefix: {0}".format(prefix))
            cms_id = int(cms_id)
            return cms_id, cms_type
        except Exception:
            raise Exception("for key {0!r}: {1}".format(key, data))

    def is_meeting_canceled(self, label):
        data = self.get_meeting(label)
        status = data.get('status')
        return status == 'canceled'

    def get_all_meeting_labels(self):
        return sorted(self.meetings.keys())

    def get_next_meeting_label(self):
        labels = common.next_meeting_labels(count=1)
        label, = labels
        return label

    def get_meeting_labels(self, count):
        """
        Return a list of the last "count" meeting labels.
        """
        # label = self.get_next_meeting_label()
        labels = self.get_all_meeting_labels()
        labels = labels[-1 * count:]

        if len(labels) < count:
            raise Exception(f'config file only contains {len(labels)} meetings (not {count})')
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
        return get_config_file_path('google_client_1.secret.json')

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
