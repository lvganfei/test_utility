#!/usr/bin/env bash
#输入想查询的目录，可以指定跳过的子目录
root=$1 skipsubdir=$2
all_potiential_files=`find $root -path "./docker" -prune -o -path "$skipsubdir" -prune -o  -name *.dcm -size +100k -type f`

for file in $all_potiential_files
do
    is_dcm=`dcmftest $file | awk -F ':' '{print $1}'`
    if [[ $is_dcm = 'yes' ]]; 
    then
        patient_id=`dcmdump -L --search 0010,0020 $file |  awk -F '[' '{print $2}'| awk -F ']' '{print $1}'`
        if [[ $patient_id =~ 'sk_' || $patient_id =~ 'anony' ]];
        then
             echo 'pass'
         else
             echo "$file 未脱敏"
             echo $file >> not_tuomin.log
        fi
    else
        echo "$file not dcm file"
    fi
done