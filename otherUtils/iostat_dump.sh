#!/usr/bin/env bash
#输入磁盘名，每秒跑一次iostat，输出csv文件中, ex: bash iostat_dump.sh sda

diskname=$1


echo $diskname
mv temp.csv temp.csv.old

header=`iostat -d "$diskname" -x -k | grep 'Device' | sed 's/\s\+/,/g'`
echo "$header" >> temp.csv

#  清除缓存
sync
echo 3 > /proc/sys/vm/drop_caches

# 等待alg-job起来
while [[ -z $(docker ps | grep 'run T') ]]
do
    echo '等待alg-job起来，sleep 1s'
    sleep 1
done

# 开始统计
while [[ -n $(docker ps | grep 'run T') ]]
do
    iostat_result=`iostat -d "$diskname" -x -m -y 1 1 | grep "$diskname" | sed 's/\s\+/,/g'`
    echo "$iostat_result"
    echo "$iostat_result" >> temp.csv
    unset iostat_result
done

sleep 5
echo 'alg finished'


