
from cgi import escape as html_escape

from pycomm import common


URL_HOME = "index.aspx?page=319"
URL_MEETINGS = "index.aspx?page=1382"

FILES_FORMAT = """\
Folder structure
----------------

{date:%Y-%m-%d} {body_name_short}/

    {file_name_prefix}_Agenda.pdf

    Agenda Packet/

        2014-09-03_BOPEC_Minutes_Draft.pdf

    Agenda Prep/

        {file_name_prefix}_Agenda.odt

    Minutes/

        {file_name_prefix}_Minutes_Draft.odt
        {file_name_prefix}_Minutes_Draft.pdf


Vision CMS structure
--------------------

{date:%Y} Meetings/

    {date:%Y-%m-%d} {body_name_short}/

        {date:%Y-%m-%d} {body_name_short} Agenda

        {date:%B {day}, %Y} {body_name_short} Agenda Packet/

            For #3: Draft Minutes for April 2, 2014 BOPEC Meeting


"""

COMMANDS_AUDIO_FORMAT = """\
Commands
========

Concatenate audio:

ffmpeg -i concat:"part1.mp3|part2.mp3" -acodec copy {audio_base}.mp3

Generate video:

ffmpeg -i {audio_base}.mp3 -f image2 -loop 1 -r 2 -i {audio_base}_thumb.png \\
    -shortest -c:a copy -c:v libx264 -crf 23 -preset veryfast \\
    -movflags faststart {audio_base}.mp4

ffmpeg -i {audio_base}.mp4 -acodec copy -vcodec copy {audio_base}.mkv


YouTube Info
============

Title
-----

{date_full_no_day} {body_name_medium} Meeting (audio only)

Description
-----------

{date_full_no_day} meeting of the {body_name_complete}.

Agenda (PDF): {url_agenda_absolute}

Agenda Packet: {url_agenda_packet_absolute}

Tags
----

San Francisco Elections Commission, San Francisco (US County),
County Commission (Organization Type),
Elections Commission (Organization Type), Elections Commission,
Elections, Meeting

Video Location
--------------

37.77932 -122.41914

"""

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
    <td headers="table_heading_1">{{body_name_short_html}}</td>
    <td headers="table_heading_2">{{desc}}</td>
    <td headers="table_heading_3">&nbsp;</td>
    <td headers="table_heading_4">&nbsp;</td>
    <td headers="table_heading_5">&nbsp;</td>
</tr>
"""

HTML_PAST_MEETING = """\
<tr>
    <td headers="table_heading_0">{date_full_short_day}</td>
    <td headers="table_heading_1">{body_name_short_html}</td>
    <td headers="table_heading_2">
    <a href="{url_agenda_html}" target="_blank">
    Agenda (PDF)</a> |
    <a href="{url_agenda_packet_html}">Packet</a>
    </td>
    <td headers="table_heading_4">
    {minutes_html}
    </td>
    <td headers="table_heading_5">
    {youtube_html}
    </td>
