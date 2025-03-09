import os
import sys
import json
import datetime
import pandas as pd
from sqlalchemy import create_engine





sql_uri = 'mysql+pymysql://root:qY1WBZ30vjsriiHiEgK2ZkE8osjYNsj@10.15.10.216:13306/plt_universe?charset=utf8mb4'



KEYWORDS_MAPPING = {
    "start_flag": "Completed algorithm process",
    "dump_start_flag": "start to gen mip/mip_boned",
    "dump_finished_flag": "vr bone file rename end",
    "end_flag": "smtr: STRUCT_REPORT closed"
}

# sql_statement = f"select case_num from plt_universe.t_case where workflow_id=6 and state = 400 and finish_time > '{today} 00:00:00' order by ctime desc"
cerebral_log_name_prefix = 'worker.log.'



# engine = create_engine(sql_uri)
# cur = engine.execute(sql_statement)

# case_list = list(map(lambda x:x[0], cur.fetchall()))

# print(case_list)

def extract_timestamp(line):
    return datetime.datetime.strptime(line[0:19], '%Y-%m-%d %H:%M:%S').timestamp()

def get_casenum_result(log_base_path):
    casenum_flag = ''
    result_dict = {}

    today = datetime.datetime.now().strftime("%Y-%m-%d")
    # today = '2022-07-07'
    full_name = cerebral_log_name_prefix+today
    with open(f'{log_base_path}/plt-cerebral-srv/{full_name}','r') as f :
        
        while True:
        # 每次读一行，如果找到start_flag，则记住casenum，后面的dump_start_flag，dump_finished_flag，end_flag都以这个
            m = f.readline()
            if m == '':
                break
            is_start_flag = m.rfind(KEYWORDS_MAPPING['start_flag'])
            is_dump_start_flag = m.rfind(KEYWORDS_MAPPING['dump_start_flag'])
            is_dump_finished_flag = m.rfind(KEYWORDS_MAPPING['dump_finished_flag'])
            is_end_flag = m.rfind(KEYWORDS_MAPPING['end_flag'])


            if is_start_flag != -1:
                casenum_start_index = m.rfind('case number: ')
                #new casenum flag
                casenum_flag = m[(casenum_start_index+13):(is_start_flag-1)]
                result_dict[casenum_flag] = {
                    "start_time": extract_timestamp(m),
                    "dump_start":0,
                    "dump_finished":0,
                    "end_time":0}
            
            if is_dump_start_flag != -1:
                result_dict[casenum_flag]["dump_start"] = extract_timestamp(m)

            if is_dump_finished_flag != -1:
                result_dict[casenum_flag]["dump_finished"] = extract_timestamp(m)

            if is_end_flag != -1:
                result_dict[casenum_flag]["end_time"] = extract_timestamp(m)
                #开始计算用时
                result_dict[casenum_flag]['overall_time'] = str(result_dict[casenum_flag]["end_time"] - result_dict[casenum_flag]["start_time"])
                result_dict[casenum_flag]['dump_time'] = str(result_dict[casenum_flag]["dump_finished"] - result_dict[casenum_flag]["dump_start"])
                print(f'case: {casenum_flag} times')
                print(f"overall_time: {result_dict[casenum_flag]['overall_time']}")
                print(f"dump_time: {result_dict[casenum_flag]['dump_time']}")
            else:
                
                continue
        f.close()
    excel_raw_list = []
    for case, case_result in result_dict.items():
        if set(case_result.keys()) == {'end_time', 'dump_start', 'dump_finished', 'start_time', 'overall_time', 'dump_time'}:
            excel_raw_list.append([case, case_result['start_time'], case_result['dump_start'], case_result['dump_finished'], case_result['end_time'], case_result['dump_time'], case_result['overall_time']])
        
    df = pd.DataFrame(excel_raw_list, columns=["casenum", "start_time", "dump_start_time", "dump_finish_time", "end_time", 'dump_time', 'overall_time'])

    xls_path = os.path.join(log_base_path, f'./test_result_{today}.xlsx')
    df.to_excel(xls_path)




if __name__ == '__main__':
    get_casenum_result('/data1/log')