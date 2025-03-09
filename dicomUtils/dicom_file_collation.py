#  -*-coding:utf8 -*-
import shutil
import subprocess
import pydicom
import sys
import os
# 整理所有输入目录下的所有文件，并将文件的名称重命名为Series_Instance_Uid.然后去掉重复的文件夹

def get_series_id(path=''):
    command = 'find ' + path + " -name *.dcm -type f | head -n 1"
    _p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, universal_newlines=True)
    _p.wait()

    if (_p.returncode == 0):
        file_name = _p.stdout.readline().strip('\n')
        if(file_name == ''):
            print(path + ' 没有dcm文件')
            raise Exception('没有dcm文件')
            # return 'empty_folder'
        print(file_name)
        ds = pydicom.dcmread(file_name, force=True)
        series_instance_uid = ds.SeriesInstanceUID
        print(series_instance_uid)
        return series_instance_uid
    else:
        return 'empty_folder'

def get_collation(base_dir = ''):
    folder_seriesid_map = {}
    folder_list = os.listdir(base_dir)
    for folder in folder_list:
        if folder == 'cerebral-3000':
            continue
        series_instance_uid = get_series_id(os.path.join(base_dir,folder))
        if series_instance_uid in folder_seriesid_map:
            folder_seriesid_map[series_instance_uid].append(folder)
        else:
            folder_seriesid_map[series_instance_uid] = [folder]
    
    print(len(folder_seriesid_map))
    print(folder_seriesid_map)
    return folder_seriesid_map

def remove_duplicate(base_dir = ''):
    f_s_map = get_collation(base_dir)
    for series_id in f_s_map:
        if len(f_s_map[series_id]) > 1:
            # print(series_id)
            
            tmp_list = f_s_map[series_id]
            tmp_list.sort()
            print(f_s_map[series_id])

            #从多个相同series_instance_uid的文件夹中删除多余的文件夹，保留T开头的
            for folder in tmp_list[:-1]:
                print('删除文件夹' + os.path.join(base_dir, folder))
                shutil.rmtree(os.path.join(base_dir, folder), ignore_errors=True)
            
            #将多余的folder从f_s_map中删除
            f_s_map[series_id] = tmp_list[-1]
            print('重命名文件夹 ' + os.path.join(base_dir, f_s_map[series_id]) + ' to ' + os.path.join(base_dir, series_id))
            os.rename(os.path.join(base_dir, f_s_map[series_id]), os.path.join(base_dir, series_id))
        else:
            print('重命名文件夹 ' + os.path.join(base_dir, f_s_map[series_id][0]) + ' to ' + os.path.join(base_dir, series_id))
            os.rename(os.path.join(base_dir, f_s_map[series_id][0]), os.path.join(base_dir, series_id))
            
    
   

if __name__ == '__main__':
    dir = sys.argv[1]
    print(dir)
    remove_duplicate(dir)