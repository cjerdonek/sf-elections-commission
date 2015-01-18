
"""Common helper functions."""

from six.moves import input

from datetime import date


def indent(text, indent='    '):
    lines = text.splitlines(True)
    lines = lines[:1] + [indent + line for line in lines[1:]]
    return "".join(lines)

def parse_label(label):
    """
    Arguments:
      label: for example: 2015_01_07_bopec.
    """
    parts = label.split("_")
    body_label = parts.pop()
    year, month, day = (int(s) for s in parts)
    dt = date(year, month, day)
    return body_label, dt


def confirm(msg):
    response = input('{0}(yes/no)? '.format(msg))
    if response != 'yes':
        exit('**Aborted by user.')
