# -*- coding: utf-8 -*-

import argparse
import os
import pandas as pd
import re

HIDDEN_FILE = '.assklog'
DEFALUT_OUTPUT_FILE = './log-timestamp.csv'

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog = 'get timestamp from assk log')
    
    parser.add_argument('directory', type=str, help='target directory')
    parser.add_argument('-g', '--grep-condition', type=str, default='', help='grep condition, defalut is ""')
    parser.add_argument('-o', '--output-file', type=str, default=DEFALUT_OUTPUT_FILE, help='output csv file, default is ./log-timestamp.csv')
    
    args = parser.parse_args()

    target_dir = re.sub("/$", "", args.directory)
    grep_condition: str = args.grep_condition
    output_file: str = args.output_file
    
    done_condition = 'State is DONE'
    os.system(f"grep '{grep_condition}' {target_dir} | grep '{done_condition}' > {HIDDEN_FILE}")
    
    task_timestamps = {}
    
    with open(HIDDEN_FILE, 'r') as f:
        for line in f.readlines():
            task_id = re.search(r"Task\.(\w+)", line).group(1)
            
            done_time = re.search(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", line).group(0)
            
            task_timestamps[task_id] = {'done':done_time}
    
    create_condition = 'Create task'
    os.system(f"grep '{grep_condition}' {target_dir} | grep '{create_condition}' > {HIDDEN_FILE}")

    with open(HIDDEN_FILE, 'r') as f:
        for line in f.readlines():
            task_id = re.search(r"Create task (\w+)", line).group(1)
            
            if task_id is None or task_timestamps.get(task_id) is None:
                continue
            
            crate_time = re.search(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", line).group(0)
            
            task_timestamps[task_id]['create'] = crate_time
            
    doing_condition = 'State is DOING'
    os.system(f"grep '{grep_condition}' {target_dir} | grep '{doing_condition}' > {HIDDEN_FILE}")

    with open(HIDDEN_FILE, 'r') as f:
        for line in f.readlines():
            task_id = re.search(r"Task\.(\w+)", line).group(1)
            
            if task_id is None or task_timestamps.get(task_id) is None:
                continue
            
            doing_time = re.search(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", line).group(0)
            
            task_timestamps[task_id]['doing'] = doing_time
    
    dataframe = pd.DataFrame(task_timestamps)
    dataframe = pd.DataFrame(dataframe.values.T, index=dataframe.columns, columns=dataframe.index)
    dataframe = dataframe[['create', 'doing', 'done']]
    dataframe.to_csv(output_file)
    
    os.remove(HIDDEN_FILE)
