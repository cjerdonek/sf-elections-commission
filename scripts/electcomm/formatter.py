
from cgi import escape as html_escape

from electcomm.common import parse_label

# For example: "Wed, January 7, 2015".
DATE_FORMAT_SHORT = "{date_short:%a, %B {day}, %Y}"

INDEX_HTML = """\
<tr>
    <td headers="table_heading_0">{date_format}</td>
    <td headers="table_heading_1">{{body_short_html}}</td>
    <td headers="table_heading_2">{{desc}}</td>
    <td headers="table_heading_3">&nbsp;</td>
    <td headers="table_heading_4">&nbsp;</td>
    <td headers="table_heading_5">&nbsp;</td>
</tr>
""".format(date_format=DATE_FORMAT_SHORT)

NAME_BOPEC = "Budget & Oversight of Public Elections Committee (BOPEC)"
NAME_COMMISSION = "Elections Commission"
WEB_SITE_HOME = "http://www.sfgov2.org/index.aspx?page=319"
WEB_SITE_MEETINGS = "http://www.sfgov2.org/index.aspx?page=1382"

BODY_NAMES = {'bopec': NAME_BOPEC, 'commission': NAME_COMMISSION}

def make_tweet(format_string, label):
    body, date = parse_label(label)
    return format_string.format(date=date, day=date.day, body=body,
                                home_page=WEB_SITE_HOME)
def get_cancel_tweet(label):
    format = ("The {0} meeting of the {{body}} will not be held: {{home_page}}"
              .format("{date:%a, %B {day}, %Y}"))
    return make_tweet(format, label)


class BodyCommission(object):

    short_name = "Commission"
    full_name = "San Francisco Elections Commission"


class BodyBOPEC(object):

    short_name = "BOPEC"
    full_name = "Budget & Oversight of Public Elections Committee (BOPEC)"


class Formatter(object):

    def __init__(self, label):
        body_label, date = parse_label(label)

        body_classes = {
            'bopec': BodyBOPEC,
            'commission': BodyCommission,
        }

        body_cls = body_classes[body_label]
        self.body = body_cls()
        self.date = date

    def get_format_kwargs(self):
        body_short_name = self.body.short_name
        return {
            'body_short': body_short_name,
            'body_short_html': html_escape(body_short_name),
            'date_short': self.date,
            'day': self.date.day,
        }

    def get_formatted(self, format_str, **extra):
        kwargs = self.get_format_kwargs()
        kwargs.update(extra)
        return format_str.format(**kwargs)

    def make_html_index_announce(self):
        # Read canceled from YAML.
        desc = 'Canceled: no meeting'
        return self.get_formatted(INDEX_HTML, desc=desc)
