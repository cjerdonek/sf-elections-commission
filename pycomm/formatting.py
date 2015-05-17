
from cgi import escape as html_escape
from datetime import date, timedelta

from pycomm import common

NBSP = "&nbsp;"
TBD = "TBD"

URL_HOME = "http://sfgov.org/electionscommission"
URL_MEETINGS = "index.aspx?page=1382"

_EMAIL_TYPE_CHOICE_PARTICIPANTS = 'notify_participants'
_EMAIL_TYPE_CHOICE_PUBLIC = 'notify_public'

EMAIL_TYPE_CHOICES = [_EMAIL_TYPE_CHOICE_PARTICIPANTS, _EMAIL_TYPE_CHOICE_PUBLIC]
TWEET_CHOICES = ['meeting_posted', 'minutes_approved', 'minutes_draft', 'youtube']

FILES_FORMAT = """\
Folder structure
----------------

{date:%Y-%m-%d} {body_name_short}/

    {file_name_prefix}_Agenda.pdf
    {file_name_prefix}_Notes.txt

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

{date_full_no_day} {meeting_type_medium} Meeting (audio only)

Description
-----------

{date_full_no_day} meeting of the {body_name_complete}.

Agenda (PDF): {url_agenda_absolute}

Agenda Packet: {url_agenda_packet_absolute}

1. Call to Order & Roll Call
2. General Public Comment x:xx
3. Approval of Minutes for previous meeting
4. Commissioners' Reports
5. Director's Report
...
Adjournment


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
    <td headers="table_heading_1">{meeting_type_html}</td>
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
    <td headers="table_heading_1">{meeting_type_html}</td>
    <td headers="table_heading_2">
    {agenda_info_html}
    </td>
    <td headers="table_heading_3">
    {minutes_html}
    </td>
    <td headers="table_heading_4">
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
Next {date:%A}'s {date:%B {day}} meeting of the {body_full} will not be held: {url_home}
"""

TWEET_AGENDA_POSTED = (
    "The agenda and packet for {day_reference} {date:%B {day}} "
    "{meeting_type_medium} meeting are now posted online: {url_home}"
)

TWEET_MINUTES_DRAFT = (
    "Draft minutes for the {date:%b. {day}, %Y} {meeting_type_medium} "
    "meeting are now posted online: {url_past_meetings_absolute}"
)

TWEET_MINUTES_APPROVED = (
    "The approved minutes for the {date:%b. {day}, %Y} {meeting_type_medium} "
    "meeting are now posted online: {url_past_meetings_absolute}"
)

TWEET_YOUTUBE = (
    "The audio for {day_reference} {date:%B {day}} {meeting_type_medium} "
    "meeting is now posted on YouTube ({youtube_length_text}): {youtube_url}"
)

TWEET_TEMPLATES = {
    'meeting_posted_agenda': TWEET_AGENDA_POSTED,
    'meeting_posted_cancellation': TWEET_CANCELLATION,
    'minutes_approved': TWEET_MINUTES_APPROVED,
    'minutes_draft': TWEET_MINUTES_DRAFT,
    'youtube': TWEET_YOUTUBE,
}


_EMAIL_FOOTER = """\
{signature}
San Francisco Elections Commission

Website: {url_home}
Twitter: @SFElectionsComm
{initials}
"""

_EMAIL_FOOTER_PUBLIC = """\
Thank you,


{normal_footer}
Note: this e-mail was sent to the public distribution list for the
San Francisco Elections Commission.  If you would like to update your
e-mail address or be removed from this list, please e-mail the commission
secretary at {{commission_email}}.  Thank you.
""".format(normal_footer=_EMAIL_FOOTER)


_EMAIL_PUBLIC_SUBJECT = """\
meeting notice: {date:%b {date.day}, %Y} {body_name_library_subject}"""

# TODO: include phone number.
# TODO: wrap paragraphs individually.
_EMAIL_PUBLIC_AGENDA = """\
Hello,

Attached is the agenda for the {date:%B {date.day}, %Y} {meeting_type_adjective}meeting
of the {body_name_complete}.

The agenda and agenda packet is or will also be posted on the
Elections Commission home page:

{url_home}

{email_footer_public}
"""

_EMAIL_PUBLIC_CANCELLATION = """\
Hello,

Attached is a cancellation notice for the {date:%B {date.day}, %Y} meeting
of the {body_name_complete}.

{email_footer_public}
"""

_EMAIL_PARTICIPANTS_SUBJECT_PREFIX = "{date.month}/{date.day}/{date.year} {body_name_short} meeting: "

_EMAIL_PARTICIPANTS_AGENDA_SUBJECT = _EMAIL_PARTICIPANTS_SUBJECT_PREFIX + "agenda now online"
_EMAIL_PARTICIPANTS_CANCELLATION_SUBJECT = _EMAIL_PARTICIPANTS_SUBJECT_PREFIX + "canceled"

_EMAIL_PARTICIPANTS_AGENDA = """\
Hi,

This is an FYI that the agenda and packet for next {date:%A}'s
{date:%B {date.day}, %Y} {meeting_type_medium} meeting are now posted online:

http://sfgov.org/electionscommission

Thanks (and please remember not to reply to all),


{email_footer}
"""

