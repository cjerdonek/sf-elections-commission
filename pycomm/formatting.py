
from html import escape as html_escape
from datetime import date, timedelta
import logging
from pprint import pprint
from textwrap import dedent

from pycomm import common


_log = logging.getLogger(__name__)

NBSP = "&nbsp;"
TBD_HTML = "TBD"
TBD_NEW_DOCS = """TBD / <a href="index.aspx?page=4408&amp;parent=2911">New Docs</a>"""

URL_HOME = "http://sfgov.org/electionscommission"
URL_MEETINGS = "meetings"

_EMAIL_TYPE_CHOICE_PARTICIPANTS = 'notify_participants'
_EMAIL_TYPE_CHOICE_PUBLIC = 'notify_public'

EMAIL_TYPE_CHOICES = [_EMAIL_TYPE_CHOICE_PARTICIPANTS, _EMAIL_TYPE_CHOICE_PUBLIC]
TWEET_CHOICES = ['meeting_posted', 'minutes_approved', 'minutes_draft', 'youtube']

DATE_FORMAT_SHORT = "{date:%b {day}, %Y}"

FILES_FORMAT = """\
Folder structure
----------------

{date:%Y-%m-%d} {body_name_short}/

    {file_name_prefix}_Agenda.pdf
    {file_name_prefix}_Notes.txt

    Agenda Packet/

        {file_name_prefix}_CMS_Index.txt
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

{youtube_agenda_link}

{youtube_agenda_packet_link}

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

HTML_INDEX = """\
<tr>
	<td headers="table_heading_0">Wed, February 3, 2016</td>
	<td headers="table_heading_1">BOPEC</td>
	<td headers="table_heading_2">6:00 PM</td>
	<td headers="table_heading_3">City Hall, Room 421</td>
	<td headers="table_heading_4">[[{"fid":"261","view_mode":"default","fields":{"format":"default"},"type":"media","attributes":{"class":"file media-element file-default"},"link_text":"Agenda"}]]</td>
	<td headers="table_heading_5"><a href="/electionscommission/bopec-agenda-packet-february-3-2016">Packet</a></td>
