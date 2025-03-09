#!/usr/bin/env bash
#通过sar -B 1 1 和vmstat -an命令获取内存信息

sarheader=`sar -B 1 1 | grep 'pgpgin' | sed 's/\s\+/,/g'`
vmstatheader=`vmstat -n 1 1 | grep 'swpd' | sed 's/\s\+/,/g'`
echo "$sarheader" >> sar_output.csv
echo "time,$vmstatheader" >> vmstat_output.csv


# 开始统计
while true
do
    currentTime=`date "+%Y-%m-%d %H:%M:%S"`
    paging_result=`sar -B 1 1 | sed -n '4p' | sed 's/\s\+/,/g'`
    vmstat_result=`vmstat -n 1 2 | sed -n '4p' | sed 's/\s\+/,/g'`
    # echo "$currentTime,$iostat_result"
    echo "$paging_result" >> sar_output.csv
    echo "$currentTime,$vmstat_result" >> vmstat_output.csv
    unset paging_result
    unset vmstat_result
    unset currentTime
    sleep 4
done