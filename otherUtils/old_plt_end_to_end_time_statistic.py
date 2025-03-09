import re
import sys
import pandas as pd
import datetime
import subprocess
import numpy as np
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import MetaData, create_engine


# 从数据库中查询当天凌晨到当前时间计算成功的所有心脑胸case，并查找series_instance_uid,product,case_num,study_datetime,series_receive_way,series_date,series_time,series_create_time,case_ctime,case_finish_time
# 根据series_instance_uid和获取方式查询数据拉取时间和推送时间，从而统计全流程时间
sql_uri = 'mysql+pymysql://root:qY1WBZ30vjsriiHiEgK2ZkE8osjYNsj@200.200.200.200:13306/plt_dicom?charset=utf8mb4'

start_time_flag = ''
today = ''
if len(sys.argv) > 1 and sys.argv[1]:
    #之前的
    today = sys.argv[1]
    start_time_flag = sys.argv[1] + ' 00:00:00'
    end_time_flag = sys.argv[1] + ' 23:59:00'
    DICOM_LOG_PATH = f"/data1/log/plt-data-service/info.{today}.log"
    DICOM_FULL_LOG_PATH = f"/data1/log/plt-data-service/dicom-info.{today}.log"
    _p = subprocess.Popen(f'gzip -d {DICOM_LOG_PATH}.gz && gzip -d {DICOM_FULL_LOG_PATH}.gz', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, universal_newlines=True)
    _p.communicate()[0].strip('\n')
    SQL_STATEMENT = f"select t_series.series_instance_uid,thoracic_cases.case_num, thoracic_cases.study_datetime, t_series.from_pull as series_receive_way,thoracic_cases.series_datetime as series_datetime, t_series.created_at as series_create_time,thoracic_cases.upload_time as case_create_time, thoracic_cases.alg_start_at,thoracic_cases.alg_finish_at, thoracic_cases.finish_time as case_finish_time from plt_dicom.series as t_series, plt_thoracic.cases as thoracic_cases  where thoracic_cases.identifier = t_series.series_instance_uid and series_datetime  > '{start_time_flag}' and series_datetime < '{end_time_flag}' and thoracic_cases.state=2 order by thoracic_cases.upload_time asc;"
    
else:
    #当天
    start_time_flag = datetime.datetime.now().strftime('%Y-%m-%d 00:00:00')
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    DICOM_LOG_PATH = "/data1/log/plt-data-service/info.log"
    DICOM_FULL_LOG_PATH = "/data1/log/plt-data-service/dicom-info.log"
    SQL_STATEMENT = f"select t_series.series_instance_uid,thoracic_cases.case_num, thoracic_cases.study_datetime, t_series.from_pull as series_receive_way,thoracic_cases.series_datetime as series_datetime, t_series.created_at as series_create_time,thoracic_cases.upload_time as case_create_time, thoracic_cases.alg_start_at,thoracic_cases.alg_finish_at, thoracic_cases.finish_time as case_finish_time from plt_dicom.series as t_series, plt_thoracic.cases as thoracic_cases  where thoracic_cases.identifier = t_series.series_instance_uid and series_datetime  > '{start_time_flag}' and thoracic_cases.state=2 order by thoracic_cases.upload_time asc;"

# print(start_time_flag)






def get_timestamp(log_text):
    time_stamp = re.search(r'\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}', log_text).group()
    return time_stamp

engine = create_engine(sql_uri,pool_recycle=3600, echo=False)
Session = sessionmaker(bind=engine)

meta = MetaData()
meta.reflect(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

Base = automap_base(metadata=meta)
Base.prepare()

result = session.execute(SQL_STATEMENT).fetchall()
session.close()

origin_arr = []

for record in result:
    # print()
    #开始查询拉取或接受时间
    receive_start_time = ''
    receive_end_time = ''
    find_series_time = ''
    move_start_time = ''
    move_end_time = ''
    # print(record[0])

    #如果是被动接收的数据
    if record[3] == 'FROM_PUSH':
        series_instance_uid = record[0]
        print(series_instance_uid)
        #第一行
        _p = subprocess.Popen(f'grep "{series_instance_uid}" {DICOM_FULL_LOG_PATH} | head -n 1', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, universal_newlines=True)
        raw_line = _p.communicate()[0].strip('\n')
        if raw_line == '':
            print(f'{series_instance_uid} not found in {DICOM_FULL_LOG_PATH}')
        else:
            receive_start_time = get_timestamp(raw_line)

        #最后一行
        _p = subprocess.Popen(f'grep "{series_instance_uid}" {DICOM_FULL_LOG_PATH} | tail -n 1', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, universal_newlines=True)
        raw_line = _p.communicate()[0].strip('\n')
        if raw_line == '':
            print(f'{series_instance_uid} not found in {DICOM_FULL_LOG_PATH}')
        else:
            receive_end_time = get_timestamp(raw_line)

    
    #如果是主动拉取的数据
    elif record[3] == 'FROM_PULL':
        series_instance_uid = record[0]
        _p = subprocess.Popen(f'grep "add {series_instance_uid}" {DICOM_LOG_PATH} | head -n 1', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, universal_newlines=True)
        raw_line = _p.communicate()[0].strip('\n')
        if raw_line == '':
            print(f'{series_instance_uid} not found in {DICOM_LOG_PATH}')
        else:
            find_series_time = get_timestamp(raw_line)
        
        _p = subprocess.Popen(f'grep "add {series_instance_uid} to move queue" {DICOM_LOG_PATH} | head -n 1', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, universal_newlines=True)
        raw_line = _p.communicate()[0].strip('\n')
        if raw_line == '':
            print(f'{series_instance_uid} not found in {DICOM_LOG_PATH}')
        else:
            move_start_time = get_timestamp(raw_line)

        _p = subprocess.Popen(f'grep "move success {series_instance_uid}" {DICOM_LOG_PATH} | head -n 1', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, universal_newlines=True)
        raw_line = _p.communicate()[0].strip('\n')
        if raw_line == '':
            print(f'{series_instance_uid} not found in {DICOM_LOG_PATH}')
        else:
            move_end_time = get_timestamp(raw_line)

    
    tmp_arr = list(record)
    tmp_arr = tmp_arr[:5] + [receive_start_time, receive_end_time, find_series_time, move_start_time, move_end_time] + tmp_arr[5:]
    
    origin_arr.append(tmp_arr)

df = pd.DataFrame(origin_arr, columns=["series_instance_uid","case_num","study_datetime","series_receive_way","series_datetime","receive_start_time","receive_end_time", "find_series_time", "move_start_time", "move_end_time","series_create_time","case_create_time","alg_start_at","alg_finish_at","case_finish_time"])
df.to_csv(f'./old_plt_e2e_time_statistic_{today}.csv')
