import re
import sys
import pandas as pd
import datetime
import subprocess
import numpy as np
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import MetaData, create_engine

STUDY_INTANCE_LIST = ["1.2.194.0.108707908.20220903082510.1600.10226.764380",
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

# 从数据库中查询当天凌晨到当前时间计算成功的所有心脑胸case，并查找series_instance_uid,product,case_num,study_datetime,series_receive_way,series_date,series_time,series_create_time,case_ctime,case_finish_time
# 根据series_instance_uid和获取方式查询数据拉取时间和推送时间，从而统计全流程时间
sql_uri = 'mysql+pymysql://root:qY1WBZ30vjsriiHiEgK2ZkE8osjYNsj@200.200.200.200:13306/plt_dicom?charset=utf8mb4'
push_record_sql_uri = 'mysql+pymysql://root:qY1WBZ30vjsriiHiEgK2ZkE8osjYNsj@10.12.10.113:13306/plt_dicom?charset=utf8mb4'

DELETE_SERIES_RECORD = "delete from plt_dicom.series where study_instance_uid="
DELETE_SERIES_FIND_RECORD = "delete from plt_dicom.dicom_series_find where study_instance_uid="
DELETE_APPLY_RECORD = "delete from plt_dicom.apply_record where study_instance_uid="
DELETE_DICOM_CASE = "delete FROM plt_dicom.cases where study_instance_uid="
DELETE_THORACIC_CASE = "delete from plt_thoracic.cases where study_identifier="
DELETE_STUDY_RECORD = "delete from plt_dicom.study where study_instance_uid="
SELECT_CASENUM = "SELECT case_num FROM plt_thoracic.cases where study_identifier="

DELETE_PUSH_RECORD = "TRUNCATE `universe_test`.`push_statistics`"

#按照Study_instance_uid逐个删除数据

engine = create_engine(sql_uri,pool_recycle=3600, echo=False)
Session = sessionmaker(bind=engine)

meta = MetaData()
meta.reflect(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

Base = automap_base(metadata=meta)
Base.prepare()

for study_instance_uid in STUDY_INTANCE_LIST:
    print(study_instance_uid)
    DELETE_SERIES_RECORD_STATEMENT = f"{DELETE_SERIES_RECORD}'{study_instance_uid}'"
    DELETE_SERIES_FIND_RECORD_STATEMENT = f"{DELETE_SERIES_FIND_RECORD}'{study_instance_uid}'"
    DELETE_APPLY_RECORD_STATEMENT = f"{DELETE_APPLY_RECORD}'{study_instance_uid}'"
    DELETE_DICOM_CASE_STATEMENT = f"{DELETE_DICOM_CASE}'{study_instance_uid}'"
    DELETE_THORACIC_CASE_STATEMENT = f"{DELETE_THORACIC_CASE}'{study_instance_uid}'"
    DELETE_STUDY_STATEMENT = f"{DELETE_STUDY_RECORD}'{study_instance_uid}'"
    SELECT_CASENUM_STATEMENT = f"{SELECT_CASENUM}'{study_instance_uid}'"

    session.execute(DELETE_SERIES_RECORD_STATEMENT)
    session.execute(DELETE_SERIES_FIND_RECORD_STATEMENT)
    session.execute(DELETE_APPLY_RECORD_STATEMENT)
    session.execute(DELETE_DICOM_CASE_STATEMENT)    
    case_num_list = session.execute(SELECT_CASENUM_STATEMENT).fetchall()
    print(case_num_list)

    for case_num in case_num_list:
        #删除source，output
        print(case_num[0])
        _p0 = subprocess.Popen(f'rm -rf /data1/data/output/thoracic/{case_num[0]}', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, universal_newlines=True)
        _p0.communicate()
        _p1 = subprocess.Popen(f'rm -rf /data1/data/source/thoracic/{case_num[0]}', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, universal_newlines=True)
        _p1.communicate()


    session.execute(DELETE_THORACIC_CASE_STATEMENT)
    session.execute(DELETE_STUDY_STATEMENT)
    session.commit()

    #删除original目录
    _p2 = subprocess.Popen(f'rm -rf /data1/data/original/{study_instance_uid}', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, universal_newlines=True)
    _p2.communicate()

session.close()
