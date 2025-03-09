#!/usr/bin/env bash
#输入磁盘名，每秒跑一次iostat，输出csv文件中, ex: bash iostat_dump.sh sda

diskname=$1


echo $diskname

header=`iostat -d "$diskname" -x -k | grep 'Device' | sed 's/\s\+/,/g'`
echo "time,$header" >> iostat_output.csv

#  清除缓存
sync
echo 3 > /proc/sys/vm/drop_caches

# 开始统计
while true
do
    currentTime=`date "+%Y-%m-%d %H:%M:%S"`
    iostat_result=`iostat -d "$diskname" -x -m -y 1 1 | grep "$diskname" | sed 's/\s\+/,/g'`
    echo "$currentTime,$iostat_result"
    echo "$currentTime,$iostat_result" >> iostat_output.csv
    unset iostat_result
    unset currentTime
    sleep 4
done




