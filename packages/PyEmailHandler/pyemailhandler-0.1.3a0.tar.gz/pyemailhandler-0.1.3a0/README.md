# PyEmailHandler

Receive and Send emails at ease. 

Intended for quick and easy projects that does not require specific function other than to receive, send and reply to emails.

**Supports:**
* IMAP4
* SMTP

## Basic Usage: 

### Send a simple Email
```py
from PyEmailHandler import EmailSMTP
email = EmailSMTP(
        username="smtp_username",
        password="smtp_password",
        sender_mail="sender@example.com",
        sender_name="WeSend",
        smtp_server="smtp.example.com",
        port = 587,
        protocol = "starttls"
    )
email.start_connection()
email.send(
    receiver="recipient@mailaddress.com",
    subject="Subject of the e-mail",
    body="Content of the e-mail, can be as long as you want"
)
```

### Send a comprehensive Email
```py
from PyEmailHandler import EmailSMTP
email = EmailSMTP(
        username="smtp_username",
        password="smtp_password",
        sender_mail="sender@example.com",
        sender_name="WeSend",
        smtp_server="smtp.example.com",
        port = 587,
        protocol = "starttls"
    )
email.start_connection()
message = MIMEText(html_text, 'html')
message['Subject'] = "Main subject"
message['To'] = "Recipient Name <recipient@mailaddress.com>"
message['From'] = "WeSend <sender@example.com>"
email.send_raw(
    receiver="recipient@mailaddress.com",
    mime=message
)
```

### Receive Inbox
```py
from PyEmailHandler import EmailIMAP
inbox = EmailIMAP(
        username="imap_username",
        password="imap_password",
        imap_server="imap.example.com",
        port=993,
        protocol="ssl"      
    )
inbox.start_connection()
mails = inbox.get_mails()
for mail in mails:
    print(mail)
```

### Reply to an inbox
By combining Both IMAP and SMTP functionalities
```py
from PyEmailHandler import EmailIMAP, EmailSMTP
from PyEmailHandler.tools import reply_mail
inbox = EmailIMAP(
        username="imap_username",
        password="imap_password",
        imap_server="imap.example.com",
        port=993,
        protocol="ssl"      
    )
inbox.start_connection()
smtp = EmailSMTP(
        username="smtp_username",
        password="smtp_password",
        sender_mail="sender@example.com",
        sender_name="WeSend",
        smtp_server="smtp.example.com",
        port = 587,
        protocol = "starttls"
    )
smtp.start_connection()

mails = inbox.get_mails()
for mail in mails:
    if mail == "Some Criteria here":
        message = MIMEText("Body of Message goes here", "plain")
        #Other headers are handled automatically only the body of the message is required.
        #Some headers are not automatically handled such as the Reply-To header which might be important
        reply_mail(smtp, mail, message)
```

PROTOCOLS:
```py
ssl
starttls
none #This is unsecure mode, use it at your own discretion
```