#! /bin/bash
# 检查文件是否存在，不存在保存
folder_list=$1

for folder in `cat $folder_list`;
  do
    if [[ -d "/data1/universe-longrun-data/coronary/$folder" ]]
    then
        echo 'exist'
    else
        echo $folder >> miss_list.log
    fi
  done
