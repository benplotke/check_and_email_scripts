#!/usr/bin/python3


# ABOUT
#  A short python script that checks if the external ip has changed and emails me if it has
#  I use a timer to run this once and hour
#  I used a junk gmail account for the send. Because I'm sending in an unsecure fashion, I needed to turn off some gmail security settings to get it to work.


import urllib.request
import smtplib

saved_ip_path = '/home/example/.ip_updater'
ip_server = "http://myip.dnsdynamic.org/"
dst_email_account = 'example1@gmail.com'
smtp_server = 'smtp.gmail.com:587'
src_email_account = 'example2@gmail.com'
src_email_passwd = 'password'

def mail_func(To, Subj, Txt, srvr, accnt, psswd):
    From = 'ip_updater@python.localhost'
    Msg = '\r\n'.join([
        'From: '+From,
        'To: '+To,
        'Subject: '+Subj,
        '',
        Txt
    ])
    srv = smtplib.SMTP(srvr)
    srv.ehlo()
    srv.starttls()
    srv.login(accnt, psswd)
    print(Msg)
    srv.sendmail(From, To, Msg)
    srv.quit()

ipfile = open(saved_ip_path, 'r')
lastip = ipfile.readline()
ipfile.close()
presentip = urllib.request.urlopen(ip_server).read().decode('ascii')
if presentip!=lastip:
    mail_func(dst_email_account, 'IP change', 'Now '+presentip, smtp_server, src_email_account, src_email_passwd)
    ipfile = open(saved_ip_path, 'w')
    ipfile.write(presentip)
    ipfile.close()

