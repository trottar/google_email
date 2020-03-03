#! /usr/bin/python

#
# Description:
# ================================================================
# Time-stamp: "2020-03-02 17:34:10 trottar"
# ================================================================
#
# Author:  Richard L. Trotta III <trotta@cua.edu>
#
# Copyright (c) trottar
#

import write_email
import sys, os, smtplib, functools, imghdr
from email.message import EmailMessage

email_entries = write_email.createGUI()

to_email = email_entries[3]
cc_email = email_entries[2]

input_emails="../user_emails/email_groups.input"

with open(input_emails) as file:
    for line in file:
        email_list = line.split('=')
        if to_email == email_list[0]:
            to_email_addr = email_list[1].strip()
        elif cc_email == email_list[0]:
            cc_email_addr = email_list[1].strip()
print("To: ", to_email_addr)
print("Cc: ", cc_email_addr)

my_email_addr = os.environ.get('PY_EMAIL_CUA')
my_email_pass = os.environ.get('PY_EMAIL_CUA_PASS')

msg = EmailMessage()
msg['Subject'] = email_entries[1]
msg['From'] = my_email_addr
msg['To'] = to_email_addr
msg['Cc'] = cc_email_addr

def stringtohtml(text):
    text_1 = text.replace('\n', '<br>')
    text_2 = text_1.replace('\t', '<span style="margin-left:2em">')
    text_3 = text_2.replace('-b', '<b>')
    text_3a = text_3.replace('-/b', '</b>')
    text_4 = text_3a.replace('-i', '<i>')
    text_4a = text_4.replace('-/i', '</i>')
    text_5 = text_4a.replace('-u', '<u>')
    text_5a = text_5.replace('-/u', '</u>')
    text_6 = text_5a.replace('-_', '<sub>')
    text_6a = text_6.replace('-/_', '</sub>')
    text_7 = text_6a.replace('-^', '<sup>')
    text_7a = text_7.replace('-/^', '</sup>')
    text_8 = text_7a.replace('-~', '<mark>')
    text_8a = text_8.replace('-/~', '</mark>')
    text_9 = text_8a.replace('-c', '<code>')
    text_9a = text_9.replace('-/c', '</code>')
    partial = text_9a.replace('-\partial', '&#8706;')
    nabla = partial.replace('-\nabla', '&#8711;')
    integral = nabla.replace('-\int', '&int;')
    return integral

html_data = stringtohtml(email_entries[0])

with open('html/signature.html', 'r') as file:
    sig_data = file.read().replace('\n', '')

msg.add_alternative(html_data+sig_data,subtype='html')

if write_email.UploadAction.has_been_called:
    image_dir = []
    for i in range(0,len(email_entries)-4):
        image_dir.append(email_entries[4+i])

    files = image_dir

    for file in files:
        with open(file,'rb') as f:
            file_type = imghdr.what(f.name)
            if file_type == None:
                file_data = f.read()
                file_name = f.name
                msg.add_attachment(file_data,maintype='application',
                            subtype='octet-stream',filename=file_name)
            else:
                file_data = f.read()
                file_name = f.name
                msg.add_attachment(file_data,maintype='image',
                            subtype=file_type,filename=file_name)

'''
Below is for running localhost debugging

to establish connection...

>python3 -m smtpd -c DebuggingServer -n localhost:1025

The following must also be commented out...
# gmail port 465, SMTP_SSL will identify with mail server 
# of use then encrypt traffic then reidentify server
with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
    smtp.login(email_addr, email_pass)

The rest is unchanged

'''
# with smtplib.SMTP('localhost',1025) as smtp:
with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
    smtp.login(my_email_addr, my_email_pass)
    smtp.send_message(msg)
