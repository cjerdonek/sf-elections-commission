
from __future__ import absolute_import

import logging

from electcomm import email, tweet
from electcomm.formatter import Formatter


if __name__ == '__main__':
    logging.basicConfig(level='INFO')
    f = Formatter('2015_01_07_bopec')
    print(f.make_html_index_announce())
