
import logging

from electcomm import email, tweet

if __name__ == '__main__':
    logging.basicConfig(level='INFO')
    email.main()
