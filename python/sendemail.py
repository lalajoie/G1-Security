#!/usr/bin/env python

import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

fromaddr = "g1sec.notif@gmail.com"
toaddr = "lalajoiedg@gmail.com"

msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "g1Sec - SOMEONE'S AT YOUR DOOR"
body = 'There is a stranger at your door.'
msg.attach(MIMEText(body, 'plain'))

filename = "intruder.jpg"
attachment = open("/var/www/html/g1-Security/python/strangers/intruder.jpg", "rb")

part = MIMEBase('application', 'octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment; filename= {}".format(filename))
msg.attach(part)

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(fromaddr, "g1secthesis")
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()