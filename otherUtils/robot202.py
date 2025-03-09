#!/usr/bin/python
#-*- coding:utf-8 -*-
"""
@author:lqfff
@file: shiyisys
@time: 2021-04-01
"""

from sqlalchemy import create_engine
import requests
import time
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

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
        self.default_receiver = ['maoxs@democompany.net','xukang@democompany.net','guyy@democompany.net','jinjie@democompany.net','lixy@democompany.net','zhengyj@democompany.net','zchao@democompany.net']
        # self.default_receiver = ['lixy@democompany.net']

    def send(self, to_list=['lixy@democompany.net', 'jinjie@democompany.net'], subject='', mail_file='', html='', text=''):

        try:
            content = self.get_content(subject=subject, from_=self.user, to_=self.default_receiver, html=html, text=text, mail_file=mail_file)
            self.server.sendmail('<%s>' % self.user, self.default_receiver, content)
            print('send email successful')
        except Exception as e:
            print(e)
            print('send email failed')
        finally:
            self.server.quit()

    def get_content(self, subject, from_, to_, html, text, mail_file):
        html_content_raw = ''
        attach = MIMEMultipart()

        if html != '':
            with open(html, 'r') as html_file:
                    html_content_raw = html_file.read()
                    html_file.close()
            html_content = MIMEText(html_content_raw, 'html', 'utf-8')
            attach.attach(html_content)

        # 添加邮件内容
        text_content = MIMEText(text)
        print(f'text_content: {text}')
        
        attach.attach(text_content)
        attach['Subject'] = subject or '【Elemon测试】'
        attach['From'] = from_
        attach['To'] = ';'.join(to_)
        print('hhhhhhh')
        # print(attach.as_string())
        if not os.path.exists(mail_file):
            return attach.as_string()
        f = open(mail_file, 'rb')
        part = MIMEApplication(f.read())
        part.add_header('Content-Disposition', 'attachment', filename=mail_file.split("/")[-1])
        attach.attach(part)
        f.close()
        # print(attach.as_string())
        return attach.as_string()

currentDate=time.strftime("%Y%m%d",time.localtime())
# currentDate= "20191231"
# endData=time.strftime("%Y-%m-%d",time.localtime())
# startData=time.strftime("%Y-%m-%d",time.localtime())
endData="2999-12-31"
startData="2000-01-01"
currentDateTime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
# currentDateTime="2019-12-27 16:22:22"

# 此处请修改微信机器人地址
roboturl="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=90971447-f371-4f6b-8f5e-56908b9e06cf"


#平台登录地址
platform_login_url="http://platform.democompany.net/api/usr/tokens"
#平台用户名
platform_username="admin_super"
#平台密码 （需转换成sha256）
# platform_password="8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92" # 123456
platform_password="edd969ea6bf8da3477e8d66bb145e58847c31599268d705e77961e7ac4f96403" # democompany2019


#交付平台登录地址
# deliver_login_url="http://localhost:6989/api/login"
deliver_login_url="http://platform.democompany.net:6989/api/login"
#交付平台账号
deliver_username="xukang"
#交付平台密码 （需转换成sha256）
deliver_password="8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92" # 123456
# deliver_password="edd969ea6bf8da3477e8d66bb145e58847c31599268d705e77961e7ac4f96403" # democompany2019


def GetResult(sqlstr):
    sqlurl="mysql+pymysql://root:qY1WBZ30vjsriiHiEgK2ZkE8osjYNsj@platform.democompany.net:13306/plt_dicom?charset=utf8mb4"
    engine = create_engine(sqlurl)
    cur = engine.execute(sqlstr)
    return cur.fetchone()



