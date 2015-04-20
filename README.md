SF Elections Commission
=======================

**Disclaimer:** This repository is a personal and unofficial collection
of documents to assist with administrative tasks.  These documents are
not approved by nor do they represent the views of the City and County
of San Francisco nor the San Francisco Elections Commission.

This repository contains--

* [Backup files](web) for some pages of the Commission web site (maintained
  using San Francisco government's [Vision CMS][vision-cms]), and
* [Instructional documents](docs/index.md) for administrative tasks like
  holding a meeting and recording and posting meeting audio.


Python Setup
------------

We need to use Python 2.7 since `google-api-python-client` doesn't
yet support Python 3: https://github.com/google/google-api-python-client/issues/3

    $ pip install google-api-python-client httplib2 pyyaml tweepy
    $ python scripts/admin.py -h


Technical Note
--------------

To preview a file in HTML, you can run the following command, for example:

    $ pandoc --from=markdown_github --to=html --output=PATH.html PATH.md


[vision-cms]: http://www6.sfgov.org/index.aspx?page=163
