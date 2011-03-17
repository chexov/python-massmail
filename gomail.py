#!/usr/bin/env python
# encoding: utf-8
# https://github.com/chexov/python-massmail
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def sendmail_mass(me, recipients, subject, text, html):
    # me == my email address
    # you == recipient's email address
    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = me

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain', 'utf-8')
    part2 = MIMEText(html, 'html', 'utf-8')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)

    # Send the message via local SMTP server.
    s = smtplib.SMTP('localhost')
    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    for you in recipients:
        if you:
            print "sending email to:", you
            msg['To'] = you
            s.sendmail(me, you, msg.as_string())
    s.quit()



if __name__ == "__main__":
    import sys
    if not len(sys.argv) == 5:
        print "Usage: %s <body.txt> <body.html> <from> <subject>" % sys.argv[0]
        print "enter recipients list in stdin. one email per line"
        sys.exit(1)
    text_fn, html_fn, me, subject = sys.argv[1:5]
    try:
        text = open(text_fn).read()
    except IOError:
        print "Error. Can not open file %s" % text_fn
        sys.exit(1)

    try:
        html = open(html_fn).read()
    except IOError:
        print "Error. Can not open file %s" % html_fn
        sys.exit(1)

    recipients = sys.stdin.readlines()
    sendmail_mass(me, recipients, subject, text, html)

