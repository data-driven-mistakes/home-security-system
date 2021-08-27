#!/usr/bin/env python3
# https://realpython.com/python-send-email/

'''
Program to send a single email to the specified address
'''

import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

smtp_server='smtp.gmail.com'
port = 465

sender='ghetto.alexa@gmail.com'.strip()
password = 'GhettoAlexa123!'.strip()
subject = 'Test1234'.strip()

receiver = 'ghetto.alexa@gmail.com'

message = MIMEMultipart("alternative")
message["Subject"] = "PING"
message["From"] = sender
message["To"] = receiver

text = input("Input CMD: ")

# Turn these into plain/html MIMEText objects
part1 = MIMEText(text, "plain")

# Add HTML/plain-text parts to MIMEMultipart message
# The email client will try to render the last part first
message.attach(part1)

context = ssl.create_default_context()

with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(sender, password)
    
    # send email
    server.sendmail(sender, receiver, message.as_string())
