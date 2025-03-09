import json
import pandas as pd
import datetime
import subprocess
import sys
import numpy as np
import re

START_POSTPROCESS_FLG = "start alg task"
COMMITTASK_FLG = "CommitTaskResponse:task_id"
OLD_FINISHJOB_FLG = "postprocess, state: completed, taskId:"
# OLD_ALG_START_FLG = "Receive new start task:{0}, postprocess, {1}".format(product. case_num)


# print(origin_arr)

# coronary_list = []
# cerebral_list = []
# thoracic_list = []


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

def get_alg_scheduler_timelines(task_arr, log_path):

    for task_item in task_arr:
        task_id = task_item[0]
        print(f'taskid: {task_id}')
        _p = subprocess.Popen(f'egrep "(postprocess|detect), state: completed, taskId: {task_id}" {log_path}', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, universal_newlines=True)
        finish_line = _p.communicate()[0].strip('\n')
        #如果根据taskid找不到postprocess|detect 类型的scheduler log，则为followup，HI等类型任务，跳过
        print(type(finish_line))
        print(finish_line == None)
        print(f'finish line: {finish_line}')
        if(finish_line == ''):
            service = 'skip'
            case_num = ''
            scheduler_start_time = ''
            scheduler_commit_time = ''
            scheduler_finish_time = ''
            task_item.extend([service, case_num, scheduler_start_time, scheduler_commit_time, scheduler_finish_time])
            continue
        # finish_line = _p.stdout.readline().strip('\n')
        # print(f'finish line: {finish_line}')
        
        scheduler_finish_time = get_timestamp(finish_line)
        case_num = re.search(r"T\d{14}H\w{8}", finish_line).group()

        print(f'scheduler_finish_time: {scheduler_finish_time}')
        print(f'case_num: {case_num}')


        service = re.search(r"cerebral|coronary|thoracic", finish_line).group()
        
        _p1 = subprocess.Popen(f'egrep "start alg task (cerebral|coronary|thoracic) {case_num} (postprocess|detect)" {log_path}', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, universal_newlines=True)
        start_line = _p1.communicate()[0].strip('\n')
        # start_line = _p1.stdout.readline().strip('\n')
        # print(f'start line: {start_line}')
        scheduler_start_time = get_timestamp(start_line)
        print(f'scheduler_start_time: {scheduler_start_time}')

        search_cmd = f'grep \'CommitTaskResponse:task_id: \"{task_id}\"\' {log_path}'
        # print(f'-----------------search_cmd: {search_cmd}')
        _p2 = subprocess.Popen(search_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, universal_newlines=True)
        commit_line = _p2.communicate()[0].strip('\n')
        # commit_line = _p2.stdout.readline().strip('\n')
        # print(f'commit line: {commit_line}')

        scheduler_commit_time = get_timestamp(commit_line)
        print(f'scheduler_commit_time: {scheduler_commit_time}')

        task_item.extend([service, case_num, scheduler_start_time, scheduler_commit_time, scheduler_finish_time])




if __name__ == '__main__':
    log_path = sys.argv[1]

    data = pd.read_csv('/data1/jenkins_scripts/thoracic_200_kernel.csv', sep=',',header=0,usecols=[0,1,2,3])

    origin_arr = data.values.tolist()
    # print(origin_arr)
    get_alg_scheduler_timelines(origin_arr, log_path)
    # print(origin_arr)

    df = pd.DataFrame(origin_arr, columns=["task_id", "kernel_create_time", "kernel_start_time", "kernel_finish_time", "service", "case_num", "scheduler_start_time", "scheduler_commit_time", "scheduler_finish_time"])
    df.to_csv('./alg_scheduler_log.csv')