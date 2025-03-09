import re
import sys
import csv
import datetime
import subprocess
import numpy as np
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import MetaData, create_engine

# 从数据库中查询当天凌晨到当前时间计算成功的所有心脑胸case，并查找series_instance_uid,product,case_num,study_datetime,series_receive_way,series_date,series_time,series_create_time,case_ctime,case_finish_time
# 根据series_instance_uid和获取方式查询数据拉取时间和推送时间，从而统计全流程时间
sql_uri = 'mysql+pymysql://root:qY1WBZ30vjsriiHiEgK2ZkE8osjYNsj@200.200.200.200:13306/plt_universe?charset=utf8mb4'

start_time_flag = ''


#之前的


def run():
    total_arr = []
    tmp_arr = get_today_result()
    total_arr.extend(tmp_arr)

    print(total_arr)
    with open(f'./sk_e2e_time_statistic_cn_tmp.csv','w') as result_csv:
            
        writer = csv.writer(result_csv)
        writer.writerow(["患者编号","数坤产品名称","数坤病例编号","检查时间","序列日期","序列时间","数坤系统病例入库时间","数坤系统创建病例时间","计算开始时间","计算完成时间","数坤系统入库完成时间"])
        writer.writerows(total_arr)
        result_csv.close()
    
        
        


def get_timestamp(log_text):
    time_stamp = re.search(r'\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}', log_text).group()
    return time_stamp

def get_today_result():
    
    start_time_flag = '2021-03-03 00:00:00'
    end_time_flag = '2022-09-28 23:59:00'
    # writer.writerow(["series_instance_uid","product","case_num","study_datetime","series_date","series_time","series_create_time","case_create_time","alg_start_time","alg_end_time","case_finish_time"])
    # SQL_STATEMENT = f"select t_series.series_instance_uid,t_workflow.key as product,t_case.case_num, t_case.study_datetime,t_series.series_date,t_series.series_time, t_series.ctime as series_create_time,t_case.ctime as case_create_time, t_case.finish_time as case_finish_time from plt_universe.t_series as t_series, plt_universe.t_case as t_case, plt_universe.t_workflow as t_workflow where t_case.workflow_id = t_workflow.id and t_case.workflow_id in (1,2,4,6) and t_case.series_id = t_series.id and t_case.study_datetime  > '{start_time_flag}' and  t_case.study_datetime < '{end_time_flag}' and t_case.state=400 order by t_series.ctime asc;"
    SQL_STATEMENT = f"select s.patient_number,w.key as product, c.case_num, c.study_datetime, s.series_date,s.series_time,s.ctime as series_create_time,c.ctime as case_create_time,c.finish_time as case_finish_time from t_case c JOIN t_series s on c.series_id = s.id  JOIN t_workflow w on c.workflow_id = w.id where c.study_datetime  > '{start_time_flag}' and  c.study_datetime < '{end_time_flag}' and c.state in (400,700) order by s.ctime desc;"
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

    today_arr = []

    

    if len(result) == 0:
        print(result)
        return today_arr

    for record in result:
        today = record[7]
        print(today)
        formated_today = today.strftime('%Y-%m-%d')
        ALG_LOG_PATH = f"/data1/log/plt-alg-scheduler/info.{formated_today}.log"

        #解压日志
        _p = subprocess.Popen(f'gzip -d {ALG_LOG_PATH}.gz', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, universal_newlines=True)
        _p.communicate()[0].strip('\n')
        # print()
        alg_start_time = ''
        alg_end_time = ''

        case_num = record[2]
        product = record[1]
        
        #开始查询alg时间
        #- start alg task {product}
        _p = subprocess.Popen(f'grep "start alg task {product} {case_num}" {ALG_LOG_PATH} | head -n 1', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, universal_newlines=True)
        raw_line = _p.communicate()[0].strip('\n')
        if raw_line == '':
            print(f'{case_num} not found in {ALG_LOG_PATH}')
        else:
            alg_start_time = get_timestamp(raw_line)
            print(f'alg_start_time of {case_num}: {alg_start_time}')

        #- end alg task {product}
        _p = subprocess.Popen(f'grep "end alg task {product} {case_num}" {ALG_LOG_PATH} | head -n 1', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, universal_newlines=True)
        raw_line = _p.communicate()[0].strip('\n')
        if raw_line == '':
            print(f'{case_num} not found in {ALG_LOG_PATH}')
        else:
            alg_end_time = get_timestamp(raw_line)
            print(f'alg_end_time of {case_num}: {alg_end_time}')
        
        tmp_arr = list(record)
        tmp_arr = tmp_arr[:8] + [alg_start_time, alg_end_time] + tmp_arr[-1:]
        

        print(tmp_arr)
        today_arr.append(tmp_arr)
        
    print(f'{formated_today} result finish')
    return today_arr

        



if __name__ == '__main__':
    run()

