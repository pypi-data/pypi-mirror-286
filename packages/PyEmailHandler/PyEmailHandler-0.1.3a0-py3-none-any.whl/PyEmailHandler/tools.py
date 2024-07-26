from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . import EmailSMTP
from email.message import Message as emailMessage
from email.mime.text import MIMEText
from email.utils import formataddr, make_msgid, parseaddr, formatdate
from email.header import Header, decode_header
import re

def dom_extract(email):
    match = re.search(r'@([^@]+)$', email)
    if match:
        return match.group(1)
    return None

def cast(obj, to_type, options=None):
    try:
        if options is None:
            return to_type(obj)
        else:
            return to_type(obj, options)
    except ValueError and TypeError:
        return obj

def parse_header(decoded_header):
    _data = ''
    for part, encoding in decoded_header:
        if isinstance(part, bytes):
            if encoding:
                part = part.decode(encoding=encoding)
            else:
                part = part.decode(encoding='utf-8')
        _data += part
    return _data

def reply_mail(
        smtp: "EmailSMTP",
        mail: emailMessage,
        message: MIMEText,
):
    '''
    Reply to the Received receipient on selected mail on IMAP.

    smtp: `EmailSMTP` instance that has active smtp connection
    mail: Selected recipient to reply to
    message: MIMEText that contains the `body` of the message. `To`, `From` and `Subject` is not required as they are automatically added
    '''
    msg = message
    receiver_full = decode_header(mail['Reply-To'] or mail['From'])
    receiver_decoded = parse_header(receiver_full)
    receiver_name, receiver_address = parseaddr(receiver_decoded)
    sender = smtp.sender_mail
    sender_name = smtp.sender_name
    msg['To'] = receiver_decoded
    msg["Message-ID"] = make_msgid(domain=dom_extract(email=sender))
    message['Date'] = formatdate()
    subject_header = mail["Subject"]
    pattern = re.compile(r"^(re:\s*)?(.*)", re.IGNORECASE)
    match = pattern.match(subject_header).group(2).strip()
    msg['Subject'] = "Re: " + (match)
    msg["In-Reply-To"] = mail["Message-ID"]
    msg["References"] = (mail["References"] or "") + " " + mail["Message-ID"]
    if sender:
        msg['From'] = formataddr((
            cast(Header(sender_name, 'utf-8'), str),
            sender
        ))
    smtp.connection_persist()
    smtp.send_raw(receiver=receiver_address, mime=msg)
