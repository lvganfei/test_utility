# -*- coding: utf-8 -*-

import email
import smtplib
import sys, io, os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage


class MailClient(object):
    def __init__(self, user='developer@democompany.net', password='6kJF64wTm88EJuiX',
                 smtp_host='smtp.exmail.qq.com', port=465, user_name=None):
        self.user = user
        self.user_name = user_name or user
        self.password = password

        self.smtp_host = smtp_host
        self.port = port

        self.server = smtplib.SMTP_SSL(self.smtp_host, self.port)
        self.server.set_debuglevel(False)
        self.server.login(user, password)

    def send(self, to_list=['lixy@democompany.net','wanggh@democompany.net','guyy@democompany.net'], subject='test', html='<html></html>', text='', mailfiles=[]):
        try:
            content = self.get_content(subject=subject, from_=self.user, to_=to_list, html=html, text=text,
                                       mailfiles=mailfiles)
            self.server.sendmail('<%s>' % self.user, to_list, content)
            print('send email successful')
        except Exception as e:
            print(e)
            print('send email failed')
        finally:
            self.server.quit()
    
    def get_content(self, subject, from_, to_, html, text, mailfiles):
        attach = MIMEMultipart()
        # 添加邮件内容
        text_content = MIMEText('<h1>' + text + '</h1>', 'html')
        html_content = MIMEText(html, 'html')
        attach.attach(text_content)
        attach.attach(html_content)
        attach['Subject'] = subject or ''
        attach['From'] = from_
        attach['To'] = ';'.join(to_)
        for mailfile in mailfiles:
            part = MIMEApplication(open(mailfile.filepath, 'rb').read())
            part.add_header('Content-Disposition', 'attachment', filename=mailfile.filename)
            attach.attach(part)
        return attach.as_string()

if __name__ == '__main__':
    print(sys.argv)
    # ex: python3 mail_notification.py lixy@democompany.net
    job_name = os.getenv('JOB_NAME')
    push_interval = os.getenv('PUSH_INTERVAL')
    print(push_interval)
    push_count = str(sys.argv[1])
    push_current_count = str(sys.argv[2])
    service = str(sys.argv[3])
    receiver = str(sys.argv[-1]).split(',')
    
    print(os.getenv('JOB_NAME'))

    
    msg = '当前推送产品:'+ service + ' 已推送病例序列总数: ' + push_count + '  当前小时推送病例序列数: ' + push_current_count
    print(receiver)
    mail_client = MailClient()
    to_list = ['lixy@democompany.net']
    to_list = to_list + receiver
    print(to_list)
    mail_client.send(to_list=to_list, subject=msg, text=msg)