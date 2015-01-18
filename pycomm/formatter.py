
from cgi import escape as html_escape

from pycomm import common
from pycomm.common import parse_label

# For example: "Wed, January 7, 2015".
DATE_FORMAT_SHORT = "{date:%a, %B {day}, %Y}"

HTML_MINUTES = (
    '<a href="modules/showdocument.aspx?documentid={minutes_id}" target="_blank">\n'
    '{draft_prefix}Minutes (PDF)</a>'
)

HTML_YOUTUBE_FORMAT = (
    '<a href="https://www.youtube.com/watch?v={youtube_id}" '
    'target="_blank">{youtube_duration} (YT)</a>'
)

INDEX_HTML = """\
<tr>
    <td headers="table_heading_0">{date_short}</td>
    <td headers="table_heading_1">{{body_short_html}}</td>
    <td headers="table_heading_2">{{desc}}</td>
    <td headers="table_heading_3">&nbsp;</td>
    <td headers="table_heading_4">&nbsp;</td>
    <td headers="table_heading_5">&nbsp;</td>
</tr>
""".format(date_short=DATE_FORMAT_SHORT)

HTML_PAST_MEETING = """\
<tr>
    <td headers="table_heading_0">{date_short}</td>
    <td headers="table_heading_1">{{body_short_html}}</td>
    <td headers="table_heading_2">
    <a href="modules/showdocument.aspx?documentid={{agenda_id}}" target="_blank">
    Agenda (PDF)</a> |
    <a href="index.aspx?page=4408&amp;parent={{agenda_packet_id}}">Packet</a>
    </td>
    <td headers="table_heading_4">
    {{minutes_html}}
    </td>
    <td headers="table_heading_5">
    {{youtube_html}}
    </td>
</tr>
""".format(date_short=DATE_FORMAT_SHORT)

TWEET_CANCEL = """\
The {date_short} meeting of the {{body_full}} will not be held: {{home_page}}
""".format(date_short=DATE_FORMAT_SHORT)

TWEET_AGENDA_POSTED = (
    "The agenda and packet for this {date:%A}'s "
    "{date:%B {day}} {body_name_medium} meeting are now posted: {home_page}"
)

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
    format = ()
    return make_tweet(format, label)


class BodyCommission(object):

    name_full = "San Francisco Elections Commission"
    name_medium = "Elections Commission"
    name_short = "Commission"


class BodyBOPEC(object):

    name_short = "BOPEC"
    name_full = "Budget & Oversight of Public Elections Committee (BOPEC)"


def parse_meeting_label(label):
    body_label, date = parse_label(label)

    body_classes = {
        'bopec': BodyBOPEC,
        'commission': BodyCommission,
    }

    body_cls = body_classes[body_label]
    body = body_cls()

    return body, date


class Formatter(object):

    def __init__(self, config):
        self.config = config

    def get_meeting_kwargs(self, label):
        data = self.config.get_meeting(label)
        body, date = parse_meeting_label(label)
        body_name_full = body.name_full
        body_name_medium = body.name_medium
        body_name_short = body.name_short

        # Minutes
        minutes_id = data['minutes_id']
        if minutes_id:
            draft_prefix = 'Draft ' if data['minutes_draft'] else ''
            minutes_html = common.indent(HTML_MINUTES.format(
                                minutes_id=minutes_id,
                                draft_prefix=draft_prefix))

        # YouTube
        youtube_id = data['youtube_id']
        youtube_duration = data['youtube_duration']
        youtube_html = HTML_YOUTUBE_FORMAT.format(youtube_id=youtube_id,
                                                  youtube_duration=youtube_duration)

        return {
            'agenda_id': data['agenda_id'],
            'agenda_packet_id': data['agenda_packet_id'],
            'body_name_medium': body_name_medium,
            'body_short': body_name_short,
            'body_short_html': html_escape(body_name_short),
            'body_full': body_name_full,
            'date': date,
            'day': date.day,
            'home_page': WEB_SITE_HOME,
            'minutes_html': minutes_html,
            'youtube_html': youtube_html,
        }

    def get_formatted(self, format_str, **kwargs):
        print(kwargs)
        return format_str.format(**kwargs)

    def get_meeting_formatted(self, format_str, meeting_label):
        kwargs = self.get_meeting_kwargs(meeting_label)
        return self.get_formatted(format_str, **kwargs)

    def make_html_index_announce(self):
        # Read canceled from YAML.
        desc = 'Canceled: no meeting'
        return self.get_formatted(INDEX_HTML, desc=desc)

    def make_html_past_meeting(self, label):
        return self.get_meeting_formatted(HTML_PAST_MEETING, label)

    def make_tweet_announce(self, label):
        return self.get_meeting_formatted(TWEET_CANCEL, label)

    def make_tweet_agenda_posted(self, label):
        return self.get_meeting_formatted(TWEET_AGENDA_POSTED, label)
