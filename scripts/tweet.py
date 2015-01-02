
import os

import tweepy
import yaml


def main():
    repo_root = os.path.join(os.path.dirname(__file__), os.pardir)
    config_path = os.path.join(repo_root, 'temp.yaml')
    with open(config_path) as f:
        config = yaml.load(f)
    # The first value is the application's non-secret Consumer Key (API Key).
    # The second is the application's Consumer Secret (API Secret).
    api_key = config['twitter_consumer_api_key']
    api_secret = config['twitter_consumer_api_secret']
    auth = tweepy.OAuthHandler(api_key, api_secret)
    redirect_url = auth.get_authorization_url()
    print(redirect_url)

if __name__ == '__main__':
    main()
