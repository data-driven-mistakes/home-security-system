#!/usr/bin/env python3
# https://www.devdungeon.com/content/read-and-send-email-python#toc-3

'''
Program to log into the specified gmail, check the inbox, and execute commands based on the recieved messages
Based on the code in: 
https://www.devdungeon.com/content/read-and-send-email-python#toc-3
and 
https://realpython.com/python-send-email/
'''

import imaplib, re
import email
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase

# gmail server username and password
u='ghetto.alexa@gmail.com'.strip()
p = 'GhettoAlexa123!'.strip()

def main():
    '''
    main method
    '''
    # log into gmail server
    imap_server = imaplib.IMAP4_SSL(host='imap.gmail.com', port=993)
    imap_server.login(u,p)
    imap_server.select()  # Default is `INBOX`

    # Find and loop through all emails in inbox
    _, message_numbers_raw = imap_server.search(None, 'ALL')
    for message_number in message_numbers_raw[0].split():
        _, msg = imap_server.fetch(message_number, '(RFC822)')

        # Parse the raw email message in to a convenient object
        message = email.message_from_bytes(msg[0][1])
        MSG_SUB = message["Subject"]
        msg_sender=message["from"]
        if message.is_multipart():
            multipart_payload = message.get_payload()
            for sub_message in multipart_payload:
                MSG_BODY = sub_message.get_payload()
        else:  # Not a multipart message, payload is simple string
            MSG_BODY = message.get_payload()
        MSG_BODY = re.sub('<[^<]+?>', '', MSG_BODY) # Strip HTML

        # Check the message subject for Ping command
        print(MSG_SUB, MSG_BODY,msg_sender)
        if MSG_SUB == 'PING':
            send_mail(msg_sender.strip(), 'RSP: PING', '')

        # Delete inbox email 
        imap_server.store(message_number, '+FLAGS', '\\Deleted')
        imap_server.expunge()
    
    # logout of the email
    imap_server.close()
    imap_server.logout()

def send_mail(dest, subject, msg, attach=None):
    '''
    Method to send a msg to a dest email
    :param dest: string for the destination email address
    :param subject: string for the subject line
    :param msg: string for the body message
    :param attach: string for the file directory of file to attach. If none: no file attached. 
    '''
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = u
    message["To"] = dest.strip()
    part1 = MIMEText(msg, "plain")
    message.attach(part1)

    # attach file if applicable
    if attach:
        with open(attach, "rb") as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        email.encoders.encode_base64(part)
        part.add_header("Content-Disposition",f"attachment; filename= {attach}",)
        message.attach(part)

    context = ssl.create_default_context()
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context)
    server.login(u,p)
    server.sendmail(u, dest, message.as_string())

# Main method to run on file
if __name__ =='__main__':
    while True:
        main()   