</tr>
"""

GENERAL_TEMPLATES = {
    'audio': COMMANDS_AUDIO_FORMAT,
    'files': FILES_FORMAT,
    'html_past': HTML_PAST_MEETING,
}

TWEET_CANCEL = """\
The {date_short} meeting of the {body_full} will not be held: {home_page}
"""

TWEET_AGENDA_POSTED = (
    "The agenda and packet for this {date:%A}'s "
    "{date:%B {day}} {body_name_medium} meeting are now posted: {home_page}"
)

TWEET_MINUTES_APPROVED = (
    "The approved minutes for the {date:%b. {day}, %Y} {body_name_medium} "
    "meeting are now posted: {url_past_meetings_absolute}"
)

TWEET_YOUTUBE = (
    "The audio for last {date:%A}'s {date:%B} {day} {body_name_medium} "
    "meeting is now posted on YouTube ({youtube_length_text}): {youtube_url}"
)

EMAIL_LIBRARY = """\
foo
"""

EMAIL_LIBRARY_SUBJECT = """\
meeting notice: {date:%b {day}, %Y} {body_name_library_subject}"""

EMAIL_TEMPLATES = {
    'notify_body': EMAIL_LIBRARY,
    'notify_library': EMAIL_LIBRARY,
}

EMAIL_SUBJECTS = {
    'notify_body': EMAIL_LIBRARY,
    'notify_library': EMAIL_LIBRARY_SUBJECT,
}

TWEET_TEMPLATES = {
    'minutes_approved': TWEET_MINUTES_APPROVED,
    'youtube': TWEET_YOUTUBE,
}

def get_date_full(date):
    """Return the date in the following format: "January 7, 2015"."""
    return "{0:%B {day}, %Y}".format(date, day=date.day)

def get_date_full_short_day(date):
    """Return the date in the following format: "Wed, January 7, 2015"."""
    return "{0:%a, %B {day}, %Y}".format(date, day=date.day)


def get_youtube_url(youtube_id):
    return "http://youtu.be/{0}".format(youtube_id)


def format_youtube_length(length):
    parts = length.split(":")
    if len(parts) == 3:
        hours = int(parts[0])
        text = "{0}:{1} hour".format(hours, parts[1])
        if hours > 1:
            text += "s"
    elif len(parts) == 2:
        text = "{0} mins".format(parts[0])
    else:
        raise Exception("bad length: {0}".format(length))
    return text


def get_absolute_url(rel_url):
    return "http://www.sfgov2.org/{0}".format(rel_url)


def get_agenda_link(agenda_id):
    return "modules/showdocument.aspx?documentid={0}".format(agenda_id)


def get_agenda_packet_link(agenda_packet_id):
    return "index.aspx?page=4408&parent={0}".format(agenda_packet_id)


def make_tweet(format_string, label):
    body, date = parse_label(label)
    return format_string.format(date=date, day=date.day, body=body,
                                home_page=WEB_SITE_HOME)
def get_cancel_tweet(label):
    format = ()
    return make_tweet(format, label)


class BodyCommission(object):

    label = common.LABEL_COMMISSION
    name_file_name = "Elections_Comm"
    name_short = "Commission"
    name_medium = "SF Elections Commission"
    name_full = "San Francisco Elections Commission"
    name_complete = "San Francisco Elections Commission"


class BodyBOPEC(object):

    label = common.LABEL_BOPEC
    name_file_name = "BOPEC"
    name_library_subject = "BOPEC (SF Elections Commission)"
    name_short = "BOPEC"
    name_medium = "BOPEC"
    name_full = "Budget & Oversight of Public Elections Committee (BOPEC)"
    name_complete = ("Budget & Oversight of Public Elections Committee (BOPEC) "
                     "of the San Francisco Elections Commission")


def get_meeting_info(label):
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
        body, date = get_meeting_info(label)
        body_name_full = body.name_full
        body_name_medium = body.name_medium
        body_name_short = body.name_short
        body_label = body.label
        file_name_prefix = ("{date:%Y_%m_%d}_{body}".
                            format(date=date, body=body.name_file_name))

        agenda_id = data.get('agenda_id')
        agenda_packet_id = data.get('agenda_packet_id')
        url_agenda = get_agenda_link(agenda_id)
        url_agenda_packet = get_agenda_packet_link(agenda_packet_id)

        # Minutes
        minutes_id = data.get('minutes_id')
        minutes_html = "TBA"
        if minutes_id:
            draft_prefix = 'Draft ' if data['minutes_draft'] else ''
            minutes_html = common.indent(HTML_MINUTES.format(
                                minutes_id=minutes_id,
                                draft_prefix=draft_prefix))

        kwargs = {
            'body_name_complete': body.name_complete,
            'body_name_library_subject': body.name_library_subject,
            'body_name_medium': body_name_medium,
            'body_name_short': body_name_short,
            'body_name_short_html': html_escape(body_name_short),
            'body_full': body_name_full,
            'date': date,
            'date_full_short_day': get_date_full_short_day(date),
            'date_full_no_day': get_date_full(date),
            'day': date.day,
            'file_name_prefix': file_name_prefix,
            'home_page': get_absolute_url(URL_HOME),
            'minutes_html': minutes_html,
            'url_agenda_html': html_escape(url_agenda),
            'url_agenda_absolute': get_absolute_url(url_agenda),
            'url_agenda_packet_html': html_escape(url_agenda_packet),
            'url_agenda_packet_absolute': get_absolute_url(url_agenda_packet),
            'url_past_meetings_absolute': get_absolute_url(URL_MEETINGS),
        }

        # YouTube
        youtube_id = data.get('youtube_id')
        if youtube_id is not None:
            audio_base = "{0:%Y%m%d}_{1}".format(date, body_label)
            youtube_length = data.get('youtube_length')
            youtube_length_text = format_youtube_length(youtube_length)
            youtube_html = HTML_YOUTUBE_FORMAT.format(youtube_id=youtube_id,
                                                      youtube_duration=youtube_length)
            youtube_url = get_youtube_url(youtube_id)
            kwargs.update({
                'audio_base': audio_base,
                'youtube_html': youtube_html,
                'youtube_length_text': youtube_length_text,
                'youtube_url': youtube_url,
            })

        return kwargs

    def get_formatted(self, format_str, **kwargs):
        try:
            formatted = format_str.format(**kwargs)
        except KeyError:
            # TODO: include more info.
            raise
        return formatted

    def format_meeting_text(self, format_str, meeting_label):
        kwargs = self.get_meeting_kwargs(meeting_label)
        return self.get_formatted(format_str, **kwargs)

    def get_meeting_text(self, template_label, meeting_label):
        format_str = GENERAL_TEMPLATES[template_label]
        return self.format_meeting_text(format_str, meeting_label)

    def make_tweet(self, template_label, meeting_label):
        format_str = TWEET_TEMPLATES[template_label]
        kwargs = self.get_meeting_kwargs(meeting_label)
        return self.get_formatted(format_str, **kwargs)

    def make_html_index_announce(self):
        # Read canceled from YAML.
        desc = 'Canceled: no meeting'
        return self.get_formatted(INDEX_HTML, desc=desc)

    def make_html_past_meeting(self, label):
        return self.format_meeting_text(HTML_PAST_MEETING, label)

    def make_tweet_announce(self, label):
        return self.format_meeting_text(TWEET_CANCEL, label)

    def make_tweet_agenda_posted(self, label):
        return self.format_meeting_text(TWEET_AGENDA_POSTED, label)
