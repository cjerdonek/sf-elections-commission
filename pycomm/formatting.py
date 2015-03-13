
from cgi import escape as html_escape

from pycomm import common

NBSP = "&nbsp;"
TBD = "TBD"

URL_HOME = "index.aspx?page=319"
URL_MEETINGS = "index.aspx?page=1382"

EMAIL_CHOICES = ['public_notice', 'body_notice']
TWEET_CHOICES = ['meeting_posted', 'minutes_approved', 'minutes_draft', 'youtube']

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
        {file_name_prefix}_Minutes.odt
        {file_name_prefix}_Minutes.pdf


Vision CMS structure
--------------------

{date:%Y} Meetings/

    {date:%Y-%m-%d} {body_name_short}/

        {date:%Y-%m-%d} {body_name_short} Agenda
        {date:%Y-%m-%d} {body_name_short} Minutes (Draft)
        {date:%Y-%m-%d} {body_name_short} Minutes

        {date:%B {day}, %Y} {body_name_short} Agenda Packet/

            1. (for #3) Draft Minutes for April 2, 2015 BOPEC Meeting


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

HTML_YOUTUBE_FORMAT = (
    '<a href="https://www.youtube.com/watch?v={youtube_id}" '
    'target="_blank">{youtube_duration} (YT)</a>'
)

# TODO: put in "&nbsp;" if meeting is canceled, etc.
# <td headers="table_heading_2">{desc}</td>
# <td headers="table_heading_3">&nbsp;</td>
# <td headers="table_heading_4">&nbsp;</td>
# <td headers="table_heading_5">&nbsp;</td>
HTML_INDEX = """\
<tr>
    <td headers="table_heading_0">{date_full_short_day}</td>
    <td headers="table_heading_1">{body_name_index_html}</td>
    <td headers="table_heading_2">{meeting_time}</td>
    <td headers="table_heading_3">{meeting_place}</td>
    <td headers="table_heading_4">
    {agenda_link_html}
    </td>
    <td headers="table_heading_5">
    {agenda_packet_link_html}
    </td>
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
    {youtube_link_html}
    </td>
</tr>
"""

GENERAL_TEMPLATES = {
    'audio': COMMANDS_AUDIO_FORMAT,
    'files': FILES_FORMAT,
    'html_index': HTML_INDEX,
    'html_past': HTML_PAST_MEETING,
}

TWEET_CANCELLATION = """\
Next {date:%A}'s {date:%B {day}} meeting of the {body_full} will not be held: {home_page}
"""

TWEET_AGENDA_POSTED = (
    "The agenda and packet for this {date:%A}'s {date:%B {day}} "
    "{body_name_medium} meeting are now posted online: {home_page}"
)

TWEET_MINUTES_DRAFT = (
    "Draft minutes for the {date:%b. {day}, %Y} {body_name_medium} "
    "meeting are now posted online: {url_past_meetings_absolute}"
)

TWEET_MINUTES_APPROVED = (
    "The approved minutes for the {date:%b. {day}, %Y} {body_name_medium} "
    "meeting are now posted online: {url_past_meetings_absolute}"
)

TWEET_YOUTUBE = (
    "The audio for {day_reference}'s {date:%B} {date.day} {body_name_medium} "
    "meeting is now posted on YouTube ({youtube_length_text}): {youtube_url}"
)

TWEET_TEMPLATES = {
    'agenda_posted': TWEET_AGENDA_POSTED,
    'meeting_canceled': TWEET_CANCELLATION,
    'minutes_approved': TWEET_MINUTES_APPROVED,
    'minutes_draft': TWEET_MINUTES_DRAFT,
    'youtube': TWEET_YOUTUBE,
}


_EMAIL_FOOTER = """\
{signature}
San Francisco Elections Commission

Website: http://sfgov.org/electionscommission
Twitter: @SFElectionsComm

{initials}
"""

_EMAIL_PUBLIC_NOTICE_SUBJECT = """\
meeting notice: {date:%b {date.day}, %Y} {body_name_library_subject}"""

# TODO: include phone number.
# TODO: wrap paragraphs individually.
_EMAIL_PUBLIC_NOTICE_AGENDA = """\
Hello,

Attached is the agenda for the {date:%B {date.day}, %Y} meeting
of the {body_name_complete}.

The agenda and agenda packet is or will also be posted on the
Elections Commission home page:

http://sfgov.org/electionscommission

Thank you,


{email_footer}
"""

_EMAIL_PUBLIC_NOTICE_CANCELLATION = """\
Hello,

Attached is a cancellation notice for the {date:%B {date.day}, %Y} meeting
of the {body_name_complete}.

Thank you,

{email_footer}
"""

_EMAIL_BODY_SUBJECT_PREFIX = "{date.month}/{date.day}/{date.year} {body_name_short} meeting: "

_EMAIL_BODY_AGENDA_SUBJECT = _EMAIL_BODY_SUBJECT_PREFIX + "agenda now online"
_EMAIL_BODY_CANCELLATION_SUBJECT = _EMAIL_BODY_SUBJECT_PREFIX + "canceled"

_EMAIL_BODY_AGENDA = """\
Hi,

This is an FYI that the agenda and packet for next {date:%A}'s
{date:%B {date.day}, %Y} {body_name_medium} meeting are now posted online:

http://sfgov.org/electionscommission

Thanks (and please remember not to reply to all),

{email_footer}
"""

_EMAIL_BODY_CANCELLATION = """\
Hi,

This is an FYI that next {date:%A}'s {date:%B {date.day}, %Y} {body_name_medium}
meeting is canceled and will not be held:

http://sfgov.org/electionscommission

Thanks (and please remember not to reply to all),

{email_footer}
"""


EMAIL_SUBJECTS = {
    'body_notice_agenda': _EMAIL_BODY_AGENDA_SUBJECT,
    'body_notice_cancellation': _EMAIL_BODY_CANCELLATION_SUBJECT,
    'public_notice_agenda': _EMAIL_PUBLIC_NOTICE_SUBJECT,
    'public_notice_cancellation': _EMAIL_PUBLIC_NOTICE_SUBJECT,
}


EMAIL_TEMPLATES = {
    'body_notice_agenda': _EMAIL_BODY_AGENDA,
    'body_notice_cancellation': _EMAIL_BODY_CANCELLATION,
    'public_notice_agenda': _EMAIL_PUBLIC_NOTICE_AGENDA,
    'public_notice_cancellation': _EMAIL_PUBLIC_NOTICE_CANCELLATION,
}


def make_notice_template_key(config, text_label, meeting_label):
    suffix = 'cancellation' if config.is_meeting_canceled(meeting_label) else 'agenda'
    return '{0}_{1}'.format(text_label, suffix)


def get_date_full(date):
    """Return the date in the following format: "January 7, 2015"."""
    return "{0:%B {day}, %Y}".format(date, day=date.day)


def get_date_full_with_short_day(date):
    """Return the date in the following format: "Wed, January 7, 2015"."""
    return "{0:%a, %B {day}, %Y}".format(date, day=date.day)


def get_youtube_url(youtube_id):
    return "http://youtu.be/{0}".format(youtube_id)


def format_youtube_length(length):
    parts = length.split(":")
    if len(parts) == 3:
        hours = int(parts[0])
        text = "{0}:{1} hours".format(hours, parts[1])
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


def get_agenda_packet_url(agenda_packet_id):
    return "index.aspx?page=4408&parent={0}".format(agenda_packet_id)


def get_document_link_html(doc_id, text):
    # TODO: html-escape the text.
    return """\
<a href="modules/showdocument.aspx?documentid={0:d}" target="_blank">
{1}</a>""".format(doc_id, text)


def get_agenda_packet_url_html(folder_id):
    packet_url = html_escape(get_agenda_packet_url(folder_id))
    return ('<a href="{0}">Packet</a>'.format(packet_url))


def make_tweet(format_string, label):
    body, date = parse_label(label)
    return format_string.format(date=date, day=date.day, body=body,
                                home_page=WEB_SITE_HOME)
def get_cancel_tweet(label):
    format = ()
    return make_tweet(format, label)


# TODO: move these classes to config.py.
class BodyCommission(object):

    label = common.LABEL_COMMISSION
    meeting_place = "City Hall, Room 408"

    name_file_name = "Elections_Comm"
    name_index_html = "Commission"
    name_short = "Commission"
    name_medium = "Elections Commission"
    name_full = "San Francisco Elections Commission"
    name_complete = "San Francisco Elections Commission"
    name_library_subject = "SF Elections Commission"

    sender = "cjerdonek"
    public_bcc = None
    body_to = ["cjerdonek", "cjung", "dparis", "jrowe", "rsafont", "wyu",
               "jarntz", "ashen", "jwhite"]
    initials = ""
    signature = "Chris Jerdonek, President"


class BodyBOPEC(object):

    label = common.LABEL_BOPEC
    meeting_place = "City Hall, Room 421"

    name_file_name = "BOPEC"
    name_index_html = "BOPEC*"
    name_short = "BOPEC"
    name_medium = "BOPEC"
    name_full = "Budget & Oversight of Public Elections Committee (BOPEC)"
    name_complete = ("Budget & Oversight of Public Elections Committee (BOPEC) "
                     "of the San Francisco Elections Commission")
    name_library_subject = "BOPEC (SF Elections Commission)"

    sender = "commission"
    public_bcc = ["jrowe"]
    body_to = ["cjerdonek", "jarntz"]
    body_cc = ["jrowe"]
    initials = "/cjj"
    signature = ""


def get_meeting_info(config, label):
    body_classes = {
        'bopec': BodyBOPEC,
        'commission': BodyCommission,
    }

    body_label, date = common.parse_label(label)
    body_cls = body_classes[body_label]
    body = body_cls()

    data = config.get_meeting(label)

    return body, date, data


class Formatter(object):

    def __init__(self, config):
        self.config = config

    def get_meeting_kwargs(self, label):
        body, date, data = get_meeting_info(self.config, label)
        body_name_full = body.name_full
        body_name_medium = body.name_medium
        body_name_short = body.name_short
        body_label = body.label

        email_footer = _EMAIL_FOOTER.format(signature=body.signature, initials=body.initials)

        file_name_prefix = ("{date:%Y_%m_%d}_{body}".
                            format(date=date, body=body.name_file_name))

        agenda_id = data.get('agenda_id')
        # TODO: clean up the below.
        agenda_packet_id = data.get('agenda_packet_id')
        url_agenda = get_agenda_link(agenda_id)
        url_agenda_packet = get_agenda_packet_url(agenda_packet_id)

        meeting_status = data.get('status')
        meeting_time = "6:00 PM"
        meeting_place = body.meeting_place

        if meeting_status is None:
            agenda_link_html = common.indent(
                get_document_link_html(doc_id=agenda_id, text="Agenda (PDF)"))
            agenda_packet_link_html = common.indent(
                get_agenda_packet_url_html(agenda_packet_id))
        elif meeting_status == "TBD":
            agenda_link_html = TBD
            agenda_packet_link_html = NBSP
        elif meeting_status == "canceled":
            meeting_time = "Canceled: no meeting"
            meeting_place = NBSP
            agenda_link_html = NBSP
            agenda_packet_link_html = NBSP
        else:
            raise Exception("unknown status: {0}".format(meeting_status))

        # Minutes
        minutes_id = data.get('minutes_id')
        minutes_html = TBD
        if minutes_id:
            draft_prefix = 'Draft ' if data.get('minutes_draft') else ''
            text = "{0}Minutes (PDF)".format(draft_prefix)
            minutes_html = common.indent(
                get_document_link_html(doc_id=minutes_id, text=text))

        kwargs = {
            'agenda_link_html': agenda_link_html,
            'agenda_packet_link_html': agenda_packet_link_html,
            'body_name_complete': body.name_complete,
            'body_name_index_html': body.name_index_html,
            'body_name_library_subject': body.name_library_subject,
            'body_name_medium': body_name_medium,
            'body_name_short': body_name_short,
            'body_name_short_html': html_escape(body_name_short),
            'body_full': body_name_full,
            'date': date,
            'date_full_short_day': get_date_full_with_short_day(date),
            'date_full_no_day': get_date_full(date),
            'day': date.day,
            # TODO: dynamically change this: e.g. today or yesterday.
            'day_reference': "last Wednesday",
            'email_footer': email_footer,
            'file_name_prefix': file_name_prefix,
            'home_page': get_absolute_url(URL_HOME),
            'minutes_html': minutes_html,
            'meeting_place': meeting_place,
            'meeting_time': meeting_time,
            'url_agenda_html': html_escape(url_agenda),
            'url_agenda_absolute': get_absolute_url(url_agenda),
            'url_agenda_packet_html': html_escape(url_agenda_packet),
            'url_agenda_packet_absolute': get_absolute_url(url_agenda_packet),
            'url_past_meetings_absolute': get_absolute_url(URL_MEETINGS),
        }

        # YouTube
        audio_base = "{0:%Y%m%d}_{1}".format(date, body_label)
        youtube_id = data.get('youtube_id')
        if youtube_id is None:
            youtube_link_html = TBD
        else:
            youtube_length = data.get('youtube_length')
            youtube_length_text = format_youtube_length(youtube_length)
            youtube_link_html = HTML_YOUTUBE_FORMAT.format(youtube_id=youtube_id,
                                                      youtube_duration=youtube_length)
            youtube_url = get_youtube_url(youtube_id)
            kwargs.update({
                'youtube_length_text': youtube_length_text,
                'youtube_url': youtube_url,
            })
        kwargs.update({
            'audio_base': audio_base,
            'youtube_link_html': youtube_link_html,
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

    def get_email_texts(self, email_choice, meeting_label):
        email_key = make_notice_template_key(self.config, email_choice, meeting_label)

        subject_format = EMAIL_SUBJECTS[email_key]
        body_format = EMAIL_TEMPLATES[email_key]

        subject = self.format_meeting_text(subject_format, meeting_label)
        body = self.format_meeting_text(body_format, meeting_label)

        return subject, body

    def make_tweet(self, tweet_label, meeting_label):
        if tweet_label == 'meeting_posted':
            tweet_label = make_notice_template_key(self.config, tweet_label, meeting_label)

        format_str = TWEET_TEMPLATES[tweet_label]
        kwargs = self.get_meeting_kwargs(meeting_label)
        return self.get_formatted(format_str, **kwargs)
