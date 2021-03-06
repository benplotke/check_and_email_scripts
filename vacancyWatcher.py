#!/usr/bin/python3

# This was written to check a particular property site for new vacancies and email me if there are any

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import smtplib 

url = 'domain.to/watch'
path = '/path/to/file/for/storage'

email_login = ('IShouldFigure@outHow.toNot', 'putCredsDirectlyInThis')
email_from = ''
email_to = ''

subject = ''

def get_current_addrs(url):
    options = Options()
    options.add_argument('--headless')
    browser = webdriver.Chrome(options = options)
    browser.get(url)
    listing_items = browser.find_elements_by_class_name('listing-item')
    current_addrs = set()
    for l in listing_items:
        addr = l.find_element_by_tag_name('a').get_attribute('aria-label') 
        current_addrs.add(addr)
    browser.close()
    return current_addrs

def get_past_addrs(path):
    past_addrs = set()
    with open(path, 'r') as f:
        for l in f:
            past_addrs.add(l.rstrip())
    return past_addrs

def save_addrs(path, addrs):
    with open(path, 'w')as f:
        f.writelines("\n".join(addrs))

def email(From, to, subj, txt, creds):
    msg = '\r\n'.join([
        'From: '+From,
        'To: '+to,
        'Subject: '+subj,
        '',
        txt
    ])
    srv = smtplib.SMTP('smtp.gmail.com:587')
    srv.ehlo()
    srv.starttls()
    srv.login(creds[0], creds[1])
    srv.sendmail(From, to, msg)
    srv.quit()

current_addrs = get_current_addrs(url)
past_addrs = get_past_addrs(path)
new_addrs = current_addrs - past_addrs

if new_addrs:
    email(email_from, email_to, subject, '\r\n'.join(new_addrs), email_login)
    all_addrs = current_addrs.union(past_addrs)
    save_addrs(path, all_addrs)
