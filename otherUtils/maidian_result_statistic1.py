# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : result_sc1.py
# Time       ：2022/9/22 1:58 下午
# Author     ：yu xin zhang
# version    ：python 3.7.5
# Description：场景一结果统计
"""
import time

import numpy as np
import pymysql
import requests

study_instance_uid_list = ["1.2.194.0.108707908.20220903082510.1600.10226.764380",
    "1.2.392.200036.9116.2.6.1.3268.2054832322.1662515699.349744",
    "1.2.392.200036.9116.2.6.1.3268.2054832322.1662515809.666202",
    "1.2.392.200036.9116.2.6.1.3268.2054832322.1662515928.18102",
    "1.2.392.200036.9116.2.6.1.3268.2054832322.1662516034.727792",
    "1.2.392.200036.9116.2.6.1.3268.2054832322.1662516147.629632",
    "1.2.392.200036.9116.2.6.1.3268.2060440108.1662521511.530002",
    "1.2.392.200036.9116.2.6.1.3268.2060440108.1662526704.118639",
    "1.2.840.113619.2.417.3.2831219466.357.1662504798.277",
    "1.2.86.76547135.7.141025.20220907141136",
    "1.3.12.2.1107.5.1.4.121099.30000022090601022528900000091",
    "1.3.6.1.4.1.46677.0.600182.214698856.2209060114",
    "1.3.6.1.4.1.46677.0.600182.214750532.2209070078",
    "1.3.6.1.4.1.46677.0.600213.214759990.2209070154",
    "1.3.6.1.4.1.46677.0.600213.214783170.2209070171",
    "1.3.6.1.4.1.46677.0.600213.214799254.2209070179",
    "1.3.6.1.4.1.46677.0.600213.214827767.2209050104",
    "1.3.6.1.4.1.46677.0.600303.214828709.2209070175",
    "1.3.6.1.4.1.46677.0.600370.214702803.2209070065",
    "1.3.6.1.4.1.46677.0.600370.214715985.2209070086",
    "1.3.6.1.4.1.46677.0.600370.214776857.2209070156",
    "1.3.6.1.4.1.46677.0.600474.214826455.2209070172",
    "1.3.6.1.4.1.46677.0.600474.214827428.2209070189",
    "1.3.6.1.4.1.46677.0.600481.214645752.2209070009",
    "1.3.6.1.4.1.46677.0.600514.214780592.2209070203",
    "1.3.6.1.4.1.46677.0.600670.214826819.2209070322",
    "1.3.6.1.4.1.46677.0.600670.214827550.2209070341",
    "1.3.6.1.4.1.46677.0.600670.214827598.2209070342",
    "1.3.6.1.4.1.46677.0.600692.214697677.2209070051",
    "1.3.6.1.4.1.46677.0.600692.214711766.2209070068",
    "1.3.6.1.4.1.46677.0.600692.214721552.2209070084",
    "1.3.6.1.4.1.46677.0.600692.214731054.2209070094",
    "1.3.6.1.4.1.46677.0.600692.214738386.2209070106",
    "1.3.6.1.4.1.46677.0.600692.214753421.2209070127",
    "1.3.6.1.4.1.46677.0.600692.214769576.2209070143",
    "1.3.6.1.4.1.46677.0.600692.214785554.2209070151",
    "1.3.6.1.4.1.46677.0.600701.214662607.2209070063",
    "1.3.6.1.4.1.46677.0.600715.214693793.2209070082",
    "1.3.6.1.4.1.46677.0.600715.214741009.2209070102",
    "1.3.6.1.4.1.46677.0.600715.214765262.2209070113",
    "1.3.6.1.4.1.46677.0.600715.214812869.2209070130",
    "1.3.6.1.4.1.46677.0.600715.214817534.2209070133",
    "1.3.6.1.4.1.46677.0.600745.214721482.2209070036",
    "1.3.6.1.4.1.46677.0.600745.214735855.2209070054",
    "1.3.6.1.4.1.46677.0.600745.214745653.2209070067",
    "1.3.6.1.4.1.46677.0.600745.214752923.2209070077",
    "1.3.6.1.4.1.46677.0.600745.214790477.2209070101",
    "1.3.6.1.4.1.46677.0.600790.214802050.2209070100",
    "1.3.6.1.4.1.46677.0.600790.214802871.2209070104",
    "1.3.6.1.4.1.46677.0.600790.214803458.2209070112"]


class Result:

    def __init__(self):
        self.host = '10.12.10.222'
        self.port = 13306
        self.user = "root"
        self.passwd = "qY1WBZ30vjsriiHiEgK2ZkE8osjYNsj"
        self.db = pymysql.connect(host=self.host, port=self.port,
                                  user=self.user, password=self.passwd, database="plt_dicom")
        self.cursor = self.db.cursor()
        self.db2 = pymysql.connect(host=self.host, port=self.port,
                                  user=self.user, password=self.passwd, database="plt_thoracic")
        self.cursor2 = self.db2.cursor()
        # 计算成功的series_uid
        self.success_series_uid_list = []
    #   计算成功的总数
        self.num = 0
    #     dicom总数量
        self.image_count = 0
    #    计算成功的series_time的时间戳
        self.series_time_list = []
        self.series_create_time = []
        self.receive_end_time = []
        self.series_receive_time = []
        self.case_create_time = []
        self.alg_start_at = []
        self.alg_finish_at = []
        self.case_finish_time = []
        self.series_select_end = []
        self.series_select_start = []

    def get_sql(self):
        # 查询所有计算成功的case
        sql = """SELECT study_identifier,identifier,image_count FROM cases WHERE `state`='2'"""
        self.cursor2.execute(sql)
        res = self.cursor2.fetchall()
        for i in res:
            if i[0] in study_instance_uid_list:
                self.num += 1
                self.image_count += i[2]
                self.success_series_uid_list.append(i[1])
        print("计算成功的series_study_uid",self.success_series_uid_list)
        print(f"计算成功{self.num}个")
    #   查询平台计算成果的series_time
        for series in self.success_series_uid_list:
            sql = f"""SELECT series_date,series_time FROM series WHERE `series_instance_uid`='{series}'"""
            self.cursor.execute(sql)
            res = self.cursor.fetchone()
            tmp_t = f"{str(res[0])[0:4]}-{str(res[0])[4:6]}-{str(res[0])[6:8]} {str(res[1])[0:2]}:{str(res[1])[2:4]}:{str(res[1])[4:6]}"
            tmp_ts = int(time.mktime(time.strptime(tmp_t, "%Y-%m-%d %H:%M:%S")))
            self.series_time_list.append(tmp_ts)
        print(self.series_time_list)
    #  查询具体时间关键节点
        for series in self.success_series_uid_list:
            sql = f"""SELECT series_instance_uid,action,event_time FROM dicom_analysis_result WHERE `series_instance_uid`='{series}'"""
            self.cursor.execute(sql)
            res = self.cursor.fetchall()
            for i in res:
                if i[1] == "case_finish_time":
                    self.case_finish_time.append(int(i[2]))
                elif i[1] == "receive_end_time":
                    self.receive_end_time.append(int(int(i[2])/1000))
                elif i[1] == "series_select_end":
                    self.series_select_end.append(int(i[2]))
                elif i[1] == "alg_finish_at":
                    self.alg_finish_at.append(int(i[2]))
                elif i[1] == "series_select_start":
                    self.series_select_start.append(int(i[2]))
                elif i[1] == "series_receive_time":
                    self.series_receive_time.append(int(i[2]))
                elif i[1] == "alg_start_at":
                    self.alg_start_at.append(int(i[2]))
                elif i[1] == "series_create_time":
                    self.series_create_time.append(int(int(i[2])/1000))
                elif i[1] == "case_create_time":
                    self.case_create_time.append(int(i[2]))

    def get_result(self):
        receive_end_time_to_series_receive_time_list = []
        seies_time_to_series_create_time_list = []
        case_create_time_to_alg_start_at_list = []
        alg_start_at_to_alg_finish_at_list = []
        alg_finish_at_to_case_finish_time_list = []
        series_time_to_case_finish_time_list = []
        for i in range(self.num):
            seies_time_to_series_create_time_list.append(self.series_create_time[i] - self.series_time_list[i])
            seies_time_to_series_create_time_list.sort()
            receive_end_time_to_series_receive_time_list.append(self.series_receive_time[i] - self.receive_end_time[i])
            receive_end_time_to_series_receive_time_list.sort()
            case_create_time_to_alg_start_at_list.append(self.alg_start_at[i] - self.case_create_time[i])
            case_create_time_to_alg_start_at_list.sort()
            alg_start_at_to_alg_finish_at_list.append(self.alg_finish_at[i] - self.alg_start_at[i])
            alg_start_at_to_alg_finish_at_list.sort()
            alg_finish_at_to_case_finish_time_list.append(self.case_finish_time[i] - self.alg_finish_at[i])
            alg_finish_at_to_case_finish_time_list.sort()
            series_time_to_case_finish_time_list.append(self.case_finish_time[i] - self.series_time_list[i])
            series_time_to_case_finish_time_list.sort()

        rebot_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=4f0ed06d-731f-44ce-bc5c-1c94d27cd8b0'
        # rebot_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=9fd2cbde-b67d-40e7-83b5-465d94255182'

        case_finish_time_copy = self.case_finish_time.copy()
        case_finish_time_copy.sort()
        series_time_list_copy = self.series_time_list.copy()
        series_time_list_copy.sort()
        self.data = {
            "msgtype": "markdown",
            "markdown": {
                "content": f"端到端测试场景一,结果统计如下:\n"
                           f"共计算成功<font color=\"warning\">{self.num}</font>个，平均数量<font color=\"warning\">{int(self.image_count/self.num)}</font>张\n"
                           f"series_time->series_create_time 最大 <font color=\"warning\">{seies_time_to_series_create_time_list[-1]}</font> 中位数 <font color=\"warning\">{seies_time_to_series_create_time_list[int(int(self.num/2))]}</font> 最小值 <font color=\"warning\">{seies_time_to_series_create_time_list[0]}</font> 平均值 <font color=\"warning\">{int(np.mean(seies_time_to_series_create_time_list))}</font></font> 标准差 <font color=\"warning\">{int(np.std(seies_time_to_series_create_time_list,ddof=1))}</font>\n"
                           f"receive_end_time->series_receive_time 最大 <font color=\"warning\">{receive_end_time_to_series_receive_time_list[-1]}</font> 中位数 <font color=\"warning\">{receive_end_time_to_series_receive_time_list[int(self.num/2)]}</font> 最小值 <font color=\"warning\">{receive_end_time_to_series_receive_time_list[0]}</font> 平均值 <font color=\"warning\">{int(np.mean(receive_end_time_to_series_receive_time_list))}</font></font> 标准差 <font color=\"warning\">{int(np.std(receive_end_time_to_series_receive_time_list,ddof=1))}</font>\n"
                           f"case_create_time->alg_start_at 最大 <font color=\"warning\">{case_create_time_to_alg_start_at_list[-1]}</font> 中位数 <font color=\"warning\">{case_create_time_to_alg_start_at_list[int(self.num/2)]}</font> 最小值 <font color=\"warning\">{case_create_time_to_alg_start_at_list[0]}</font> 平均值 <font color=\"warning\">{int(np.mean(case_create_time_to_alg_start_at_list))}</font></font> 标准差 <font color=\"warning\">{int(np.std(case_create_time_to_alg_start_at_list,ddof=1))}</font>\n"
                           f"alg_start_at->alg_finish_at 最大 <font color=\"warning\">{alg_start_at_to_alg_finish_at_list[-1]}</font> 中位数 <font color=\"warning\">{alg_start_at_to_alg_finish_at_list[int(self.num/2)]}</font> 最小值 <font color=\"warning\">{alg_start_at_to_alg_finish_at_list[0]}</font> 平均值 <font color=\"warning\">{int(np.mean(alg_start_at_to_alg_finish_at_list))}</font></font> 标准差 <font color=\"warning\">{int(np.std(alg_start_at_to_alg_finish_at_list,ddof=1))}</font>\n"
                           f"alg_finish_at->case_finish_time 最大 <font color=\"warning\">{alg_finish_at_to_case_finish_time_list[-1]}</font> 中位数 <font color=\"warning\">{alg_finish_at_to_case_finish_time_list[int(self.num/2)]}</font> 最小值 <font color=\"warning\">{alg_finish_at_to_case_finish_time_list[0]}</font> 平均值 <font color=\"warning\">{int(np.mean(alg_finish_at_to_case_finish_time_list))}</font></font> 标准差 <font color=\"warning\">{int(np.std(alg_finish_at_to_case_finish_time_list,ddof=1))}</font>\n"
                           f"series_time->case_finish_time 最大 <font color=\"warning\">{series_time_to_case_finish_time_list[-1]}</font> 中位数 <font color=\"warning\">{series_time_to_case_finish_time_list[int(self.num/2)]}</font> 最小值 <font color=\"warning\">{series_time_to_case_finish_time_list[0]}</font> 平均值 <font color=\"warning\">{int(np.mean(series_time_to_case_finish_time_list))}</font></font> 标准差 <font color=\"warning\">{int(np.std(series_time_to_case_finish_time_list,ddof=1))}</font>\n"
                           f"50个case总时间 series_time->case_finish_time <font color=\"warning\">{case_finish_time_copy[-1] - series_time_list_copy[0]}</font>  \n"
            }
        }
        requests.post(url=rebot_url, json=self.data)

    def run(self):
        self.get_sql()
        self.get_result()


if __name__ == '__main__':
    Result().run()