</tr>
"""

# TODO: put in "&nbsp;" if meeting is canceled, etc.
# <td headers="table_heading_2">{desc}</td>
# <td headers="table_heading_3">&nbsp;</td>
# <td headers="table_heading_4">&nbsp;</td>
# <td headers="table_heading_5">&nbsp;</td>
HTML_INDEX_OLD = """\
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
<tr{tr_class}>
    <td headers="table_heading_0">{date_full_short_day}</td>
    <td headers="table_heading_1">{meeting_type_html}</td>
    <td headers="table_heading_2">
    {agenda_links_html}
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
{day_reference} {date:%b {day}} meeting of the {body_full} will not be held: {url_home}
"""

TWEET_AGENDA_POSTED = (
    "The agenda and packet for {day_reference} {date:%B {day}} "
    "{meeting_type_medium} meeting are now posted online: {url_home}"
)

TWEET_MINUTES_DRAFT = (
    "Draft minutes for the {date_format} {{meeting_type_medium}} "
    "meeting are now posted online: {{url_past_meetings_absolute}}"
    .format(date_format=DATE_FORMAT_SHORT)
)

TWEET_MINUTES_APPROVED = (
    "The approved minutes for the {date_format} {{meeting_type_medium}} "
    "meeting are now posted online: {{url_past_meetings_absolute}}"
    .format(date_format=DATE_FORMAT_SHORT)
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


def make_day_reference(meeting_date):
    """For example, return "today", "yesterday", "this past Wednesday", etc.

    The return value is used in text like the following:

        The agenda and packet for ***** April 15 Comission meeting...."

    """
    meeting_day_name = meeting_date.strftime("%A")
    days_after_saturday = meeting_date.weekday() + 2
    saturday_before = meeting_date - timedelta(days=days_after_saturday)
    sunday_before = saturday_before + timedelta(days=1)
    wednesday_before = saturday_before - timedelta(days=3)
    saturday_after = saturday_before + timedelta(days=7)
    today = date.today()
    days_away = (meeting_date - today).days
    # The time clauses below are organized by the date of the meeting
    # in reverse chronological order.
    if wednesday_before <= today <= saturday_before:
        # Wednesday through Saturday of previous week.
        text = "next {0}'s".format(meeting_day_name)
    elif today < saturday_before:
        text = "the upcoming"
    elif sunday_before <= today < meeting_date:
        text = "this {0}'s".format(meeting_day_name)
    elif today == meeting_date:
        text = "today's"
    elif today == meeting_date + timedelta(days=1):
        text = "yesterday's"
    elif meeting_date < today <= saturday_after:
        text = "this past {0}'s".format(meeting_day_name)
    elif saturday_after <= today <= saturday_after + timedelta(days=5):
        text = "last week's".format(meeting_day_name)
    else:
        text = "the previous"
    return text


def get_date_full(date):
    """Return the date in the following format: "January 7, 2015"."""
    return "{0:%B {day}, %Y}".format(date, day=date.day)


def get_date_full_with_short_day(date):
    """Return the date in the following format: "Wed, January 7, 2015"."""
    return "{0:%a, %B {day}, %Y}".format(date, day=date.day)


def get_url_youtube(youtube_id):
    return "https://www.youtube.com/watch?v={0}".format(youtube_id)


def get_url_youtube_short(youtube_id):
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
        hour_suffix = "s" if hours > 1 else ""
        text = "{0} hr{1} {2} mins".format(hours, hour_suffix, mins)
    elif len(parts) == 2:
        text = "{0} mins".format(mins)
    else:
        raise Exception("bad length: {0!r}".format(length))
    return text


def get_absolute_url(rel_url):
    if rel_url is None:
        return None
    return "https://sfgov.org/electionscommission/{0}".format(rel_url)


def get_document_url(doc_id):
    doc_id = int(doc_id)
    return "modules/showdocument.aspx?documentid={0:d}".format(doc_id)


def get_page_url(page_id, parent_id=None):
    extra = "" if parent_id is None else "&parent={0}".format(parent_id)
    url = "index.aspx?page={0}{extra}".format(page_id, extra=extra)
    return url


def get_agenda_packet_url(agenda_packet_id):
    if agenda_packet_id is None:
        return None
    return get_page_url(4408, parent_id=agenda_packet_id)


def format_text_link(url, text):
    """Return link in text form (e.g. for YouTube).

    For example, returns "Agenda (PDF): http://...".
    """
    return "{0}: {1}".format(text, url)


def get_link_info(doc_address, text, absolute=False):
    if doc_address is None:
        return None
    doc_id, doc_id_type = doc_address
    if doc_id_type == 'url':
        url = doc_id
    elif doc_id_type == 'pdf':
        url = get_document_url(doc_id=doc_id)
        text = "{text} ({doc_id_type})".format(text=text, doc_id_type='PDF')
    elif doc_id_type == 'page':
        url = get_page_url(page_id=doc_id)
    else:
        raise Exception("unknown type: {0}".format(doc_id_type))
    if absolute:
        url = get_absolute_url(url)
    return url, text, doc_id_type


def get_agenda_packet_link_info(packet_id, absolute=False):
    text = "Packet"
    url = get_agenda_packet_url(packet_id)
    if absolute:
        url = get_absolute_url(url)

    return text, url


def make_text_link(cms_info, text, absolute=False):
    """Return link in text form (e.g. for YouTube).

    For example, returns "Agenda (PDF): http://...".
    """
    if cms_info is None:
        return None
    url, text, link_type = get_link_info(cms_info, text, absolute=absolute)
    return format_text_link(url, text)


def get_html_link(url, text, link_type=None):
    attrs = ''
    if link_type == 'pdf':
        attrs = ' target="_blank"'
    html = dedent("""\
    <a href="{url}"{attrs}>
    {text}</a>""".format(attrs=attrs, text=html_escape(text),
                         url=html_escape(url)))

    return html


def make_html_link(cms_info, text):
    """
    Returns for a PDF link, for example:

        <a href="modules/showdocument.aspx?documentid=2406" target="_blank">
        Agenda (PDF)</a>
    """
    url, text, link_type = get_link_info(cms_info, text)
    html = get_html_link(url, text, link_type=link_type)
    return html


def get_link_html_youtube(youtube_id, duration):
    url = get_url_youtube(youtube_id)
    text = "{0} (YT)".format(duration)
    html = get_html_link(url, text, link_type=None)
    return html


def get_agenda_links_html(agenda_cms_info, agenda_packet_id, status):
    if status == 'TBD':
        html = ''
    elif status == 'canceled':
        if agenda_cms_info:
            html = make_html_link(agenda_cms_info, text="Canceled")
        else:
            html = "No meeting"
    elif status == 'posted':
        if agenda_packet_id is None:
            packet_link = "No Packet"
        elif agenda_packet_id is False:
            packet_link = None
        else:
            text, url = get_agenda_packet_link_info(packet_id=agenda_packet_id)
            packet_link = get_html_link(text=text, url=url)
        html = make_html_link(agenda_cms_info, text="Agenda")
        if packet_link is not None:
            html += " |\n{0}".format(packet_link)
        return html
    else:
        raise Exception("unknown status: {0}".format(status))
    return html


# TODO: move these classes to config.py.
class BodyCommission(object):

    label = common.LABEL_COMMISSION
    meeting_place = "City Hall, Room 408"

    name_file_name = "Elections_Comm"
    name_web = "Commission"
    name_web_index = "Commission"
    name_short = "Commission"
    name_medium = "Elections Commission"
    name_full = "San Francisco Elections Commission"
    name_complete = "San Francisco Elections Commission"
    name_library_subject = "SF Elections Commission"

    sender = "commission"
    public_bcc = None
    body_to = ["cjung", "dparis", "jrowe", "rsafont", "wyu",
               "jarntz", "ashen", "jwhite"]
    body_cc = []
    initials = "/cjj"
    signature = ""
    # signature = "Chris Jerdonek, President"
    tr_class = ''


class BodyBOPEC(object):

    label = common.LABEL_BOPEC
    meeting_place = "City Hall, Room 421"

    name_file_name = "BOPEC"
    name_web = "BOPEC"
    name_web_index = "BOPEC*"
    name_short = "BOPEC"
    name_medium = "BOPEC"
    name_full = "Budget & Oversight of Public Elections Committee (BOPEC)"
    name_complete = ("Budget & Oversight of Public Elections Committee (BOPEC) "
                     "of the San Francisco Elections Commission")
    name_library_subject = "BOPEC (SF Elections Commission)"

    sender = "cjerdonek"
    public_bcc = []
    body_to = ["dparis", "rsafont", "jarntz"]
    body_cc = []
    initials = ""
    signature = ""
    tr_class = ' class="committee"'


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
        print("processing label: {0}".format(label))
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
        agenda_cms_info = config.get_cms_info(data, 'agenda_id')
        agenda_packet_id = data.get('agenda_packet_id')
        agenda_links_html = None
        agenda_packet_link_html = NBSP
        youtube_agenda_link = None
        youtube_agenda_packet_link = None
        minutes_html = TBD_NEW_DOCS
        youtube_id = data.get('youtube_id')
        youtube_link_html = TBD_HTML
        if youtube_id is False:
            # Then the video is known not to exist.
            youtube_link_html = NBSP
        # TODO: make these statuses module constants.
        if meeting_status == 'posted':
            youtube_agenda_link = make_text_link(agenda_cms_info, text="Agenda", absolute=True)
            # YouTube agenda packet info.
            youtube_packet_text, youtube_packet_url = get_agenda_packet_link_info(
                            packet_id=agenda_packet_id, absolute=True)
            youtube_agenda_packet_link = format_text_link(text=youtube_packet_text,
                                                url=youtube_packet_url)
            agenda_link_html = common.indent(make_html_link(agenda_cms_info, text="Agenda"))
            if agenda_packet_id is None:
                agenda_packet_link_html = "None"
            else:
                text, url = get_agenda_packet_link_info(packet_id=agenda_packet_id)
                agenda_packet_link_html = get_html_link(text=text, url=url)
        elif meeting_status == "TBD":
            agenda_link_html = TBD_NEW_DOCS
        elif meeting_status == "canceled":
            meeting_time = "Canceled: no meeting"
            meeting_place = NBSP
            agenda_link_html = NBSP
            agenda_packet_link_html = NBSP
            minutes_html = NBSP
            youtube_link_html = NBSP
        else:
            raise Exception("unknown status: {0}".format(meeting_status))

        agenda_links_html = get_agenda_links_html(agenda_cms_info,
                                agenda_packet_id=agenda_packet_id,
                                status=meeting_status)
        # Minutes
        minutes_cms_info = config.get_cms_info(data, 'minutes_id')
        if minutes_cms_info:
            draft_prefix = 'Draft ' if data.get('minutes_draft') else ''
            text = "{0}Minutes".format(draft_prefix)
            minutes_html = make_html_link(minutes_cms_info, text=text)

        kwargs = {
            'agenda_links_html': common.indent(agenda_links_html),
            'agenda_link_html': agenda_link_html,
            'agenda_packet_link_html': common.indent(agenda_packet_link_html),
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
            'minutes_html': common.indent(minutes_html),
            'meeting_place': meeting_place,
            'meeting_time': meeting_time,
            'meeting_type_adjective': ("{0} ".format(meeting_type_adjective) if
                                       meeting_type_adjective else ""),
            'meeting_type_medium': meeting_type_medium,
            'meeting_type_html': html_escape(meeting_type),
            'tr_class': body.tr_class,
            'youtube_agenda_link': youtube_agenda_link,
            'youtube_agenda_packet_link': youtube_agenda_packet_link,
            'url_home': URL_HOME,
            'url_past_meetings_absolute': get_absolute_url(URL_MEETINGS),
        }

        # YouTube
        audio_base = "{0:%Y%m%d}_{1}".format(date, body_label)
        if youtube_id:
            youtube_length = data.get('youtube_length')
            youtube_length_text = format_youtube_length(youtube_length)
            youtube_link_html = get_link_html_youtube(youtube_id=youtube_id, duration=youtube_length)
            youtube_url = get_url_youtube_short(youtube_id)
            kwargs.update({
                'youtube_length_text': youtube_length_text,
                'youtube_url': youtube_url,
            })
        kwargs.update({
            'audio_base': audio_base,
            'youtube_link_html': common.indent(youtube_link_html),
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
        text = self.get_formatted(format_str, **kwargs)
        text = text[0].upper() + text[1:]

        return text
