#!/usr/bin/env bash
# 统计docker stats 输出的io平均值 运行方式 bash io_avg.sh xxxxx.log

rm -rf test_io.csv
# 输出case_num
all_case=`cat $1 | awk -F '-' '{print $3}' | sort | uniq`
for case in $all_case
do
    echo $case|tr "\n" "," >> test_io.csv
    size_i=`grep $case $1 |awk -F ' ' '{print $11}'|grep 'MB'| awk -F 'MB' '{print $1}'|awk 'BEGIN {max = 0} {if ($1+0 > max+0) max=$1} END {print max}'`
    if [ $size_i = 0 ];then
        echo $case 'I：' `grep $case $1 |awk -F ' ' '{print $11}'|grep 'kB'|awk 'BEGIN {max = 0} {if ($1+0 > max+0) max=$1} END {print "Max=", max}'`
        ikB=`cat $1 |grep $case |awk -F ' ' '{print $11}'|grep 'kB'| awk -F 'kB' '{print $1}'|awk 'BEGIN {max = 0} {if ($1+0 > max+0) max=$1} END {print max}'`
        echo 'i为kB：'$ikB
        iMB=$(printf "%.5f" `echo "scale=2;$ikB/1024"|bc`)
        echo $iMB |tr "\n" ",">> test_io.csv
    else
        echo $case 'I：' `grep $case $1 |awk -F ' ' '{print $11}'|grep 'MB'|awk 'BEGIN {max = 0} {if ($1+0 > max+0) max=$1} END {print "Max=", max}'`
        cat $1 |grep $case |awk -F ' ' '{print $11}'|grep 'MB'| awk -F 'MB' '{print $1}'|awk 'BEGIN {max = 0} {if ($1+0 > max+0) max=$1} END {print max}'|tr "\n" ",">> test_io.csv
    fi
    size_o=`grep $case $1 |awk -F ' ' '{print $13}'|grep 'MB'| awk -F 'MB' '{print $1}'|awk 'BEGIN {max = 0} {if ($1+0 > max+0) max=$1} END {print max}'`
    if [ $size_o = 0 ];then
        echo $case 'O：' `grep $case $1 |awk -F ' ' '{print $13}'|grep 'kB'|awk 'BEGIN {max = 0} {if ($1+0 > max+0) max=$1} END {print "Max=", max}'`
        okB=`cat $1 |grep $case |awk -F ' ' '{print $13}'|grep 'kB'| awk -F 'kB' '{print $1}'|awk 'BEGIN {max = 0} {if ($1+0 > max+0) max=$1} END {print max}'`
        echo 'O为kB：'$okB
        oMB=$(printf "%.5f" `echo "scale=5;$okB/1024"|bc`)
        echo $oMB |tr "\n" ",">> test_io.csv
    else
        echo $case 'O：' `grep $case $1 |awk -F ' ' '{print $13}'|grep 'MB'|awk 'BEGIN {max = 0} {if ($1+0 > max+0) max=$1} END {print "Max=", max}'`
        cat $1 |grep $case |awk -F ' ' '{print $13}'|grep 'MB'| awk -F 'MB' '{print $1}'|awk 'BEGIN {max = 0} {if ($1+0 > max+0) max=$1} END {print max}'|tr "\n" ",">> test_io.csv
    fi
    echo '\n' >> test_io.csv
    echo '-------------'

done
echo 'I_avg:' `cat test_io.csv |awk -F ',' '{print $2}'|awk '{ sum += $0 } END { print(sum / NR) }'`'MB'
i_avg=`cat test_io.csv |awk -F ',' '{print $2}'|awk '{ sum += $0 } END { print(sum / NR) }'`
i_avg_kB=$(printf "%.5f" `echo "scale=5;$i_avg*1024"|bc`)
echo 'I_avg:' $i_avg_kB'kB'

echo 'O_avg:' `cat test_io.csv |awk -F ',' '{print $3}'|awk '{ sum += $0 } END { print(sum / NR) }'`'MB'
o_avg=`cat test_io.csv |awk -F ',' '{print $3}'|awk '{ sum += $0 } END { print(sum / NR) }'`
o_avg_kB=$(printf "%.5f" `echo "scale=5;$o_avg*1024"|bc`)
echo 'O_avg:' $o_avg_kB'kB'