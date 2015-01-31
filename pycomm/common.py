
"""Common helper functions."""

from six.moves import input

from datetime import date


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
    dt = date(year, month, day)
    return body_label, dt


def confirm(msg):
    response = input('{0}(yes/no)? '.format(msg))
    if response != 'yes':
        exit('**Aborted by user.')


def advance_days(dt, days=1):
    return date(dt.year, dt.month, dt.day + days)


def labels_in_month(year, month):
    # Start at the first.
    day = date(year, month, 1)
    while day.weekday() != 2:  # Wednesday
        day = advance_days(day, 1)
    labels = [
        make_label(day, LABEL_BOPEC),
        make_label(advance_days(day, 14), LABEL_COMMISSION),
    ]
    return labels


def next_meeting_labels(month_count):
    today = date.today()
    year, month = today.year, today.month

    labels = []
    for i in xrange(month_count):
        current = date(year, month, 1)
        new_labels = labels_in_month(year, month)
        labels.extend(new_labels)
        month += 1

    return labels
