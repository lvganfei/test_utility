import json
import pandas as pd
import datetime
import sys
import numpy as np
import re
from sqlalchemy import create_engine


OLD_ALG_START_FLG = "Receive new start task"
ASSIGN_GPU_FLG = "Assign task "
OLD_CREATJOB_FLG = "CMD: [run, T"
OLD_FINISHJOB_FLG = '"progress_status":"completed","status":"completed"'
sql_uri = 'mysql+pymysql://root:qY1WBZ30vjsriiHiEgK2ZkE8osjYNsj@127.0.0.1:13306/plt_dicom?charset=utf8mb4'
# OLD_ALG_START_FLG = "Receive new start task:{0}, postprocess, {1}".format(product. case_num)


# print(origin_arr)

# coronary_list = []
# cerebral_list = []
# thoracic_list = []

def find_casenum_from_sql(origin_arr,case_num):
    for i in range(len(origin_arr)):
        sql_statement = f'select series_instance_uid FROM plt_dicom.apply_record where case_num = "{case_num}" limit 1'

        engine = create_engine(sql_uri)
        cur = engine.execute(sql_statement)
        test_data = cur.fetchone()
        series_instance_uid = test_data[0]
        if origin_arr[i][0] == series_instance_uid:
            return i
    return -1

def find_casenum(origin_arr,case_num):
    for i in range(len(origin_arr)):
        if origin_arr[i][1] == case_num:
            return i
    return -1
def get_timestamp(log_text):
    time_stamp = re.search(r'\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}', log_text).group()
    return time_stamp

    
# for item in origin_arr:
#     if item[2] == 'cerebral':
#         cerebral_list.append(item)
#     elif item[2] == 'coronary':
#         coronary_list.append(item)
#     elif item[2] == 'thoracic':
#         thoracic_list.append(item)
#     else:
#         print('odd_item')
# print(coronary_list[0][1])

def get_old_alg_timelines(case_arr, log_path):
    with open(log_path,'r') as log_f:
        log_lines = log_f.readlines()
        for line in log_lines:
            if line.find(OLD_ALG_START_FLG) > 0:
                case_num = re.search(r"T\d{14}H\w{8}", line).group()
                print(f'now find {case_num} times')
                case_idx = find_casenum(origin_arr, case_num)
                if case_idx != -1:
                    alg_start_time = get_timestamp(line)
                    # case_arr[case_idx][1] = case_num
                    #解决肺结节随访导致的time重复错误
                    if case_arr[case_idx][3] == 0 or case_arr[case_idx][3] == '':
                        case_arr[case_idx][3] = alg_start_time

            if line.find(ASSIGN_GPU_FLG) > 0:
                case_num = re.search(r"T\d{14}H\w{8}", line).group()
                case_idx = find_casenum(origin_arr, case_num)
                if case_idx != -1:
                    assign_gpu_time = get_timestamp(line)
                    #解决肺结节随访导致的time重复错误
                    if (case_arr[case_idx][5] == 0 or case_arr[case_idx][5] == '') and datetime.datetime.strptime(assign_gpu_time,"%Y-%m-%d %H:%M:%S") > datetime.datetime.strptime(case_arr[case_idx][3],"%Y-%m-%d %H:%M:%S"):
                        case_arr[case_idx][4] = assign_gpu_time
                
            elif line.find(OLD_CREATJOB_FLG) > 0:
                case_num = re.search(r"T\d{14}H\w{8}", line).group()
                case_idx = find_casenum(origin_arr, case_num)
                if case_idx != -1:
                    create_job_time = get_timestamp(line)
                    case_arr[case_idx][5] = create_job_time

            elif line.find(OLD_FINISHJOB_FLG) > 0:
                case_num = re.search(r"T\d{14}H\w{8}", line).group()
                case_idx = find_casenum(origin_arr, case_num)
                if case_idx != -1:
                    finish_job_time = get_timestamp(line)
                    
                    if case_arr[case_idx][6] == 0 or case_arr[case_idx][6] == '':
                        case_arr[case_idx][6] = finish_job_time

if __name__ == '__main__':
    log_path = sys.argv[1]

    data = pd.read_csv('/data1/jenkins_scripts/old_plt_mixed_press_600_0817.csv', sep=',',header=0,usecols=[0,1,2,3,4,5,6])

    origin_arr = data.values.tolist()
    # print(origin_arr)
    get_old_alg_timelines(origin_arr, log_path)
    print(origin_arr)

    df = pd.DataFrame(origin_arr, columns=["series_instance_uid", "case_num", "service", "receive_job_time", "assign_gpu_time", "create_job_time", "finish_job_time"])
    df.to_csv('./old_alg_log.csv')