_EMAIL_PARTICIPANTS_CANCELLATION = """\
Hi,

This is an FYI that next {date:%A}'s {date:%B {date.day}, %Y} {meeting_type_medium}
meeting is canceled and will not be held:

http://sfgov.org/electionscommission

Thanks (and please remember not to reply to all),


{email_footer}
"""


EMAIL_SUBJECTS = {
    'notify_participants_agenda': _EMAIL_PARTICIPANTS_AGENDA_SUBJECT,
    'notify_participants_cancellation': _EMAIL_PARTICIPANTS_CANCELLATION_SUBJECT,
    'notify_public_agenda': _EMAIL_PUBLIC_SUBJECT,
    'notify_public_cancellation': _EMAIL_PUBLIC_SUBJECT,
}


EMAIL_TEMPLATES = {
    'notify_participants_agenda': _EMAIL_PARTICIPANTS_AGENDA,
    'notify_participants_cancellation': _EMAIL_PARTICIPANTS_CANCELLATION,
    'notify_public_agenda': _EMAIL_PUBLIC_AGENDA,
    'notify_public_cancellation': _EMAIL_PUBLIC_CANCELLATION,
}


class EmailChoiceEnum(object):

    notify_participants = _EMAIL_TYPE_CHOICE_PARTICIPANTS
    notify_public = _EMAIL_TYPE_CHOICE_PUBLIC


def make_notice_template_key(config, text_label, meeting_label):
    suffix = 'cancellation' if config.is_meeting_canceled(meeting_label) else 'agenda'
    return '{0}_{1}'.format(text_label, suffix)


# TODO: generalize this to work with a day of the week other than Wednesday.
def make_day_reference(meeting_date):
    """For example, return "today", "yesterday", "this past Wednesday", etc.

    The return value is used in text like the following:

        The agenda and packet for *****'s April 15 Comission meeting...."

    """
    meeting_day_name = meeting_date.strftime("%A")
    days_after_sunday = meeting_date.weekday() + 1
    sunday_before = meeting_date - timedelta(days=days_after_sunday)
    saturday_after = sunday_before + timedelta(days=6)
    today = date.today()
    days_away = (meeting_date - today).days
    if days_away == 0:
        text = "today's"
    elif days_away == -1:
        text = "yesterday's"
    elif sunday_before <= today < meeting_date:
        text = "this {0}'s".format(meeting_day_name)
    elif saturday_after <= today <= saturday_after + timedelta(days=5):
        text = "last week's".format(meeting_day_name)
    elif 5 <= days_away <= 7:
        # Wednesday through Friday of previous week.
        text = "next {0}'s".format(meeting_day_name)
    elif days_away > 7:
        text = "the upcoming"
    elif days_away < -7:
        text = "the previous"
    else:
        raise Exception("unhandled day reference: {0} days".format(days_away))
    return text


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
        hours = int(parts.pop(0))
    else:
        hours = None

    mins = int(parts[0]) + 1.0 * int(parts[1]) / 60
    mins = round(mins)

    if hours is not None:
        text = "{0}:{1} hours".format(hours, mins)
        if hours > 1:
            text += "s"
    elif len(parts) == 2:
        text = "{0} mins".format(mins)
    else:
        raise Exception("bad length: {0!r}".format(length))
    return text


def get_absolute_url(rel_url):
    if rel_url is None:
        return None
    return "http://www.sfgov2.org/{0}".format(rel_url)


def get_agenda_url(agenda_id):
    return "modules/showdocument.aspx?documentid={0}".format(agenda_id)


def get_agenda_packet_url(agenda_packet_id):
    if agenda_packet_id is None:
        return None
    return "index.aspx?page=4408&parent={0}".format(agenda_packet_id)


def get_document_link_html(doc_id, text):
    # TODO: html-escape the text.
    return """\
<a href="modules/showdocument.aspx?documentid={0:d}" target="_blank">
{1}</a>""".format(doc_id, text)


def get_agenda_packet_url_html(agenda_packet_id):
    packet_url = get_agenda_packet_url(agenda_packet_id)
    packet_url = html_escape(packet_url)
    return ('<a href="{0}">Packet</a>'.format(packet_url))


def get_agenda_info_html(agenda_url, agenda_packet_id):
    if agenda_packet_id is None:
        packet_info = "No Packet"
    else:
        packet_info = get_agenda_packet_url_html(agenda_packet_id)
    return """\
<a href="{agenda_url}" target="_blank">
Agenda (PDF)</a> |
{packet_info}""".format(agenda_url=agenda_url, packet_info=packet_info)


