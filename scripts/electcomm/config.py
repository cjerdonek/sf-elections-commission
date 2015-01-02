
"""Exposes config data."""

import os
import yaml


def get_config():
    scripts_dir = os.path.join(os.path.dirname(__file__), os.pardir)
    config_path = os.path.join(scripts_dir, 'data.yaml')
    with open(config_path) as f:
        data = yaml.load(f)
    return Config(data)


class Config(object):

    def __init__(self, data):
        self.data = data

    def get_email(self, label):
        """Return a realname, email_address 2-tuple."""
        person = self.data['people'][label]
        return person['name'], person['mail']
