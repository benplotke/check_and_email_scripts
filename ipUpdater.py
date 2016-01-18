#!/usr/bin/python3
# if results from icanhazip.com differ from file lastip.txt, it updates lastip.txt and emails the new one

import urllib.request
import smtplib

def mail_func(To, Subj, Txt):
    From = 'ben@python.localhost'
    Msg = '\r\n'.join([
        'From: '+From,
        'To: '+To,
        'Subject: '+Subj,
        '',
        Txt
    ])
    srv = smtplib.SMTP('smtp.gmail.com:587')
    srv.ehlo()
    srv.starttls()
    srv.login('youremail@gmail.com','password')
    print(Msg)
    srv.sendmail(From, To, Msg)
    srv.quit()

ipfile = open('/home/ben/tmp/lastip.txt', 'r')
lastip = ipfile.readline()
ipfile.close()
presentip = urllib.request.urlopen("http://myip.dnsdynamic.org/").read().decode('ascii')
if presentip!=lastip:
    mail_func('benplotke@gmail.com', 'IP change', 'Now '+presentip)
    ipfile = open('/home/ben/tmp/lastip.txt', 'w')
    ipfile.write(presentip)
    ipfile.close()