# TODO: move these classes to config.py.
class BodyCommission(object):

    label = common.LABEL_COMMISSION
    meeting_place = "City Hall, Room 408"

    name_file_name = "Elections_Comm"
    name_web = "Commission"
    name_short = "Commission"
    name_medium = "Elections Commission"
    name_full = "San Francisco Elections Commission"
    name_complete = "San Francisco Elections Commission"
    name_library_subject = "SF Elections Commission"

    sender = "cjerdonek"
    public_bcc = None
    body_to = ["cjung", "dparis", "jrowe", "rsafont", "wyu",
               "jarntz", "ashen", "jwhite"]
    body_cc = []
    initials = ""
    signature = "Chris Jerdonek, President"


class BodyBOPEC(object):

    label = common.LABEL_BOPEC
    meeting_place = "City Hall, Room 421"

    name_file_name = "BOPEC"
    name_web = "BOPEC*"
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
        config = self.config
        body, date, data = get_meeting_info(config, label)
        body_name_full = body.name_full
        meeting_type_medium = body.name_medium
        body_name_short = body.name_short
        body_label = body.label

        email_footer = _EMAIL_FOOTER.format(signature=body.signature,
                                            initials=body.initials,
                                            url_home=URL_HOME)
        commission_email = config.get_email_address('commission')
        email_footer_public = _EMAIL_FOOTER_PUBLIC.format(signature=body.signature,
                                            initials=body.initials,
                                            commission_email=commission_email,
                                            url_home=URL_HOME)

        file_name_prefix = ("{date:%Y_%m_%d}_{body}".
                            format(date=date, body=body.name_file_name))

        meeting_type_adjective = data.get('type')
        meeting_type = body.name_web
        if meeting_type_adjective:
            meeting_type = "{0} ({1})".format(meeting_type, meeting_type_adjective)
            meeting_type_medium = "{0} {1}".format(meeting_type_adjective, meeting_type_medium)
        meeting_status = data.get('status', 'posted')
        meeting_time = data.get('time', "6:00 PM")
        meeting_place = data.get('place', body.meeting_place)

        # TODO: simplify and DRY up this if logic more.
        agenda_info_html = None
        agenda_packet_link_html = NBSP
        agenda_url_absolute = None
        agenda_packet_url_absolute = None
        minutes_html = TBD
        youtube_link_html = TBD
        if meeting_status == 'posted':
            agenda_id = int(data.get('agenda_id'))
            agenda_packet_id = data.get('agenda_packet_id')
            agenda_url = get_agenda_url(agenda_id)
            agenda_url_absolute = get_absolute_url(agenda_url)
            agenda_packet_url = get_agenda_packet_url(agenda_packet_id)
            agenda_packet_url_absolute = get_absolute_url(agenda_packet_url)
            agenda_link_html = common.indent(
                get_document_link_html(doc_id=agenda_id, text="Agenda (PDF)"))
            if agenda_packet_id is None:
                agenda_packet_link_html = "None"
            else:
                agenda_packet_link_html = common.indent(get_agenda_packet_url_html(agenda_packet_id))
            agenda_info_html = common.indent(get_agenda_info_html(agenda_url, agenda_packet_id))
        elif meeting_status == "TBD":
            agenda_link_html = TBD
        elif meeting_status == "canceled":
            meeting_time = "Canceled: no meeting"
            meeting_place = NBSP
            agenda_info_html = "No meeting"
            agenda_link_html = NBSP
            agenda_packet_link_html = NBSP
            minutes_html = NBSP
            youtube_link_html = NBSP
        else:
            raise Exception("unknown status: {0}".format(meeting_status))

        # Minutes
        minutes_id = data.get('minutes_id')
        if minutes_id:
            minutes_id = int(minutes_id)
            draft_prefix = 'Draft ' if data.get('minutes_draft') else ''
            text = "{0}Minutes (PDF)".format(draft_prefix)
            minutes_html = common.indent(get_document_link_html(doc_id=minutes_id, text=text))

        kwargs = {
            'agenda_info_html': agenda_info_html,
            'agenda_link_html': agenda_link_html,
            'agenda_packet_link_html': agenda_packet_link_html,
            'body_name_complete': body.name_complete,
            'body_name_library_subject': body.name_library_subject,
            'body_name_short': body_name_short,
            'body_full': body_name_full,
            'date': date,
            'date_full_short_day': get_date_full_with_short_day(date),
            'date_full_no_day': get_date_full(date),
            'day': date.day,
            'day_reference': make_day_reference(date),
            'email_footer': email_footer,
            'email_footer_public': email_footer_public,
            'file_name_prefix': file_name_prefix,
            'minutes_html': minutes_html,
            'meeting_place': meeting_place,
            'meeting_time': meeting_time,
            'meeting_type_adjective': ("{0} ".format(meeting_type_adjective) if
                                       meeting_type_adjective else ""),
            'meeting_type_medium': meeting_type_medium,
            'meeting_type_html': html_escape(meeting_type),
            'url_agenda_absolute': agenda_url_absolute,
            'url_agenda_packet_absolute': agenda_packet_url_absolute,
            'url_home': URL_HOME,
            'url_past_meetings_absolute': get_absolute_url(URL_MEETINGS),
        }

        # YouTube
        audio_base = "{0:%Y%m%d}_{1}".format(date, body_label)
        youtube_id = data.get('youtube_id')
        if youtube_id:
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