if __name__ == '__main__':


    #产品平台模拟登录token
    platform_data = {
        "username": platform_username,
        "password": platform_password
    }
    platform_login=requests.post(platform_login_url,headers={"Content-Type": "application/json","User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"},json=platform_data)
    platform_token=platform_login.json().get("token")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
        "Authorization": "Bearer "+platform_token
    }

    #交付平台模拟登录token
    deliver_data = {
        "username": deliver_username,
        "password": deliver_password
    }
    # deliver_login=requests.post(deliver_login_url,headers={"Content-Type": "application/json"},json=deliver_data)
    # print(deliver_login.status_code)
    # deliver_headers=deliver_login.json().get("token")
    #
    # # GPU信息
    # gpustate = requests.get("http://platform.democompany.net:6989/api/system/gpu/status",headers = {"Authorization" : deliver_headers})
    # gpuc = ""
    # gpulist = gpustate.json().get("data")
    # for gpu in gpulist:
    #     gpuc = gpuc + "显卡" + str(gpu.get("id")) + ":" + gpu.get("name") + "  当前温度:" + str(gpu.get("temperature")) + "\n"

    # 收到的序列总量
    sql_all_t_series = "SELECT count(*) FROM plt_universe.t_series ; "
    all_t_series = int(GetResult(sql_all_t_series)[0])
    # 收到的序列总张数
    sql_all_t_images = "SELECT ifnull(sum(images),0) FROM plt_universe.t_series ; "
    all_t_images = int(GetResult(sql_all_t_images)[0])
    # 收到的病例总量
    sql_all_series = "SELECT ifnull(sum(instance_count),0) FROM series ; "
    all_series = int(GetResult(sql_all_series)[0])

    # 通过推送接收的未应用病例总量
    sql_push_unapply = "SELECT ifnull(sum(instance_count),0) FROM series WHERE from_pull = 'FROM_PUSH' AND state = 'UNAPPLY'"
    push_unapply = int(GetResult(sql_push_unapply)[0])

    # 通过拉取接收的未应用病例总量
    sql_pull_unapply = "SELECT ifnull(sum(instance_count),0) FROM series WHERE from_pull = 'FROM_PULL' AND state = 'UNAPPLY'"
    pull_unapply = int(GetResult(sql_pull_unapply)[0])

    # 肺结节计算成功量
    sql_thoracic_completetask = "select ifnull(count(*),0) from plt_thoracic.cases where state =2 "
    thoracic_completetask = int(GetResult(sql_thoracic_completetask)[0])

    # 肺结节计算失败量
    sql_thoracic_failtask = "select ifnull(count(*),0) from plt_thoracic.cases where state =6 "
    thoracic_failtask = int(GetResult(sql_thoracic_failtask)[0])

    # 肺结节等待计算量
    sql_thoracic_waittasks = "select ifnull(count(*),0) from plt_thoracic.cases where state =11 "
    thoracic_waittasks = int(GetResult(sql_thoracic_waittasks)[0])

    # 分发到肺结节的序列数
    sql_thoracic_applytask = "select ifnull(count(*),0) from plt_dicom.series where applied_services='thoracic' "
    thoracic_applytask = int(GetResult(sql_thoracic_applytask)[0])

    # 分发到冠脉的序列数
    sql_coronary_applytask = "select ifnull(count(*),0) from plt_dicom.series where applied_services='coronary' "
    coronary_applytask = int(GetResult(sql_coronary_applytask)[0])

    # 分发到头颈的序列数
    sql_cerebral_applytask = "select ifnull(count(*),0) from plt_dicom.series where applied_services='cerebral' "
    cerebral_applytask = int(GetResult(sql_cerebral_applytask)[0])

    # 已应用序列数
    sql_apply_series = "select ifnull(count(*),0) from plt_dicom.series where state = 'APPLIED' "
    apply_series = int(GetResult(sql_apply_series)[0])

    # 未应用序列数\
    sql_unapply_series = "select ifnull(count(*),0) from plt_dicom.series where state = 'UNAPPLIED' "
    unapply_series = int(GetResult(sql_unapply_series)[0])

    # 等待计算病例
    sql_waittask = "SELECT ifnull(count(*),0) FROM `plt_alg_srv`.`t_task_queue`; "
    waittask = int(GetResult(sql_waittask)[0])

    # 冠脉重建完成
    sql_coronary_generatedtask = "select ifnull(count(*),0) from plt_coronary.cases where state =2  "
    coronary_generatedtask = int(GetResult(sql_coronary_generatedtask)[0])

    # 冠脉诊断完成
    sql_coronary_acceptedtasks = "select ifnull(count(*),0) from plt_coronary.cases where state =4  "
    coronary_acceptedtasks = int(GetResult(sql_coronary_acceptedtasks)[0])

    # 冠脉无法计算
    sql_coronary_nopasstasks = "select ifnull(count(*),0) from plt_coronary.cases where state =6  "
    coronary_nopasstasks = int(GetResult(sql_coronary_nopasstasks)[0])

    # 冠脉等待计算
    sql_coronary_waittasks = "select ifnull(count(*),0) from plt_coronary.cases where state =11  "
    coronary_waittasks = int(GetResult(sql_coronary_waittasks)[0])

    # 头颈重建完成
    sql_cerebral_generatedtask = "select ifnull(count(*),0) from plt_cerebral.cases where state =2 "
    cerebral_generatedtask = int(GetResult(sql_cerebral_generatedtask)[0])

    # 头颈诊断完成
    sql_cerebral_acceptedtasks = "select ifnull(count(*),0) from plt_cerebral.cases where state =4 "
    cerebral_acceptedtasks = int(GetResult(sql_cerebral_acceptedtasks)[0])

    # 头颈无法计算
    sql_cerebral_nopasstasks = "select ifnull(count(*),0) from plt_cerebral.cases where state =6 "
    cerebral_nopasstasks = int(GetResult(sql_cerebral_nopasstasks)[0])

    # 头颈等待计算
    sql_cerebral_waittasks = "select ifnull(count(*),0) from plt_cerebral.cases where state =11 "
    cerebral_waittasks = int(GetResult(sql_cerebral_waittasks)[0])

    content = "今日状态:" \
              + "\n收到的序列总量:" + str(all_t_series) \
              + "\n收到的序列总张数:" + str(all_t_images) \
              # + "\n接收case数总量:" + str(all_series) \
              # + "\n通过推送接收的未应用病例张数总量:" + str(pull_unapply) \
              # + "\n通过拉取接收的未应用病例张数总量:" + str(push_unapply) \
              # + "\n已应用序列总数:" + str(apply_series) \
              # + "\n未应用序列总数:" + str(unapply_series) \
              # + "\n剩余计算task(包含正在计算中):" + str(waittask) \
              # + "\n\n分发到冠脉的量(序列):" + str(coronary_applytask) \
              # + "\n冠脉重建完成量(序列):" + str(coronary_generatedtask) \
              # + "\n冠脉诊断完成量(序列):" + str(coronary_acceptedtasks) \
              # + "\n冠脉无法计算量(序列):" + str(coronary_nopasstasks) \
              # + "\n冠脉等待计算量(序列):" + str(coronary_waittasks) \
              # + "\n\n分发到头颈的量(序列):" + str(cerebral_applytask) \
              # + "\n头颈重建完成量(序列):" + str(cerebral_generatedtask) \
              # + "\n头颈诊断完成量(序列):" + str(cerebral_acceptedtasks) \
              # + "\n头颈无法计算量(序列):" + str(cerebral_nopasstasks) \
              # + "\n头颈等待计算量(序列):" + str(cerebral_waittasks) \
              # + "\n\n分发到肺结节的量(序列)" + str(thoracic_applytask) \
              # + "\n肺结节计算成功量(序列):" + str(thoracic_completetask) \
              # + "\n肺结节计算失败量(序列)" + str(thoracic_failtask) \
              # + "\n肺结节等待计算量(序列)" + str(thoracic_waittasks) \
              # + "\n\n显卡使用情况:\n" + gpuc
    print(currentDateTime + "  " + content)

    
    mail_client = MailClient()
    to_list = ['maoxs@democompany.net','xukang@democompany.net','guyy@democompany.net','jinjie@democompany.net','lixy@democompany.net','zhengyj@democompany.net','zchao@democompany.net']
    print(to_list)
    mail_client.send(to_list=to_list, subject='序列接收状态提醒', text=content)