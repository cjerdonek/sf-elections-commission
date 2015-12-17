
"""Common helper functions."""

from six.moves import input

from datetime import date


CMS_ID_TYPE_PAGE = 'page'
CMS_ID_TYPE_PDF = 'pdf'
CMS_ID_TYPE_URL = 'url'

LABEL_BOPEC = 'bopec'
LABEL_COMMISSION = 'commission'


def indent(text, indent='    '):
    lines = text.splitlines(True)
    lines = lines[:1] + [indent + line for line in lines[1:]]
    return "".join(lines)


def make_label(date, body_label):
    return "{0:%Y%m%d}_{1}".format(date, body_label)


def parse_label(label):
    """
    Arguments:
      label: for example: 20150107_bopec.
    """
    date_string, body_label = label.split("_")
    date_parts = date_string[:4], date_string[4:6], date_string[6:8]
    year, month, day = (int(s) for s in date_parts)
    date_ = date(year, month, day)
    return body_label, date_


def confirm(msg):
    response = input('{0}(yes/no)? '.format(msg))
    if response != 'yes':
        exit('**Aborted by user.')


def advance_days(dt, days=1):
    return date(dt.year, dt.month, dt.day + days)


def _labels_in_month(year, month):
    """Return the meeting labels for the meetings in the given month."""
    # Start at the first.
    day = date(year, month, 1)
    while day.weekday() != 2:  # Wednesday
        day = advance_days(day, 1)
    labels = [
        make_label(day, LABEL_BOPEC),
        make_label(advance_days(day, 14), LABEL_COMMISSION),
    ]
    return labels


def next_meeting_labels(count):
    today = date.today()
    year, month = today.year, today.month

    labels = []
    while len(labels) < count:
        new_labels = _labels_in_month(year, month)
        for label in new_labels:
            body_label, date_ = parse_label(label)
            if date_ > today:
                labels.append(label)
        if month == 12:
            month = 1
            year += 1
        else:
            month += 1

    return labels[:count]
